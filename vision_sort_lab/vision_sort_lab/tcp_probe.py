"""Check the nominal TCP against a fresh state, MoveIt FK and matching TF."""

import argparse
from copy import deepcopy
import math
from pathlib import Path
import time
from urllib.parse import unquote, urlparse

from geometry_msgs.msg import TransformStamped
from moveit_msgs.msg import MoveItErrorCodes
from moveit_msgs.srv import GetPositionFK
import rclpy
from rclpy.clock import Clock
from rclpy.clock_type import ClockType
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.time import Time
from sensor_msgs.msg import JointState
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from tf2_ros.transform_listener import TransformListener

from vision_sort_lab.panda_tcp import (
    HAND_FRAME, HAND_TCP, TCP_FRAME, check_finger_mesh, hand_pose_to_tcp,
    pose_transform, validate_panda_hand,
)
from vision_sort_lab.robot_reference import find_parameter
from vision_sort_lab.tcp_geometry import RigidTransform, compose, fixed_transform, inverse


def read_model(path):
    """Read either raw URDF or a robot_state_publisher parameter dump."""
    text = Path(path).read_text(encoding='utf-8')
    if text.lstrip().startswith('<'):
        return text
    import yaml
    return find_parameter(yaml.safe_load(text), 'robot_description')


def resolve_mesh(uri, model_path):
    """Resolve local/package mesh references without downloading anything."""
    parsed = urlparse(uri)
    if parsed.scheme == 'file':
        if parsed.netloc not in ('', 'localhost'):
            raise ValueError('A local mesh file is required')
        return Path(unquote(parsed.path))
    if parsed.scheme == 'package':
        from ament_index_python.packages import get_package_share_directory
        return Path(get_package_share_directory(parsed.netloc)) / unquote(parsed.path).lstrip('/')
    if parsed.scheme:
        raise ValueError(f'Unsupported mesh URI: {uri}')
    return Path(model_path).parent / uri


def transform_errors(actual, expected):
    """Return translation distance in metres and quaternion angle in radians."""
    distance = math.dist(actual.translation, expected.translation)
    dot = abs(sum(a * b for a, b in zip(actual.rotation, expected.rotation)))
    angle = 2 * math.acos(min(1.0, dot))
    return distance, angle


class TCPProbe(Node):
    """Read-only, one-sample checker; optionally publish a virtual fixed frame."""

    def __init__(self, urdf_xml, *, show=False, timeout_sec=8.0):
        expected_tip_hand = fixed_transform(urdf_xml, 'panda_link8', HAND_FRAME)
        super().__init__('tcp_reference_probe')
        self.show = show
        self.expected_tip_hand = expected_tip_hand
        self.finished = False
        self.succeeded = False
        self.sample = None
        self.latest_sample = None
        self.future = None
        self.tf_hand = None
        self.actual_tcp = None
        self.static_broadcaster = None
        self.names = [f'panda_joint{i}' for i in range(1, 8)]
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)
        self.client = self.create_client(GetPositionFK, '/compute_fk')
        self.subscription = self.create_subscription(
            JointState, '/joint_states', self.on_joint_state, qos_profile_sensor_data
        )
        self.steady_clock = Clock(clock_type=ClockType.STEADY_TIME)
        self.timer = self.create_timer(0.05, self.tick, clock=self.steady_clock)
        self.start_ros_ns = self.get_clock().now().nanoseconds
        self.deadline = time.monotonic() + timeout_sec

    def finish(self, succeeded, message):
        """Set exactly one terminal result and stop the deadline timer."""
        if self.finished:
            return
        self.finished = True
        self.succeeded = succeeded
        self.timer.cancel()
        if succeeded:
            self.get_logger().info(message)
        else:
            self.get_logger().error(message)

    def on_joint_state(self, msg):
        """Capture one complete finite arm state strictly newer than startup."""
        if self.finished or self.future is not None:
            return
        stamp = msg.header.stamp.sec * 1_000_000_000 + msg.header.stamp.nanosec
        if stamp <= self.start_ros_ns or stamp > self.get_clock().now().nanoseconds:
            return
        if len(msg.name) != len(msg.position) or len(set(msg.name)) != len(msg.name):
            return
        positions = dict(zip(msg.name, msg.position))
        if not all(name in positions and math.isfinite(positions[name]) for name in self.names):
            return
        self.latest_sample = deepcopy(msg)
        if self.sample is None:
            self.sample = deepcopy(msg)

    def tick(self):
        """Wait for matching TF and FK readiness within a steady deadline."""
        if self.finished:
            return
        if time.monotonic() >= self.deadline:
            self.finish(False, 'TCP FAIL: timeout in attesa di campione, TF o FK')
            return
        if self.sample is None or self.future is not None or not self.client.service_is_ready():
            return
        try:
            # Exact sample time: never compare FK with an unrelated latest TF.
            transform = self.buffer.lookup_transform(
                'panda_link0', HAND_FRAME, Time.from_msg(self.sample.header.stamp)
            )
        except TransformException:
            # During discovery TF may have missed the first joint sample.
            # Retain a later candidate and let its matching TF arrive.
            if self.latest_sample is not None:
                self.sample = deepcopy(self.latest_sample)
            return
        t = transform.transform.translation
        q = transform.transform.rotation
        try:
            self.tf_hand = RigidTransform((t.x, t.y, t.z), (q.x, q.y, q.z, q.w))
            request = GetPositionFK.Request()
            request.header.frame_id = 'panda_link0'
            request.fk_link_names = ['panda_link8', HAND_FRAME]
            request.robot_state.is_diff = True
            request.robot_state.joint_state.header = deepcopy(self.sample.header)
            request.robot_state.joint_state.name = self.names
            values = dict(zip(self.sample.name, self.sample.position))
            request.robot_state.joint_state.position = [values[name] for name in self.names]
            self.future = self.client.call_async(request)
            self.future.add_done_callback(self.on_fk)
        except Exception as exc:
            self.finish(False, f'TCP FAIL: richiesta FK non riuscita: {exc}')

    def on_fk(self, future):
        """Check hand/tip geometry, then compare hand FK and TF at one timestamp."""
        if self.finished or future is not self.future:
            return
        if time.monotonic() >= self.deadline:
            self.finish(False, 'TCP FAIL: risposta FK oltre il timeout')
            return
        try:
            response = future.result()
            if response.error_code.val != MoveItErrorCodes.SUCCESS:
                raise ValueError(f'FK error code {response.error_code.val}')
            if len(response.fk_link_names) != 2 or len(response.pose_stamped) != 2:
                raise ValueError('Unexpected FK dimensions')
            poses = dict(zip(response.fk_link_names, response.pose_stamped))
            if set(poses) != {'panda_link8', HAND_FRAME}:
                raise ValueError('Unexpected FK links')
            if any(pose.header.frame_id != 'panda_link0' for pose in poses.values()):
                raise ValueError('Unexpected FK reference frame')
            fk_hand = pose_transform(poses[HAND_FRAME])
            fk_tip = pose_transform(poses['panda_link8'])
            observed_tip_hand = compose(inverse(fk_tip), fk_hand)
            fixed_error = transform_errors(observed_tip_hand, self.expected_tip_hand)
            if fixed_error[0] > 1e-7 or fixed_error[1] > 1e-6:
                raise ValueError(f'MoveIt tip/hand geometry differs: {fixed_error}')
            distance, angle = transform_errors(fk_hand, self.tf_hand)
            if distance > 0.001 or angle > 0.001:
                raise ValueError(f'FK/TF disagreement: {distance} m, {angle} rad')
            self.actual_tcp = hand_pose_to_tcp(poses[HAND_FRAME])
            p = self.actual_tcp.pose.position
            if self.show:
                self.publish_frame()
            stamp = self.sample.header.stamp
            self.finish(True,
                f'TCP PASS | stamp={stamp.sec}.{stamp.nanosec:09d} | '
                f'FK-TF={distance * 1000:.6f} mm, {angle:.9f} rad | '
                f'TCP in panda_link0=({p.x:.6f}, {p.y:.6f}, {p.z:.6f}) m | '
                'hand->TCP=(0, 0, 0.1034) m | movimenti=0')
        except Exception as exc:
            self.finish(False, f'TCP FAIL: {exc}')

    def publish_frame(self):
        """Expose the virtual point for RViz without changing the robot model."""
        self.static_broadcaster = StaticTransformBroadcaster(self)
        frame = TransformStamped()
        frame.header.stamp = self.get_clock().now().to_msg()
        frame.header.frame_id = HAND_FRAME
        frame.child_frame_id = TCP_FRAME
        t = frame.transform.translation
        q = frame.transform.rotation
        t.x, t.y, t.z = HAND_TCP.translation
        q.x, q.y, q.z, q.w = HAND_TCP.rotation
        self.static_broadcaster.sendTransform(frame)


def main(args=None):
    """Validate geometry locally and run a read-only live check."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', required=True, type=Path)
    parser.add_argument('--show', action='store_true', help='Keep the virtual TCP visible until Ctrl+C')
    options, ros_args = parser.parse_known_args(args)
    try:
        xml = read_model(options.model)
        for uri in validate_panda_hand(xml):
            check_finger_mesh(resolve_mesh(uri, options.model).read_bytes())
    except Exception as exc:
        parser.exit(1, f'TCP model check failed: {exc}\n')
    rclpy.init(args=ros_args)
    node = None
    succeeded = False
    try:
        node = TCPProbe(xml, show=options.show)
        while rclpy.ok() and not node.finished:
            rclpy.spin_once(node, timeout_sec=0.05)
        succeeded = node.succeeded
        if succeeded and options.show:
            node.get_logger().info(f'Frame {TCP_FRAME} attivo; Ctrl+C per chiudere')
            rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.try_shutdown()
    if not succeeded:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
