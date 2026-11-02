"""Real rclpy timer test, requiring ROS but neither MoveIt nor a robot."""

import pytest

rclpy = pytest.importorskip('rclpy')
from vision_sort_lab.timeout_probe import run_probe


def test_real_timeout_and_single_notification():
    """Observe the actual steady timer and a three second quiet interval."""
    rclpy.init()
    try:
        assert 2.0 <= run_probe() <= 4.0
    finally:
        rclpy.try_shutdown()
