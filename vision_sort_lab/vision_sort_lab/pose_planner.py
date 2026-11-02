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


class PosePlanner(Node):
    def __init__(self):
        super().__init__('pose_planner')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.plan_client = self.create_client(
            GetMotionPlan, '/plan_kinematic_path'
        )
        self.plan_future = None
        self.planned_trajectory = None
        self.plan_requested = False

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
        self.plan_timer = self.create_timer(1.0, self.try_plan)

        self.tool_frame = 'panda_hand'

#----------------------------------------------------#
    def try_plan(self):
        # ritornare se self.plan_requested è già vero;
        if self.plan_requested:
            return

        # controllare self.plan_client.service_is_ready(): restituisce un 
        # booleano senza attendere; se falso, ritornare e lasciare ritentare il timer;
        if not rclpy.ok():
            return

        if not self.plan_client.service_is_ready():
            self.get_logger().info('In attesa del servizio...')
            return
        if rclpy.ok():
            self.get_logger().info(
                'Servizio di pianificazione disponibile'    
            )

        if not self.fk_client.service_is_ready():
            self.get_logger().info('In attesa del servizio...')
            return
        if rclpy.ok():
            self.get_logger().info(
                'Servizio di FK disponibile'    
            )

        if not self.validity_client.service_is_ready():
            self.get_logger().info('In attesa del servizio...')
            return
        if rclpy.ok():
            self.get_logger().info(
                'Servizio di State Validitation disponibile'    
            )
    
        if not self.motion_execution.is_ready():
                self.get_logger().info(
                    "In attesa dell'esecuzione..."
                )
                return

        # acquisire TF con il try/except
        try:
            transform = self.tf_buffer.lookup_transform(
                'panda_link0', self.tool_frame, Time()
            )
        except TransformException as exc:
            self.get_logger().info(
                f"TF non ancora disponibile: {exc}"
            )   
            return

        # costruire e stampare il target;
        target = PoseStamped()
        target.header.frame_id = 'panda_link0'

        target.pose.position.x = transform.transform.translation.x
        target.pose.position.y = transform.transform.translation.y
        target.pose.position.z = transform.transform.translation.z + 0.03

        target.pose.orientation = deepcopy(
            transform.transform.rotation
        )

        position = target.pose.position
        orientation = target.pose.orientation

        self.get_logger().info(
            f'Target panda_hand in {target.header.frame_id}: '
            f'pos=({position.x:.4f}, '
            f'{position.y:.4f}, '
            f'{position.z:.4f}) m | '
            f'q=({orientation.x:.6f}, '
            f'{orientation.y:.6f}, '
            f'{orientation.z:.6f}, '
            f'{orientation.w:.6f})'
        )
        
        # inviare una sola richiesta:
        request = build_pose_plan_request(target, self.tool_frame)
        # la verifica deve usare il riferimento dell’operazione corrente.
        self.target_pose = deepcopy(target)
        self.target_constraints = deepcopy(
            request.motion_plan_request.goal_constraints[0]
        )

        self.plan_future = self.plan_client.call_async(request)
        self.plan_requested = True
        self.plan_timer.cancel()
        self.plan_future.add_done_callback(self.on_plan_response)
#----------------------------------------------------#
    def on_plan_response(self, future):
        self.planned_trajectory = None

        try:
            response = future.result()
        except Exception as exc:
            self.get_logger().error(
                f'Errore nel recupero della risposta: {exc}'
            )
            return

        result = response.motion_plan_response
        error_code = result.error_code.val
        error_name = describe_moveit_error(error_code)

        if error_code != MoveItErrorCodes.SUCCESS:
            self.get_logger().error(
                f'Pianificazione fallita: {error_name} ({error_code})'
            )
            return

        points = result.trajectory.joint_trajectory.points

        if not points:
            self.get_logger().error(
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
            self.get_logger().error(
                'La traiettoria non contiene punti'
            )
            return

        last_point = trajectory.points[-1]

        joint_names = list(trajectory.joint_names)
        joint_positions = list(last_point.positions)

        if len(joint_positions) != len(joint_names):
            self.get_logger().warning(
                'Nomi e posizioni hanno lunghezze diverse'
            )
            return

        expected_names = {
            f'panda_joint{i}' for i in range(1, 8)
        }

        if len(joint_names) != 7 or set(joint_names) != expected_names:
            self.get_logger().error(
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

        self.fk_future = self.fk_client.call_async(request)
        self.fk_future.add_done_callback(self.on_fk_response)
#----------------------------------------------------#
    def on_fk_response(self, future):
        try:
            response = future.result()
        except Exception as exc:
            self.get_logger().error(
                f"Errore nel recupero della risposta: {exc}"
            )
            return 
                
        if response.error_code.val != MoveItErrorCodes.SUCCESS:
            error_code = response.error_code.val
            error_name = describe_moveit_error(error_code)
            self.get_logger().error(
                f"Calcolo FK fallito: {error_name} {error_code}"
            )
            return
        
        if (
            len(response.fk_link_names) != 1
            or len(response.pose_stamped) != 1
        ):
            self.get_logger().error(
                'Risposta FK con dimensioni inattese'
                )
            return

        returned_link = response.fk_link_names[0]
        predicted = response.pose_stamped[0]

        if returned_link != self.tool_frame:
            self.get_logger().error(
                f'Link inatteso: ricevuto {returned_link}, '
                f'atteso {self.tool_frame}'
            )
            return

        if predicted.header.frame_id != self.target_pose.header.frame_id:
            self.get_logger().error(
                f'Frame inatteso: ricevuto {predicted.header.frame_id}, '
                f'atteso {self.target_pose.header.frame_id}'
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

        self.validity_future = self.validity_client.call_async(request)
        self.validity_future.add_done_callback(
            self.on_endpoint_validity_response
        )
#----------------------------------------------------#
    def on_endpoint_validity_response(self, future):
        # Se lo stato contiene una collisione o non soddisfa i vincoli inviati, 
        # il servizio può rispondere normalmente con valid = False
        try:
            response = future.result()
        except Exception as exc:
            self.get_logger().error(
                f'Errore nel recupero della risposta di validità: {exc}'
            )
            return 

        if response.valid:
            self.get_logger().info(
                "Lo stato finale supera la verifica di validità"
            )
        else:
            self.get_logger().info(
                "Lo stato finale non supera la verifica di validità"
            )

        results = response.constraint_result

        constraints_ok = (
            len(results) == 2
            and all(item.result for item in results)
        )

        self.endpoint_verified = (
            response.valid
            and constraints_ok
            and self.endpoint_position_ok
        )

        message = (
            f'Validità dello stato: {response.valid} | '
            f'Vincoli: {[item.result for item in results]} | '
            f'Numero di contatti: {len(response.contacts)} | '
            f'Verifica endpoint: {self.endpoint_verified}'
        )

        if self.endpoint_verified:
            self.get_logger().info(message)
            submitted = self.motion_execution.request_execution(self.planned_trajectory)
            if not submitted:
                self.get_logger().error(
                    "Non è stato avviato un nuovo invio della traiettoria"
                )
        else:
            self.get_logger().error(message)
#----------------------------------------------------#
    def on_execution_finished(self, succeeded):
        self.execution_succeeded = succeeded

        if not succeeded:
            self.get_logger().error(
                'Esecuzione non riuscita: verifica della posa non avviata'
            )
            return

        self.get_logger().info('Esecuzione conclusa con successo')

        started = self.pose_verifier.start(
            self.target_pose,
            self.target_constraints,
            self.tool_frame,
        )

        if not started:
            self.get_logger().error(
                'Non è stato possibile avviare la verifica della posa'
            )
#----------------------------------------------------#
    def on_pose_verification_finished(self, succeeded):
        self.pose_verified = succeeded

        if succeeded:
            self.get_logger().info(
                'Verifica della posa conclusa con successo'
            )
        else:
            self.get_logger().error(
                'Verifica della posa conclusa con esito negativo'
            )



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