"""Exercise the real verifier deadline without receiving states or moving a robot."""

import time

from geometry_msgs.msg import PoseStamped
from moveit_msgs.msg import Constraints
import rclpy
from rclpy.node import Node

from vision_sort_lab.pose_verifier import PoseVerifier


def run_probe():
    """Return the observed timeout after one False and three quiet seconds.

    The caller owns the rclpy context. Only this instance's subscription is
    destroyed; no publisher, controller, action or planning scene is modified.
    """
    node = Node('pose_verifier_timeout_probe')
    verifier = None
    results = []
    started_at = None

    def on_finished(succeeded):
        results.append((succeeded, time.monotonic() - started_at))

    try:
        verifier = PoseVerifier(node, on_finished)
        if not node.destroy_subscription(verifier.joint_subscription):
            raise RuntimeError('Impossibile isolare la subscription del test')
        verifier.joint_subscription = None

        target = PoseStamped()
        target.header.frame_id = 'panda_link0'
        target.pose.orientation.w = 1.0
        # No state can arrive, so these constraints are never sent to a service.
        started_at = time.monotonic()
        if not verifier.start(target, Constraints(), 'panda_hand'):
            raise RuntimeError('Avvio del verificatore rifiutato')

        # The independent watchdog makes a broken verifier fail rather than hang.
        watchdog = started_at + verifier.timeout_sec + 2.0
        while not results and time.monotonic() < watchdog:
            rclpy.spin_once(node, timeout_sec=0.05)
        if not results:
            raise AssertionError('Il timeout non ha notificato alcun risultato')

        quiet_until = time.monotonic() + 3.0
        while time.monotonic() < quiet_until:
            rclpy.spin_once(node, timeout_sec=0.05)

        if len(results) != 1 or results[0][0] is not False:
            raise AssertionError(f'Attesa una sola notifica False: {results}')
        elapsed = results[0][1]
        if elapsed < verifier.timeout_sec or elapsed > verifier.timeout_sec + 2.0:
            raise AssertionError(f'Scadenza fuori intervallo: {elapsed:.3f} s')
        if verifier.verification_pending or not verifier.verification_timer.is_canceled():
            raise AssertionError('Il verificatore non ha chiuso il timer')
        if verifier.sample_captured or verifier.fk_future is not None or verifier.validity_future is not None:
            raise AssertionError('Il test ha acquisito dati o richiesto servizi')

        node.get_logger().info(
            f'TIMEOUT PASS | notifiche=1 | risultato=False | '
            f'durata={elapsed:.3f} s | osservazione_successiva=3 s | '
            'FK=0 | validita=0 | movimenti=0'
        )
        return elapsed
    finally:
        if verifier is not None:
            verifier.destroy()
        node.destroy_node()


def main(args=None):
    """Run the isolated ROS test and exit nonzero on failure."""
    rclpy.init(args=args)
    try:
        run_probe()
    finally:
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
