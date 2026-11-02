"""Exercise the production verifier with fake clocks, services and messages."""

import importlib.util
import sys
from concurrent.futures import Future
from copy import deepcopy
import math
from pathlib import Path
from types import ModuleType, SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch


class FakeClock:
    def __init__(self, *, clock_type=None):
        self.clock_type = clock_type
        self.current_ns = 5_000_000_000

    def now(self):
        return NS(nanoseconds=self.current_ns)


class FKRequest:
    def __init__(self):
        self.header = NS(frame_id='')
        self.fk_link_names = []
        self.robot_state = NS(
            is_diff=False,
            joint_state=NS(header=NS(stamp=NS(sec=0, nanosec=0)), name=[], position=[]),
        )


class ValidityRequest:
    def __init__(self):
        self.robot_state = None
        self.group_name = None
        self.constraints = None


class FakeFK:
    Request = FKRequest


class FakeValidity:
    Request = ValidityRequest


class FakeClient:
    def __init__(self):
        self.ready = True
        self.requests = []
        self.futures = []
        self.send_error = None

    def service_is_ready(self):
        return self.ready

    def call_async(self, request):
        if self.send_error is not None:
            raise self.send_error
        future = Future()
        self.requests.append(request)
        self.futures.append(future)
        return future


class FakeTimer:
    def __init__(self, period, callback, clock):
        self.period = period
        self.callback = callback
        self.clock = clock
        self.cancelled = False

    def cancel(self):
        self.cancelled = True

    def reset(self):
        self.cancelled = False

    def fire(self):
        if not self.cancelled:
            self.callback()


class FakeNode:
    def __init__(self):
        self.logger = Mock()
        self.ros_clock = FakeClock()
        self.ros_clock.current_ns = 1_000_000_000
        self.fk_client = FakeClient()
        self.validity_client = FakeClient()
        self.subscription_arguments = None
        self.destroyed = []

    def get_logger(self):
        return self.logger

    def get_clock(self):
        return self.ros_clock

    def create_client(self, service_type, name):
        return self.fk_client if service_type is FakeFK else self.validity_client

    def create_subscription(self, *arguments):
        self.subscription_arguments = arguments
        return object()

    def create_timer(self, period, callback, *, clock):
        return FakeTimer(period, callback, clock)

    def destroy_subscription(self, subscription):
        self.destroyed.append(('subscription', subscription))

    def destroy_timer(self, timer):
        self.destroyed.append(('timer', timer))

    def destroy_client(self, client):
        self.destroyed.append(('client', client))


def load_verifier_with_ros_doubles():
    """Import the complete production module with scoped ROS substitutes."""
    modules = {}

    def module(name, **values):
        value = ModuleType(name)
        value.__dict__.update(values)
        modules[name] = value

    module('moveit_msgs')
    module('moveit_msgs.msg', MoveItErrorCodes=NS(SUCCESS=1))
    module('moveit_msgs.srv', GetPositionFK=FakeFK, GetStateValidity=FakeValidity)
    module('rclpy')
    module('rclpy.clock', Clock=FakeClock)
    module('rclpy.clock_type', ClockType=NS(STEADY_TIME='steady'))
    module('rclpy.qos', qos_profile_sensor_data=object())
    module('sensor_msgs')
    module('sensor_msgs.msg', JointState=object)
    module('vision_sort_lab.motion_errors', describe_moveit_error=lambda code: f'CODE_{code}')
    source_path = Path(__file__).resolve().parents[1] / 'vision_sort_lab' / 'pose_verifier.py'
    spec = importlib.util.spec_from_file_location('_verifier_under_test', source_path)
    loaded = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(loaded)
    return loaded.PoseVerifier


PoseVerifier = load_verifier_with_ros_doubles()


def target():
    return NS(
        header=NS(frame_id='panda_link0'),
        pose=NS(position=NS(x=0.0, y=0.0, z=0.0)),
    )


def constraints():
    return NS(position_constraints=['sphere'], orientation_constraints=['rotation_vector'])


def fk_response(x=0.004):
    value = target()
    value.pose.position.x = x
    value.pose.orientation = NS(x=0.0, y=0.0, z=0.0, w=1.0)
    return NS(error_code=NS(val=1), fk_link_names=['panda_hand'], pose_stamped=[value])


def validity_response(valid=True, results=(True, True)):
    return NS(valid=valid, constraint_result=[NS(result=value) for value in results], contacts=[])


class VerifierUnitTests(unittest.TestCase):
    def make(self, start=True):
        node = FakeNode()
        callback = Mock()
        verifier = PoseVerifier(node, callback)
        if start:
            self.assertTrue(verifier.start(target(), constraints(), 'panda_hand'))
        return node, callback, verifier

    def message(self, node, stamp_ns=None):
        node.ros_clock.current_ns += 1_000_000
        if stamp_ns is None:
            stamp_ns = node.ros_clock.current_ns - 1
        names = [f'panda_joint{i}' for i in range(7, 0, -1)]
        return NS(
            header=NS(stamp=NS(sec=stamp_ns // 1_000_000_000, nanosec=stamp_ns % 1_000_000_000)),
            name=names,
            position=[index / 10 for index in range(7)],
        )

    def test_start_records_two_different_clocks_and_copies_targets(self):
        node, callback, verifier = self.make(start=False)
        requested, requested_constraints = target(), constraints()
        self.assertTrue(verifier.start(requested, requested_constraints, 'panda_hand'))
        self.assertEqual(verifier.verification_start_ns, 1_000_000_000)
        self.assertEqual(verifier.start_steady_ns, 5_000_000_000)
        self.assertIsNot(verifier.target_pose, requested)
        self.assertIsNot(verifier.target_constraints, requested_constraints)
        requested.pose.position.x = 100.0
        self.assertEqual(verifier.target_pose.pose.position.x, 0.0)
        self.assertIs(verifier.verification_timer.clock, verifier.steady_clock)
        self.assertFalse(verifier.verification_timer.cancelled)
        callback.assert_not_called()

    def test_full_success_from_fresh_message_to_callback(self):
        node, callback, verifier = self.make()
        msg = self.message(node)
        original = dict(zip(msg.name, msg.position))
        verifier.on_joint_state(msg)
        self.assertEqual(len(node.fk_client.requests), 1)
        request = node.fk_client.requests[0]
        self.assertEqual(request.robot_state.joint_state.name, verifier.expected_joint_names)
        self.assertEqual(request.robot_state.joint_state.position, [original[name] for name in verifier.expected_joint_names])
        self.assertIsInstance(verifier.sample_stamp_ns, int)
        self.assertGreater(verifier.sample_stamp_ns, verifier.verification_start_ns)
        self.assertIsNot(verifier.sampled_state, request.robot_state)
        self.assertEqual(request.robot_state.joint_state.header.stamp, msg.header.stamp)
        node.fk_client.futures[0].set_result(fk_response())
        self.assertEqual(len(node.validity_client.requests), 1)
        self.assertEqual(node.validity_client.requests[0].robot_state, verifier.sampled_state)
        node.validity_client.futures[0].set_result(validity_response())
        callback.assert_called_once_with(True)
        self.assertFalse(verifier.verification_pending)
        self.assertTrue(verifier.verification_timer.cancelled)

    def test_timeout_at_exact_boundary_without_ros_clock_progress(self):
        node, callback, verifier = self.make()
        ros_before = node.ros_clock.current_ns
        verifier.steady_clock.current_ns += 2_000_000_000
        self.assertTrue(verifier.check_timeout())
        callback.assert_called_once_with(False)
        self.assertEqual(node.ros_clock.current_ns, ros_before)
        self.assertFalse(verifier.check_timeout())
        self.assertTrue(verifier.verification_timer.cancelled)

    def test_expired_on_joint_callback_stops_before_capture(self):
        node, callback, verifier = self.make()
        msg = self.message(node)
        verifier.steady_clock.current_ns += 2_000_000_000
        verifier.on_joint_state(msg)
        callback.assert_called_once_with(False)
        self.assertFalse(verifier.sample_captured)
        self.assertEqual(node.fk_client.requests, [])

    def test_old_equal_and_future_stamps_are_ignored(self):
        for stamp in (999_999_999, 1_000_000_000, 10_000_000_000):
            with self.subTest(stamp=stamp):
                node, callback, verifier = self.make()
                verifier.on_joint_state(self.message(node, stamp))
                self.assertEqual(node.fk_client.requests, [])
                self.assertTrue(verifier.verification_pending)
                callback.assert_not_called()

    def test_invalid_joint_messages_do_not_capture(self):
        for case in ('missing', 'duplicate', 'length', 'nan', 'infinite'):
            with self.subTest(case=case):
                node, callback, verifier = self.make()
                msg = self.message(node)
                if case == 'missing':
                    msg.name[-1] = 'other_joint'
                elif case == 'duplicate':
                    msg.name[-1] = msg.name[0]
                elif case == 'length':
                    msg.position.pop()
                elif case == 'nan':
                    msg.position[0] = float('nan')
                else:
                    msg.position[0] = float('inf')
                verifier.on_joint_state(msg)
                self.assertFalse(verifier.sample_captured)
                self.assertEqual(node.fk_client.requests, [])
                callback.assert_not_called()

    def test_service_readiness_uses_service_client_api(self):
        for client_name in ('fk_client', 'validity_client'):
            with self.subTest(client=client_name):
                node, callback, verifier = self.make()
                getattr(node, client_name).ready = False
                verifier.on_joint_state(self.message(node))
                self.assertFalse(verifier.sample_captured)
                self.assertEqual(node.fk_client.requests, [])
                self.assertTrue(verifier.verification_pending)

    def test_second_message_does_not_start_second_fk_chain(self):
        node, callback, verifier = self.make()
        verifier.on_joint_state(self.message(node))
        stamp = verifier.sample_stamp_ns
        verifier.on_joint_state(self.message(node))
        self.assertEqual(len(node.fk_client.requests), 1)
        self.assertEqual(verifier.sample_stamp_ns, stamp)

    def test_fk_send_exception_notifies_once_and_closes_timer(self):
        node, callback, verifier = self.make()
        node.fk_client.send_error = RuntimeError('send failed')
        verifier.on_joint_state(self.message(node))
        callback.assert_called_once_with(False)
        self.assertFalse(verifier.verification_pending)
        self.assertTrue(verifier.verification_timer.cancelled)

    def test_timeout_during_fk_ignores_late_response(self):
        node, callback, verifier = self.make()
        verifier.on_joint_state(self.message(node))
        verifier.steady_clock.current_ns += 2_000_000_000
        verifier.verification_timer.fire()
        node.fk_client.futures[0].set_result(fk_response())
        callback.assert_called_once_with(False)
        self.assertEqual(node.validity_client.requests, [])

    def test_timeout_during_validity_ignores_late_response(self):
        node, callback, verifier = self.make()
        verifier.on_joint_state(self.message(node))
        node.fk_client.futures[0].set_result(fk_response())
        verifier.steady_clock.current_ns += 2_000_000_000
        verifier.verification_timer.fire()
        node.validity_client.futures[0].set_result(validity_response())
        callback.assert_called_once_with(False)

    def test_negative_position_and_orientation_results(self):
        for x, results in ((0.006, (True, True)), (0.004, (True, False))):
            with self.subTest(x=x, results=results):
                node, callback, verifier = self.make()
                verifier.on_joint_state(self.message(node))
                node.fk_client.futures[0].set_result(fk_response(x=x))
                node.validity_client.futures[0].set_result(validity_response(results=results))
                callback.assert_called_once_with(False)

    def test_finish_uses_result_parameter_and_not_a_node_attribute(self):
        for succeeded in (False, True):
            with self.subTest(succeeded=succeeded):
                node, callback, verifier = self.make()
                node.logger.reset_mock()
                verifier._finish(succeeded, 'terminal')
                callback.assert_called_once_with(succeeded)
                if succeeded:
                    node.logger.info.assert_called_once_with('terminal')
                    node.logger.error.assert_not_called()
                else:
                    node.logger.error.assert_called_once_with('terminal')
                    node.logger.info.assert_not_called()
                verifier._finish(not succeeded, 'duplicate')
                self.assertEqual(callback.call_count, 1)

    def test_invalid_start_and_second_start(self):
        node, callback, verifier = self.make(start=False)
        self.assertFalse(verifier.start(target(), constraints(), ''))
        self.assertFalse(verifier.verification_pending)
        self.assertTrue(verifier.verification_timer.cancelled)
        self.assertTrue(verifier.start(target(), constraints(), 'panda_hand'))
        self.assertFalse(verifier.start(target(), constraints(), 'panda_hand'))

    def test_destroy_releases_entities_without_terminal_callback(self):
        node, callback, verifier = self.make()
        verifier.destroy()
        self.assertFalse(verifier.verification_pending)
        self.assertTrue(verifier.verification_timer.cancelled)
        self.assertEqual(len(node.destroyed), 4)
        callback.assert_not_called()

    def test_quiet_interval_and_repeated_finish_do_not_notify_again(self):
        node, callback, verifier = self.make()
        verifier.steady_clock.current_ns += 2_000_000_000
        verifier.verification_timer.fire()
        for unused in range(30):
            verifier.steady_clock.current_ns += 100_000_000
            verifier.verification_timer.fire()
            verifier.check_timeout()
            verifier._finish(True, 'late success')
        callback.assert_called_once_with(False)
        self.assertEqual(node.fk_client.requests, [])
        self.assertEqual(node.validity_client.requests, [])

    def test_service_response_at_deadline_cannot_succeed(self):
        node, callback, verifier = self.make()
        verifier.on_joint_state(self.message(node))
        node.fk_client.futures[0].set_result(fk_response())
        verifier.steady_clock.current_ns += 2_000_000_000
        node.validity_client.futures[0].set_result(validity_response())
        callback.assert_called_once_with(False)

    def test_unrelated_future_is_ignored(self):
        node, callback, verifier = self.make()
        verifier.on_joint_state(self.message(node))
        unrelated = Future()
        unrelated.set_result(fk_response())
        verifier.on_fk_response(unrelated)
        self.assertEqual(node.validity_client.requests, [])
        callback.assert_not_called()

    def test_destroy_after_subscription_was_isolated(self):
        node, callback, verifier = self.make()
        verifier.joint_subscription = None
        verifier.destroy()
        self.assertEqual([kind for kind, entity in node.destroyed], ['timer', 'client', 'client'])
        callback.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)
