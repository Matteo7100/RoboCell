"""ROS plumbing tests with synthetic FK/TF; no controller or physical robot."""

import math
from pathlib import Path
import time

import pytest

rclpy = pytest.importorskip('rclpy')
from geometry_msgs.msg import PoseStamped, TransformStamped
from moveit_msgs.srv import GetPositionFK
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster

from vision_sort_lab.tcp_probe import TCPProbe


MODEL = Path(__file__).resolve().parents[2] / 'docs/robot_reference/robot_state_publisher.urdf'


class SyntheticRobot(Node):
    """Publish one known hand pose and answer FK at the sampled state."""

    def __init__(self, *, invalid_frame=False):
        super().__init__('tcp_test_robot')
        self.invalid_frame = invalid_frame
        self.requests = []
        self.started_at = time.monotonic()
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.broadcaster = TransformBroadcaster(self)
        self.service = self.create_service(GetPositionFK, '/compute_fk', self.fk)
        self.timer = self.create_timer(0.02, self.publish_state)

    def publish_state(self):
        """Use exactly one timestamp for states and the matching hand TF."""
        stamp = self.get_clock().now().to_msg()
        state = JointState()
        state.header.stamp = stamp
        state.name = [f'panda_joint{i}' for i in range(1, 8)]
        state.position = [0.0] * 7
        self.publisher.publish(state)
        # Make the first candidate unavailable in TF to exercise recovery.
        if time.monotonic() - self.started_at < 0.2:
            return
        transform = TransformStamped()
        transform.header.stamp = stamp
        transform.header.frame_id = 'panda_link0'
        transform.child_frame_id = 'panda_hand'
        transform.transform.translation.x = 0.3
        transform.transform.translation.z = 0.6
        transform.transform.rotation.x = 1.0
        transform.transform.rotation.w = 0.0
        self.broadcaster.sendTransform(transform)

    def fk(self, request, response):
        """Return known hand and tip poses, independently of the probe helpers."""
        self.requests.append(request)
        response.error_code.val = 1
        response.fk_link_names = request.fk_link_names
        for link in request.fk_link_names:
            pose = PoseStamped()
            pose.header.frame_id = 'wrong_frame' if self.invalid_frame else 'panda_link0'
            pose.pose.position.x = 0.3
            pose.pose.position.z = 0.6
            pose.pose.orientation.w = 0.0
            if link == 'panda_hand':
                pose.pose.orientation.x = 1.0
            else:
                pose.pose.orientation.x = math.cos(math.pi / 8)
                pose.pose.orientation.y = -math.sin(math.pi / 8)
            response.pose_stamped.append(pose)
        return response


@pytest.mark.parametrize('invalid_frame', [False, True])
def test_fresh_sample_fk_tf_and_virtual_tcp(invalid_frame):
    """Check ROS callbacks and reject a response in the wrong reference frame."""
    rclpy.init()
    executor = SingleThreadedExecutor()
    robot = probe = None
    try:
        robot = SyntheticRobot(invalid_frame=invalid_frame)
        probe = TCPProbe(MODEL.read_text(encoding='utf-8'), show=True)
        executor.add_node(robot)
        executor.add_node(probe)
        watchdog = time.monotonic() + 10
        while not probe.finished and time.monotonic() < watchdog:
            executor.spin_once(timeout_sec=0.05)
        assert probe.finished
        assert probe.succeeded is not invalid_frame
        assert len(robot.requests) == 1
        stamp = probe.sample.header.stamp
        assert stamp.sec * 1_000_000_000 + stamp.nanosec > probe.start_ros_ns
        if not invalid_frame:
            assert probe.actual_tcp.pose.position.z == pytest.approx(0.4966)
            assert probe.static_broadcaster is not None
    finally:
        executor.shutdown()
        if probe is not None:
            probe.destroy_node()
        if robot is not None:
            robot.destroy_node()
        rclpy.try_shutdown()


def test_tcp_deadline_without_states():
    """A missing state causes a bounded failure even without FK/TF servers."""
    rclpy.init()
    probe = None
    try:
        probe = TCPProbe(MODEL.read_text(encoding='utf-8'), timeout_sec=0.2)
        watchdog = time.monotonic() + 2
        while not probe.finished and time.monotonic() < watchdog:
            rclpy.spin_once(probe, timeout_sec=0.02)
        assert probe.finished and not probe.succeeded
        assert probe.future is None
    finally:
        if probe is not None:
            probe.destroy_node()
        rclpy.try_shutdown()
