
from moveit_msgs.srv import GetMotionPlan
import rclpy
from rclpy.node import Node
from moveit_msgs.msg import Constraints, JointConstraint
from moveit_msgs.msg import MoveItErrorCodes
from rclpy.action import ActionClient
from moveit_msgs.action import ExecuteTrajectory
from action_msgs.msg import GoalStatus
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import JointState
from vision_sort_lab.motion_builders import build_plan_request
from vision_sort_lab.motion_errors import describe_moveit_error
from action_msgs.srv import CancelGoal

class MotionCommander(Node):

    def __init__(self):
        super().__init__('motion_commander')

        self.joint_positions = {}
        self.last_joint_state_stamp = None
        self.joint_state_subscription = self.create_subscription(JointState, '/joint_states', self.on_joint_state, qos_profile_sensor_data)

        self.verification_pending = False
        self.verification_start_ns = None

        self.verification_timeout_sec = 2.0
        self.verification_timer = self.create_timer(0.1, self.check_verification_timeout)

        self.plan_client = self.create_client(GetMotionPlan, '/plan_kinematic_path')
        self.planned_trajectory = None  
        self.execute_client = ActionClient(
            self,
            ExecuteTrajectory,
            '/execute_trajectory'
        )

        self.cancel_future = None

        self.plan_retry_count = 0
        self.max_plan_retries = 1

        self.declare_parameter("target_joint1", 0.0)

        while rclpy.ok() and not (self.plan_client.wait_for_service(timeout_sec=1.0)):
            self.get_logger().info(
                'In attesa del servizio di pianificazione…'
            )
        
        if rclpy.ok():
                self.get_logger().info(
                    'Servizio di pianificazione disponibile'    
                )
                while rclpy.ok() and not (self.execute_client.wait_for_server(timeout_sec = 1.0)):
                    self.get_logger().info(
                        "In attesa dell'action di esecuzione..."
                    )
                if rclpy.ok():
                    self.get_logger().info(
                        'Action di esecuzione disponibile'
                    )
                    self.target_positions = {
                        "panda_joint1": self.get_parameter("target_joint1").value,
                        "panda_joint2": -0.785,
                        "panda_joint3": 0.0,
                        "panda_joint4": -2.356,
                        "panda_joint5": 0.0,
                        "panda_joint6": 1.571,
                        "panda_joint7": 0.785,
                    }
                    self.request_plan(self.target_positions)

        self.goal_tolerance = 0.01  # radianti
#----------------------------------------------------#
    def request_plan(self, target_positions):
        request = build_plan_request(target_positions)
        self.get_logger().info(
            "Richiesta di pianificazione inviata"
        )
        self.plan_future = self.plan_client.call_async(request)
        # registra una funzione da chiamare al completamento dell’operazione.
        # Nel nostro caso la funzione è il metodo on_plan_response.
        self.plan_future.add_done_callback(self.on_plan_response)
#----------------------------------------------------#
    def on_plan_response(self, future):
        try:
            response = future.result()
        except Exception as exc:
            self.get_logger().error(
                f"Errore nel recupero della risposta: {exc}"
            )
            return 
            
        result = response.motion_plan_response # accede alla parte della risposta che contiene l’esito della pianificazione

        if result.error_code.val == MoveItErrorCodes.SUCCESS:
            self.planned_trajectory = result.trajectory
            self.get_logger().info(
                f"Pianificazione riuscita in {result.planning_time:.3f} secondi"
            )
            num_points = len(result.trajectory.joint_trajectory.points) 
            self.get_logger().info(
                f"La traiettoria contiene {num_points} punti"
            ) 
            self.request_execution()  
        else:
            self.planned_trajectory = None
            error_code = result.error_code.val
            error_name = describe_moveit_error(error_code)
            self.get_logger().error(
                f"Pianificazione fallita: {error_name} {error_code}"
            )

            if error_code in (
                MoveItErrorCodes.PLANNING_FAILED,
                MoveItErrorCodes.TIMED_OUT,
                ) and self.plan_retry_count < self.max_plan_retries:
                self.plan_retry_count += 1
                self.get_logger().warning(f"Nuovo tentativo di pianificazione {self.plan_retry_count}/{self.max_plan_retries}")
                self.request_plan(self.target_positions)
#----------------------------------------------------#
    def build_execution_goal(self):  
        if self.planned_trajectory is None:
            self.get_logger().error(
                "Error in trajectory planning"
            )
            return None
        # metodo per riconoscere una lista vuota: if not .......
        if not self.planned_trajectory.joint_trajectory.points:            
            self.get_logger().error(
                "Error in trajectory planning points"
            )
            return None

        goal = ExecuteTrajectory.Goal()
        goal.trajectory = self.planned_trajectory

        return goal
#----------------------------------------------------#
    def request_execution(self):
        goal = self.build_execution_goal()
        if goal is None:
            return
        self.execute_goal_future = self.execute_client.send_goal_async(
            goal,
            feedback_callback = self.on_execution_feedback
        )
        self.execute_goal_future.add_done_callback(
            self.on_execution_goal_response
        )
        self.get_logger().info(
            "Goal di esecuzione inviato"
        )
#----------------------------------------------------#
    def on_execution_goal_response(self, future):
        # future rappresenta dei risultati che ancora devono essere ricevuti da operazioni asincrone. 
        # quando questa callback viene chiamata, il suo Future è già completato.
        try:
            goal_handle = future.result() 
        except Exception as exc:
            self.get_logger().error(
                f"Errore nella risposta al goal di esecuzione: {exc}"
            )
            return
        if not goal_handle.accepted:
            self.get_logger().error(
                "Goal di esecuzione rifiutato"
            )
            return
        self.execute_goal_handle = goal_handle
        self.get_logger().info(
            "Goal di esecuzione accettato"
        )
        self.execute_result_future = goal_handle.get_result_async()
        self.execute_result_future.add_done_callback(
            self.on_execution_result
        )       
#----------------------------------------------------#
    def on_execution_result(self, future):
        try:
            response = future.result() 
        except Exception as exc:
            self.get_logger().error(
                f"Errore nel recupero del risultato di esecuzione: {exc}"
            )
            return
        status = response.status
        error_code = response.result.error_code.val
        if (
            status == GoalStatus.STATUS_SUCCEEDED
            and error_code == MoveItErrorCodes.SUCCESS
        ):
            self.get_logger().info(
                "Esecuzione completata con successo"
            )            
            self.verification_start_ns = self.get_clock().now().nanoseconds
            self.verification_pending = True
        else:  
            error_name = describe_moveit_error(error_code)
            self.get_logger().error(
                f"Esecuzione non riuscita: status ROS={status}, codice MoveIt={error_name}({error_code})"
            )
#----------------------------------------------------#
    def on_execution_feedback(self, feedback_msg):
        state = feedback_msg.feedback.state
        self.get_logger().info(
            f"Stato esecuzione: {state}"
        )
#----------------------------------------------------#
    def on_joint_state(self, msg):
        if not msg.position:
            return
        if len(msg.name) != len(msg.position):
            self.get_logger().warning(
                'Nomi e posizioni hanno lunghezze diverse'
            )
            return

        self.joint_positions = dict(zip(msg.name, msg.position))
        self.last_joint_state_stamp = msg.header.stamp

        testo = str(self.joint_positions)
        self.get_logger().info(
            testo, throttle_duration_sec=1.0
        )
        # -----TEST-----
        # if self.verification_pending:  # SOLO TEST: sospende la verifica articolare
        #    return

        if self.verification_pending == False:
            return
        stamp_ns = msg.header.stamp.sec * 1_000_000_000 + msg.header.stamp.nanosec
        
        self.get_logger().info(
            f"{stamp_ns} - {self.verification_start_ns}", throttle_duration_sec=1.0
        )

        if stamp_ns <= self.verification_start_ns:
            return
        
        result = self.check_target_reached()

        if result is None:
            return

        if result is True:
            self.get_logger().info(
                "Configurazione raggiunta entro la tolleranza"
            )
        else:
            self.get_logger().error(
                "Configurazione fuori tolleranza"
            )

        self.verification_pending = False            
#----------------------------------------------------#
    def check_target_reached(self):
        check = True
        for name, objective in self.target_positions.items():
            if name not in self.joint_positions:
                self.get_logger().warning(
                    f"Target position of joint {name} not in Joint position"
                )
                return None
            error = abs(self.joint_positions[name] - objective)
            self.get_logger().info(
                f'{name}: errore = {error:.6f} rad'
            )
            if error > self.goal_tolerance:
                check = False
        return check
#----------------------------------------------------#
    def check_verification_timeout(self):
        if self.verification_pending == False:
            return
        if ((self.get_clock().now().nanoseconds - self.verification_start_ns)/1_000_000_000) >= self.verification_timeout_sec:
            self.get_logger().error(
                "time expired, verification not executed"
            )
            self.verification_pending = False
#----------------------------------------------------#
    def request_cancel(self):
        if self.execute_goal_handle is None:
            self.get_logger().error(
                "Impossibile richiedere la cancellazione: nessun goal di esecuzione disponibile"
            )
            return
        else:
            self.cancel_future = self.execute_goal_handle.cancel_goal_async()
            self.cancel_future.add_done_callback(self.on_cancel_response)
            self.get_logger().info(
                "Richiesta di cancellazione inviata"
            )
#----------------------------------------------------#
    def on_cancel_response(self, future):
        try: 
            response = future.result()
        except Exception as exc:
            self.get_logger().error(
                f"Errore nel recupero della risposta di cancellazione: {exc}"
            )
            return
        return_code = response.return_code
        num_goals = len(response.goals_canceling)

        if return_code == CancelGoal.Response.ERROR_NONE and num_goals > 0:            
            self.get_logger().info(
                "Richiesta di cancellazione accettata"
            )
        else:
            self.get_logger().error(
                f"Richiesta di cancellazione non accettata: codice={return_code}, "
                f"goal in cancellazione={num_goals}"
            )
#----------------------------------------------------#
   


#----------------------------------------------------#
def main(args=None):
    commander = None
    rclpy.init(args=args)
    try: 
        commander = MotionCommander()   
        rclpy.spin(commander)
    except KeyboardInterrupt:
        pass
    finally:
        if commander is not None:
            commander.destroy_node()
        rclpy.try_shutdown()
#----------------------------------------------------#

if __name__ == '__main__':
    main()