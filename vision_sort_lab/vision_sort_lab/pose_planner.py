from copy import deepcopy

import rclpy
from geometry_msgs.msg import PoseStamped
from moveit_msgs.msg import MoveItErrorCodes
from moveit_msgs.srv import GetMotionPlan
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from vision_sort_lab.motion_builders import build_pose_plan_request
from vision_sort_lab.motion_errors import describe_moveit_error

import math
from moveit_msgs.srv import GetPositionFK, GetStateValidity

from vision_sort_lab.motion_execution import MotionExecution
from vision_sort_lab.pose_verifier import PoseVerifier
from collections.abc import Callable


class PosePlanner(Node):
    def __init__(
        self,
        result_callback: Callable[[bool, str], None] | None = None,
        *,
        demo: bool = True,
    ):
        super().__init__('pose_planner')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.plan_client = self.create_client(
            GetMotionPlan, '/plan_kinematic_path'
        )
        self.plan_future = None
        self.planned_trajectory = None
        self.plan_requested = False
        self.result_callback = result_callback

        self.fk_client = self.create_client(
            GetPositionFK, '/compute_fk'
        )
        self.validity_client = self.create_client(
            GetStateValidity, '/check_state_validity'
        )

        self.fk_future = None
        self.validity_future = None
        self.target_pose = None
        self.target_constraints = None
        self.endpoint_state = None
        self.endpoint_position_ok = False
        self.endpoint_verified = False

        self.execution_succeeded = False
        self.motion_execution = MotionExecution(
            self,
            self.on_execution_finished,
        )

        self.pose_verified = False
        self.pose_verifier = PoseVerifier(
            self,
            self.on_pose_verification_finished,
        )
        self.tool_frame = 'panda_hand'
        self.plan_timer = None
        if demo:
            self.plan_timer = self.create_timer(1.0, self.try_plan)
#----------------------------------------------------#
    def _build_demo_target(self) -> PoseStamped | None:
        try:
            transform = self.tf_buffer.lookup_transform(
                'panda_link0', self.tool_frame, Time()
            )
        except TransformException as exc:
            self.get_logger().info(
                f"TF non ancora disponibile: {exc}"
            )
            return None

        target = PoseStamped()
        target.header.frame_id = 'panda_link0'

        target.pose.position.x = transform.transform.translation.x
        target.pose.position.y = transform.transform.translation.y
        target.pose.position.z = transform.transform.translation.z + 0.03

        target.pose.orientation = deepcopy(
            transform.transform.rotation
        )
        return target
#----------------------------------------------------#
    def request_pose(self, target: PoseStamped) -> bool:

        if not rclpy.ok() or self.plan_requested or target.header.frame_id != 'panda_link0':
            return False

        if self.motion_execution.execution_uncertain:
            self.get_logger().error("Stato dell'ultima esecuzione incerto")
            return False

        if not self.plan_client.service_is_ready():
            self.get_logger().info('In attesa del servizio...')
            return False
        if rclpy.ok():
            self.get_logger().info(
                'Servizio di pianificazione disponibile'
            )

        if not self.fk_client.service_is_ready():
            self.get_logger().info('In attesa del servizio...')
            return False
        if rclpy.ok():
            self.get_logger().info(
                'Servizio di FK disponibile'
            )

        if not self.validity_client.service_is_ready():
            self.get_logger().info('In attesa del servizio...')
            return False
        if rclpy.ok():
            self.get_logger().info(
                'Servizio di State Validitation disponibile'
            )

        if not self.motion_execution.is_ready():
            self.get_logger().info(
                "In attesa dell'esecuzione..."
            )
            return False

        target_snapshot = deepcopy(target)
        request = build_pose_plan_request(target_snapshot, self.tool_frame)

        target_constraints_snapshot = deepcopy(
            request.motion_plan_request.goal_constraints[0]
        )

        position = target_snapshot.pose.position
        orientation = target_snapshot.pose.orientation

        self.get_logger().info(
            f'Target panda_hand in {target_snapshot.header.frame_id}: '
            f'pos=({position.x:.4f}, '
            f'{position.y:.4f}, '
            f'{position.z:.4f}) m | '
            f'q=({orientation.x:.6f}, '
            f'{orientation.y:.6f}, '
            f'{orientation.z:.6f}, '
            f'{orientation.w:.6f})'
        )

        try:
            future = self.plan_client.call_async(request)
        except Exception as exc:
            self.get_logger().error(
                f"Invio della richiesta di pianificazione fallito: {exc}"
            )
            return False
        self.planned_trajectory = None
        self.endpoint_state = None
        self.fk_future = None
        self.validity_future = None
        self.endpoint_position_ok = False
        self.endpoint_verified = False
        self.execution_succeeded = False
        self.pose_verified = False
        self.target_constraints = target_constraints_snapshot
        self.plan_future = future
        self.target_pose = target_snapshot
        self.plan_requested = True
        future.add_done_callback(self.on_plan_response)
        return True
#----------------------------------------------------#
    def try_plan(self) -> None:
        if self.plan_timer is None or self.plan_requested:
            return

        if not rclpy.ok():
            return

        target = self._build_demo_target()
        if target is None:
            return
        submitted = self.request_pose(target)
        if submitted:
            self.plan_timer.cancel()
#----------------------------------------------------#
    def _finish_request(self, succeeded: bool, reason: str) -> None:
        if not self.plan_requested:
            return
        self.plan_requested = False
        self.plan_future = None
        self.fk_future = None
        self.validity_future = None
        message = f'Esito richiesta posa | riuscita={succeeded} | motivo={reason}'
        logger = self.get_logger()

        if succeeded:
            logger.info(message)
        else:
            logger.error(message)

        if self.result_callback is not None:
            self.result_callback(succeeded, reason)
#----------------------------------------------------#
    def on_plan_response(self, future):
        if not self.plan_requested or future is not self.plan_future:
            return
        self.plan_future = None

        try:
            response = future.result()
        except Exception as exc:
            self._finish_request(
                False, f'Errore nella risposta di pianificazione: {exc}'
            )
            return

        if response is None:
            self._finish_request(False, 'Risposta di pianificazione vuota')
            return

        result = response.motion_plan_response
        error_code = result.error_code.val
        error_name = describe_moveit_error(error_code)

        if error_code != MoveItErrorCodes.SUCCESS:
            self._finish_request(False,
                f'Pianificazione fallita: {error_name} ({error_code})'
            )
            return

        points = result.trajectory.joint_trajectory.points

        if not points:
            self._finish_request(False,
                'Ricevuto SUCCESS, ma la traiettoria è vuota'
            )
            return

        self.planned_trajectory = result.trajectory
        self.get_logger().info(
            f'Pianificazione riuscita: {error_name} ({error_code}) | '
            f'tempo={result.planning_time:.3f} s | '
            f'punti={len(points)}'
        )
        self.request_endpoint_fk()
#----------------------------------------------------#
    def request_endpoint_fk(self):
        trajectory = self.planned_trajectory.joint_trajectory
        self.endpoint_position_ok = False
        self.endpoint_verified = False

        if not trajectory.points:
            self._finish_request(False, 'La traiettoria non contiene punti')
            return

        last_point = trajectory.points[-1]

        joint_names = list(trajectory.joint_names)
        joint_positions = list(last_point.positions)

        if len(joint_positions) != len(joint_names):
            self._finish_request(False,
                'Nomi e posizioni hanno lunghezze diverse'
            )
            return

        expected_names = {
            f'panda_joint{i}' for i in range(1, 8)
        }

        if len(joint_names) != 7 or set(joint_names) != expected_names:
            self._finish_request(False,
                f'Nomi dei giunti inattesi: {joint_names}'
            )
            return

        request = GetPositionFK.Request()
        request.header.frame_id = self.target_pose.header.frame_id
        request.fk_link_names = [self.tool_frame]

        request.robot_state.is_diff = True
        request.robot_state.joint_state.name = joint_names
        request.robot_state.joint_state.position = joint_positions

        self.endpoint_state = deepcopy(request.robot_state)
        try:
            self.fk_future = self.fk_client.call_async(request)
        except Exception as exc:
            self._finish_request(False, f'Invio della richiesta FK fallito: {exc}')
            return

        self.fk_future.add_done_callback(self.on_fk_response)
#----------------------------------------------------#
    def on_fk_response(self, future):
        if not self.plan_requested or future is not self.fk_future:
            return
        self.fk_future = None

        try:
            response = future.result()
        except Exception as exc:
            self._finish_request(False, f'Errore nella risposta FK: {exc}')
            return
        if response is None:
            self._finish_request(False, 'Risposta FK vuota')
            return

        error_code = response.error_code.val

        if error_code != MoveItErrorCodes.SUCCESS:
            error_name = describe_moveit_error(error_code)
            self._finish_request(
                False, f'Calcolo FK fallito: {error_name} ({error_code})'
            )
            return

        if (
            len(response.fk_link_names) != 1
            or len(response.pose_stamped) != 1
        ):
            self._finish_request(False, 'Risposta FK con dimensioni inattese')
            return

        returned_link = response.fk_link_names[0]
        predicted = response.pose_stamped[0]

        if returned_link != self.tool_frame:
            self._finish_request(
                False,
                f'Link inatteso: ricevuto {returned_link}, atteso {self.tool_frame}',
            )
            return

        expected_frame = self.target_pose.header.frame_id
        if predicted.header.frame_id != expected_frame:
            self._finish_request(
                False,
                f'Frame inatteso: ricevuto {predicted.header.frame_id}, '
                f'atteso {expected_frame}',
            )
            return


        position = predicted.pose.position
        target_position = self.target_pose.pose.position

        dx = position.x - target_position.x
        dy = position.y - target_position.y
        dz = position.z - target_position.z

        position_error = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        self.endpoint_position_ok = position_error <= 0.005

        orientation = predicted.pose.orientation

        self.get_logger().info(
            f'Posa FK in {predicted.header.frame_id}: '
            f'pos=({position.x:.4f}, {position.y:.4f}, {position.z:.4f}) m | '
            f'q=({orientation.x:.6f}, {orientation.y:.6f}, '
            f'{orientation.z:.6f}, {orientation.w:.6f})'
        )

        self.get_logger().info(
            f'Errore posizione: '
            f'dx={dx * 1000:.3f}, '
            f'dy={dy * 1000:.3f}, '
            f'dz={dz * 1000:.3f} mm | '
            f'distanza={position_error * 1000:.3f} mm | '
            f'entro 5 mm={self.endpoint_position_ok}'
        )

        request = GetStateValidity.Request()
        request.robot_state = deepcopy(self.endpoint_state)
        request.group_name = ''
        request.constraints = deepcopy(self.target_constraints)

        try:
            self.validity_future = self.validity_client.call_async(request)
        except Exception as exc:
            self._finish_request(
                False, f'Invio della richiesta di validità fallito: {exc}'
            )
            return

        self.validity_future.add_done_callback(self.on_endpoint_validity_response)
#----------------------------------------------------#
    def on_endpoint_validity_response(self, future):
        if not self.plan_requested or future is not self.validity_future:
            return
        self.validity_future = None

        # Se lo stato contiene una collisione o non soddisfa i vincoli inviati,
        # il servizio può rispondere normalmente con valid = False
        try:
            response = future.result()
        except Exception as exc:
            self._finish_request(False, f'Errore nella risposta di validità: {exc}')
            return
        if response is None:
            self._finish_request(False, 'Risposta di validità vuota')
            return
        if response.valid:
            self.get_logger().info(
                "Lo stato finale supera la verifica di validità"
            )
        else:
            self.get_logger().info(
                "Lo stato finale non supera la verifica di validità"
            )

        results = [item.result for item in response.constraint_result]
        constraints_ok = len(results) == 2 and all(results)

        self.endpoint_verified = (
            response.valid
            and constraints_ok
            and self.endpoint_position_ok
        )

        message = (
            f'Validità dello stato: {response.valid} | '
            f'Vincoli: {results} | '
            f'Numero di contatti: {len(response.contacts)} | '
            f'Posizione entro 5 mm: {self.endpoint_position_ok} | '
            f'Verifica endpoint: {self.endpoint_verified}'
        )
        if not self.endpoint_verified:
            self._finish_request(False, f'Verifica endpoint fallita. {message}')
            return
        self.get_logger().info(message)
        submitted = self.motion_execution.request_execution(self.planned_trajectory)
        if not submitted:
            self._finish_request(False, 'Invio della traiettoria non avviato')
#----------------------------------------------------#
    def on_execution_finished(self, succeeded):
        if not self.plan_requested:
            return
        self.execution_succeeded = succeeded

        if not succeeded:
            self._finish_request(False, 'Esecuzione della traiettoria fallita')
            return

        self.get_logger().info('Esecuzione conclusa con successo')

        started = self.pose_verifier.start(
            self.target_pose,
            self.target_constraints,
            self.tool_frame,
        )

        if not started:
            self._finish_request(False, 'Avvio della verifica della posa fallito')
#----------------------------------------------------#
    def on_pose_verification_finished(self, succeeded):
        if not self.plan_requested:
            return
        self.pose_verified = succeeded

        if succeeded:
            self._finish_request(True, 'Verifica della posa conclusa con successo')
        else:
            self._finish_request(False, 'Verifica della posa conclusa con esito negativo')



def main(args=None):
    pose_planner = None

    rclpy.init(args=args)
    try:
        pose_planner = PosePlanner()
        rclpy.spin(pose_planner)
    except KeyboardInterrupt:
        pass
    finally:
        if pose_planner is not None:
            pose_planner.pose_verifier.destroy()
            pose_planner.motion_execution.destroy()
            pose_planner.destroy_node()
        rclpy.try_shutdown()
#----------------------------------------------------#

if __name__ == '__main__':
    main()
