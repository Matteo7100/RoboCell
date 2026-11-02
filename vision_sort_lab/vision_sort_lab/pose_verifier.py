# Dopo l’esecuzione, la pinza si trova entro la posa che avevamo richiesto?

from copy import deepcopy
import math

from moveit_msgs.msg import MoveItErrorCodes
from moveit_msgs.srv import GetPositionFK, GetStateValidity
from rclpy.clock import Clock
from rclpy.clock_type import ClockType
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import JointState

from vision_sort_lab.motion_errors import describe_moveit_error



class PoseVerifier():
    def __init__(self, node, result_callback):
        self.node = node
        self.result_callback = result_callback
        self.target_pose = None
        self.target_constraints = None
        self.tool_frame = None
        self.sampled_state = None
        self.sample_stamp_ns = None
        self.fk_future = None
        self.validity_future = None	
        self.verification_start_ns = None
        self.start_steady_ns = None	
        self.verification_started = False
        self.verification_pending = False	
        self.sample_captured = False
        self.position_ok = False
        self.timeout_sec = 2.0
        self.expected_joint_names = [f'panda_joint{i}' for i in range(1, 8)]

        self.fk_client = self.node.create_client(GetPositionFK, '/compute_fk')
        self.validity_client = self.node.create_client(GetStateValidity, '/check_state_validity')
        self.joint_subscription = self.node.create_subscription(JointState, '/joint_states', self.on_joint_state, qos_profile_sensor_data)

        self.steady_clock = Clock(clock_type=ClockType.STEADY_TIME)
        self.verification_timer = self.node.create_timer(0.1, self.check_timeout, clock = self.steady_clock)
        self.verification_timer.cancel()
# -----------------------------------------------------------#
    def _finish(self, succeeded, message):
        # se la verifica è già conclusa, entri nell’`if` ed esci subito;
        # se è ancora attiva, superi il controllo ed esegui le operazioni di conclusione.

        if not self.verification_pending:
            return

        self.verification_pending = False
        self.verification_timer.cancel()
        if succeeded is True:
            self.node.get_logger().info(
                message
            )
        else:
             self.node.get_logger().error(
                message
            )
        self.result_callback(succeeded)
# -----------------------------------------------------------#
    def check_timeout(self):
        if self.verification_pending is False:
            return False
        elapsed_ns = self.steady_clock.now().nanoseconds - self.start_steady_ns
        if elapsed_ns >= self.timeout_sec * 1_000_000_000:
            self._finish(False, 'Timeout scaduto')
            return True
        else:
            return False
# -----------------------------------------------------------#
    def start(self, target_pose, target_constraints, tool_frame):
        if self.verification_started is True:
            self.node.get_logger().info(
                "Verifica già in corso"
            )
            return False
        if target_pose is None:
            self.node.get_logger().error(
                "il messaggio della posa obiettivo non è stato fornito"
            )
            return False
        if target_constraints is None:
            self.node.get_logger().error(
                "i vincoli non sono stati forniti"
            )
            return False
        if not target_pose.header.frame_id:
            self.node.get_logger().error(
                "La posa non specifica il frame di riferimento: la stringa è vuota"
            )
            return False            
        if not tool_frame:
            self.node.get_logger().error(
                "Non è specificato il link da verificare: la stringa è vuota"
            )
            return False

        self.target_pose = deepcopy(target_pose)
        self.target_constraints = deepcopy(target_constraints)
        self.tool_frame = tool_frame

        self.verification_start_ns = self.node.get_clock().now().nanoseconds
        self.start_steady_ns = self.steady_clock.now().nanoseconds

        self.verification_pending = True
        self.verification_started = True
        self.verification_timer.reset()
        self.node.get_logger().info(
            "verifica avviata"
        )
        return True
# -----------------------------------------------------------#
    def on_joint_state(self, msg):
        if not self.verification_pending or self.sample_captured:
            return
        if self.check_timeout():
            return
        stamp_ns = msg.header.stamp.sec * 1_000_000_000 + msg.header.stamp.nanosec

        now_ros_ns = self.node.get_clock().now().nanoseconds

        if stamp_ns <= self.verification_start_ns or stamp_ns > now_ros_ns:
            return
        # Nomi e posizioni devono avere la stessa lunghezza.
        if len(msg.name) != len(msg.position):
            return

        # Ogni nome deve comparire una sola volta.
        if len(set(msg.name)) != len(msg.name):
            return

        # Devono essere presenti tutti i sette giunti del braccio.
        for joint_name in self.expected_joint_names:
            if joint_name not in msg.name:
                return

        positions_by_name = dict(zip(msg.name, msg.position))
        joint_names = list(self.expected_joint_names)
        joint_positions = [positions_by_name[name] for name in joint_names]
        if not all(math.isfinite(value) for value in joint_positions):            
            self.node.get_logger().error(
                "numero di joint infinito"
            )
            return
        if not self.fk_client.service_is_ready():
            return
        if not self.validity_client.service_is_ready():
            return
        
        request = GetPositionFK.Request()
        request.header.frame_id = self.target_pose.header.frame_id
        request.fk_link_names = [self.tool_frame]
        request.robot_state.is_diff = True
        request.robot_state.joint_state.name = joint_names
        request.robot_state.joint_state.position = joint_positions
        request.robot_state.joint_state.header.stamp = deepcopy(msg.header.stamp)
        self.sampled_state = deepcopy(request.robot_state)
        self.sample_stamp_ns = stamp_ns
        self.sample_captured = True

        self.node.get_logger().info(
            f'Campione aggiornato acquisito: stamp_ns={stamp_ns} | '
            f'riferimento_ns={self.verification_start_ns}'
        )

        if self.check_timeout():
            return

        try:
            self.fk_future = self.fk_client.call_async(request)
        except Exception as exc:
            self._finish(False, f'Errore nella richiesta FK: {exc}')
            return

        self.fk_future.add_done_callback(self.on_fk_response)
# -----------------------------------------------------------#
    def on_fk_response(self, future):
        if not self.verification_pending:
            return
        if future is not self.fk_future:
            return
        if self.check_timeout():
            return

        try:
            response = future.result()
        except Exception as exc:
            self._finish(False, f'Errore nella risposta FK: {exc}')
            return

        if response is None:
            self._finish(False, 'Risposta FK vuota')
            return

        error_code = response.error_code.val
        if error_code != MoveItErrorCodes.SUCCESS:
            error_name = describe_moveit_error(error_code)
            self._finish(
                False,
                f'FK della posa raggiunta fallita: {error_name} ({error_code})',
            )
            return

        if len(response.fk_link_names) != 1 or len(response.pose_stamped) != 1:
            self._finish(False, 'Risposta FK con dimensioni inattese')
            return

        returned_link = response.fk_link_names[0]
        actual_pose = response.pose_stamped[0]

        if returned_link != self.tool_frame:
            self._finish(
                False,
                f'Link FK inatteso: {returned_link}, atteso {self.tool_frame}',
            )
            return

        if self.target_pose is None or self.target_constraints is None:
            self._finish(False, 'Target o vincoli della verifica mancanti')
            return

        if actual_pose.header.frame_id != self.target_pose.header.frame_id:
            self._finish(
                False,
                f'Frame FK inatteso: {actual_pose.header.frame_id}, '
                f'atteso {self.target_pose.header.frame_id}',
            )
            return

        if (
            self.sampled_state is None
            or self.sample_stamp_ns is None
            or self.verification_start_ns is None
            or self.sample_stamp_ns <= self.verification_start_ns
        ):
            self._finish(False, 'Campione articolare assente o non aggiornato')
            return

        position = actual_pose.pose.position
        orientation = actual_pose.pose.orientation
        values = (
            position.x, position.y, position.z,
            orientation.x, orientation.y, orientation.z, orientation.w,
        )
        if not all(math.isfinite(value) for value in values):
            self._finish(False, 'La posa FK contiene valori non finiti')
            return

        target_position = self.target_pose.pose.position
        dx = position.x - target_position.x
        dy = position.y - target_position.y
        dz = position.z - target_position.z
        position_error = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        self.position_ok = position_error <= 0.005

        self.node.get_logger().info(
            f'Posa raggiunta da FK in {actual_pose.header.frame_id}: '
            f'pos=({position.x:.4f}, {position.y:.4f}, {position.z:.4f}) m | '
            f'q=({orientation.x:.6f}, {orientation.y:.6f}, '
            f'{orientation.z:.6f}, {orientation.w:.6f})'
        )
        self.node.get_logger().info(
            f'Campione verificato: stamp_ns={self.sample_stamp_ns} | '
            f'dx={dx * 1000:.3f}, dy={dy * 1000:.3f}, '
            f'dz={dz * 1000:.3f} mm | '
            f'distanza={position_error * 1000:.3f} mm | '
            f'entro 5 mm={self.position_ok}'
        )

        request = GetStateValidity.Request()
        request.robot_state = deepcopy(self.sampled_state)
        request.group_name = ''
        request.constraints = deepcopy(self.target_constraints)

        if self.check_timeout():
            return

        try:
            self.validity_future = self.validity_client.call_async(request)
        except Exception as exc:
            self._finish(False, f'Errore nella richiesta di validità: {exc}')
            return

        self.validity_future.add_done_callback(self.on_validity_response)
# -----------------------------------------------------------#
    def on_validity_response(self, future):
        if not self.verification_pending:
            return
        if future is not self.validity_future:
            return
        if self.check_timeout():
            return

        try:
            response = future.result()
        except Exception as exc:
            self._finish(False, f'Errore nella risposta di validità: {exc}')
            return

        if response is None:
            self._finish(False, 'Risposta di validità vuota')
            return

        results = [item.result for item in response.constraint_result]
        constraints_ok = len(results) == 2 and all(results)
        succeeded = response.valid and constraints_ok and self.position_ok

        self.node.get_logger().info(
            f'Validità posa raggiunta: {response.valid} | '
            f'Vincoli: {results} | '
            f'Numero di contatti: {len(response.contacts)} | '
            f'Posizione entro 5 mm: {self.position_ok}'
        )

        if self.check_timeout():
            return

        if succeeded:
            message = 'Posa raggiunta verificata sui dati aggiornati'
        else:
            message = (
                'La posa raggiunta non supera la verifica: '
                f'valid={response.valid}, vincoli={results}, '
                f'posizione_ok={self.position_ok}'
            )

        self._finish(succeeded, message)
# -----------------------------------------------------------#
    def destroy(self):
        self.verification_pending = False
        self.verification_timer.cancel()
        if self.joint_subscription is not None:
            self.node.destroy_subscription(self.joint_subscription)
            self.joint_subscription = None
        self.node.destroy_timer(self.verification_timer)
        self.node.destroy_client(self.fk_client)
        self.node.destroy_client(self.validity_client)

