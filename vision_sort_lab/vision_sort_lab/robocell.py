from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from geometry_msgs.msg import PoseStamped
    from rclpy.node import Node


class RoboCell():
    def __init__(
        self,
        result_callback: Callable[[bool, str], None] | None = None,
    ) -> None:
        from .pose_planner import PosePlanner
        self._planner = PosePlanner(
            result_callback = result_callback,
            demo = False
        )
        self._closed = False
    
    # @property permette di accedere al nodo con cell.node, senza parentesi
    @property 
    def node(self) -> Node:
        return self._planner

    def request_pose(self, target: PoseStamped) -> bool:
        if self._closed:
            return False
        else:
            return self._planner.request_pose(target)

    def close(self) -> None:
        if self._closed:
            return

        self._closed = True
        self._planner.pose_verifier.destroy()
        self._planner.motion_execution.destroy()
        self._planner.destroy_node()        