from action_msgs.msg import GoalStatus
from moveit_msgs.action import ExecuteTrajectory
from moveit_msgs.msg import MoveItErrorCodes
from rclpy.action import ActionClient

from vision_sort_lab.motion_errors import describe_moveit_error




class MotionExecution():
    def __init__(self, node, result_callback):
        self.node = node
        self.result_callback = result_callback
        self.execute_client = ActionClient(
            node,
            ExecuteTrajectory,
            '/execute_trajectory',
        )
        self.execute_goal_future = None
        self.execute_goal_handle = None
        self.execute_result_future = None
        self.execution_requested = False
        self.execution_uncertain = False
# ---------------------------------------------------------#
    def is_ready(self):
        return self.execute_client.server_is_ready()
# ---------------------------------------------------------#
    def build_execution_goal(self, trajectory):
        if trajectory is None:
            self.node.get_logger().error(
                "Nessuna traiettoria pianificata"
            )
            return None
        if len(trajectory.joint_trajectory.points) == 0:
            self.node.get_logger().error(
                "Traiettoria vuota"
            )
            return None

        goal = ExecuteTrajectory.Goal()
        goal.trajectory = trajectory

        return goal
# ---------------------------------------------------------#
    def _finish(self, succeeded: bool, *, can_rearm: bool) -> None:
        if not self.execution_requested:
            return
        self.execution_requested = False
        self.execution_uncertain = not can_rearm
        self.execute_goal_future = None
        self.execute_result_future = None
        if can_rearm:
            self.execute_goal_handle = None
        self.result_callback(succeeded)
# ---------------------------------------------------------#
    def on_execution_result(self, future):
        # riguarda il risultato del movimento
        if not self.execution_requested or future is not self.execute_result_future:
            return
        self.execute_result_future = None

        try:
            response = future.result()
        except Exception as exc:
            self.node.get_logger().error(
                f"Risultato dell'esecuzione fallito: {exc}"
            )
            self._finish(False, can_rearm=False)
            return
        if response is None:
            self.node.get_logger().error("Risultato dell'esecuzione assente")
            self._finish(False, can_rearm=False)
            return

        status = response.status
        if status not in (
            GoalStatus.STATUS_SUCCEEDED,
            GoalStatus.STATUS_CANCELED,
            GoalStatus.STATUS_ABORTED,
        ):
            self.node.get_logger().error(f"Stato dell'esecuzione non terminale: {status}")
            self._finish(False, can_rearm=False)
            return

        error_code = response.result.error_code.val
        error_name = describe_moveit_error(error_code)
        succeed = (status == GoalStatus.STATUS_SUCCEEDED) and (error_code == MoveItErrorCodes.SUCCESS)

        if succeed is True:
            self.node.get_logger().info(
                f"Esito dell'esecuzione positivo: statusROS = {status} | error = {error_name}({error_code})"
            )
        else:
             self.node.get_logger().error(
                f"Esito dell'esecuzione negativo: statusROS = {status} | error = {error_name}({error_code})"
            )
        self._finish(succeed, can_rearm=True)
# ---------------------------------------------------------#
    def on_execution_feedback(self, feedback_msg):
        state = feedback_msg.feedback.state
        self.node.get_logger().info(
            f"Stato dell'esecuzione: {state}"
        )
# ---------------------------------------------------------#
    def on_execution_goal_response(self, future):
        # riguarda l’accettazione della richiesta
        if not self.execution_requested or future is not self.execute_goal_future:
            return
        self.execute_goal_future = None

        try:
            goal_handle = future.result()
        except Exception as exc:
            self.node.get_logger().error(
                f"Goal response non trovata: {exc}"
            )
            self._finish(False, can_rearm=False)
            return
        if goal_handle is None:
            self.node.get_logger().error("Risposta del goal assente")
            self._finish(False, can_rearm=False)
            return
        if goal_handle.accepted is False:
            self.node.get_logger().error(
                f"Goal rifiutato"
            )
            self._finish(False, can_rearm=True)
            return
        else:
            self.execute_goal_handle = goal_handle
            self.node.get_logger().info(
                f"Goal accettato"
            )
        # il goal è stato accettato, hai conservato il suo handle in self.execute_goal_handle.
        # Ora devi chiedere a quell’handle il risultato dell’esecuzione
        try:
            self.execute_result_future = self.execute_goal_handle.get_result_async()

        except Exception as exc:
            self.node.get_logger().error(
                f"Risultato dell'esecuzione non trovato: {exc}"
            )
            self._finish(False, can_rearm=False)
            return
        # Quando questo Future si completa, chiama on_execution_result
        # e passaglielo. on_execution_result recupera e interpreta il risultato finale
        self.execute_result_future.add_done_callback(self.on_execution_result)
# ---------------------------------------------------------#
    def request_execution(self, trajectory) -> bool:
        if self.execution_uncertain:
            self.node.get_logger().error("Stato dell'ultima esecuzione incerto")
            return False
        if self.execution_requested is True:
            self.node.get_logger().warning(
                "Questa chiamata non ha avviato un nuovo invio"
            )
            return False

        goal = self.build_execution_goal(trajectory)

        if goal is None:
            return False

        if self.is_ready() is False:
            self.node.get_logger().warning(
                "Il server non è disponibile"
            )
            return False

        self.execution_requested = True
        try:
            self.execute_goal_future = self.execute_client.send_goal_async(
                goal,
                # Quando arriva un feedback di questo goal,
                # chiama il mio metodo on_execution_feedback
                feedback_callback=self.on_execution_feedback,
            )
        except Exception as exc:
            self.node.get_logger().error(
                f"Esecuzione non inviata: {exc}"
            )
            self.execution_requested = False
            self.execution_uncertain = True
            return False
        self.execute_goal_future.add_done_callback(self.on_execution_goal_response)
        self.node.get_logger().info(
            "Il goal è stato inviato"
        )
        return True
# ---------------------------------------------------------#
    def destroy(self):
        self.execute_client.destroy()

# ---------------------------------------------------------#
