from collections.abc import Callable
from math import isfinite

from action_msgs.msg import GoalStatus
from control_msgs.action import GripperCommand
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.task import Future
from math import isfinite

class GripperCommander:
    def __init__(self, node: Node, result_callback):
        self._node = node
        self._result_callback = result_callback
        self._client = ActionClient(
            node,
            GripperCommand,
            '/panda_hand_controller/gripper_cmd',
        )
        self._goal_future = None
        self._goal_handle = None
        self._result_future = None
        self._uncertain = False
# ----------------------------------------------------- #        
    def request_position(self, position: float) -> bool:
        if not isfinite(position) or not 0.0 <= position <= 0.04:
            return False

        if self._goal_future is not None or self._result_future is not None:
            return False

        if self._uncertain or not self._client.server_is_ready():
            return False

        goal = GripperCommand.Goal()
        goal.command.position = float(position)
        goal.command.max_effort = 0.0

        try:
            future = self._client.send_goal_async(goal)
        except Exception as exc:
            self._uncertain = True
            self._node.get_logger().error(
                f"Invio del comando pinza fallito: {exc}"
            )
            return False

        self._goal_future = future
        future.add_done_callback(self._on_goal_response)
        return True        
# ----------------------------------------------------- #        
    def _on_goal_response(self, future: Future) -> None:
        if future is not self._goal_future:
            return

        try:
            goal_handle = future.result()
        except Exception as exc:
            self._finish(
                False,
                f"Errore nella risposta al comando pinza: {exc}",
                uncertain=True,
            )
            return

        if goal_handle is None:
            self._finish(False, "Risposta al comando pinza assente", uncertain=True)
            return

        if not goal_handle.accepted:
            self._finish(False, "Comando pinza rifiutato", uncertain=False)
            return

        self._goal_handle = goal_handle
        try:
            self._result_future = goal_handle.get_result_async()
        except Exception as exc:
            self._finish(
                False,
                f"Richiesta del risultato della pinza fallita: {exc}",
                uncertain=True,
            )
            return

        self._goal_future = None
        self._result_future.add_done_callback(self._on_result)
# ----------------------------------------------------- #        
    def _on_result(self, future: Future) -> None:
        if future is not self._result_future:
            return

        try:
            response = future.result()
        except Exception as exc:
            self._finish(
                False,
                f"Errore nel risultato della pinza: {exc}",
                uncertain=True,
            )
            return

        if response is None:
            self._finish(False, "Risultato della pinza assente", uncertain=True)
            return

        terminal_statuses = (
            GoalStatus.STATUS_SUCCEEDED,
            GoalStatus.STATUS_CANCELED,
            GoalStatus.STATUS_ABORTED,
        )
        if response.status not in terminal_statuses:
            self._finish(
                False,
                f"Stato della pinza non terminale: {response.status}",
                uncertain=True,
            )
            return

        result = response.result
        succeeded = (
            response.status == GoalStatus.STATUS_SUCCEEDED
            and result.reached_goal
        )
        reason = (
            f"Pinza: statusROS={response.status}, "
            f"position={result.position:.4f} m, "
            f"reached_goal={result.reached_goal}, stalled={result.stalled}"
        )
        self._finish(succeeded, reason, uncertain=False)
# ----------------------------------------------------- #            
    def _finish(self, succeeded: bool, reason: str, *, uncertain: bool) -> None:
        if self._goal_future is None and self._result_future is None:
            return

        self._uncertain = uncertain
        self._goal_future = None
        self._goal_handle = None
        self._result_future = None

        logger = self._node.get_logger()
        if succeeded:
            logger.info(reason)
        else:
            logger.error(reason)

        self._result_callback(succeeded, reason)
# ----------------------------------------------------- #            
    def destroy(self) -> None:
        self._goal_future = None
        self._goal_handle = None
        self._result_future = None
        self._client.destroy()