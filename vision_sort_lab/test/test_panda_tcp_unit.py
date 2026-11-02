"""Check the chosen TCP against the received hand model and known target poses."""

from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace as NS
import unittest

from vision_sort_lab.panda_tcp import (
    HAND_TCP, check_finger_mesh, hand_pose_to_tcp, tcp_target_to_hand,
    validate_panda_hand,
)


MODEL = Path(__file__).resolve().parents[2] / 'docs/robot_reference/robot_state_publisher.urdf'


def pose():
    return NS(
        header=NS(frame_id='panda_link0', stamp=NS(sec=12, nanosec=34)),
        pose=NS(position=NS(x=0.45, y=-0.2, z=0.02),
                orientation=NS(x=1.0, y=0.0, z=0.0, w=0.0)),
    )


class PandaTCPTests(unittest.TestCase):
    """Exercise the actual uploaded XML and reject changed finger assumptions."""

    def test_received_model_matches_the_reviewed_hand_convention(self):
        meshes = validate_panda_hand(MODEL.read_text(encoding='utf-8'))
        self.assertEqual(len(meshes), 2)
        self.assertTrue(all(uri.endswith('/collision/finger.stl') for uri in meshes))
        self.assertEqual(HAND_TCP.translation, (0, 0, 0.1034))

    def test_downward_tcp_target_converts_to_hand_above_target(self):
        target = pose()
        saved = deepcopy(target)
        hand = tcp_target_to_hand(target)
        self.assertAlmostEqual(hand.pose.position.z, 0.1234)
        self.assertEqual(hand.header, target.header)
        self.assertIsNot(hand.header, target.header)
        self.assertEqual(target, saved)
        restored = hand_pose_to_tcp(hand)
        self.assertAlmostEqual(restored.pose.position.z, 0.02)
        self.assertAlmostEqual(restored.pose.position.x, 0.45)
        self.assertAlmostEqual(restored.pose.position.y, -0.2)

    def test_missing_frame_or_zero_quaternion_is_rejected(self):
        target = pose()
        target.header.frame_id = ''
        with self.assertRaises(ValueError):
            tcp_target_to_hand(target)
        target = pose()
        target.pose.orientation.x = 0.0
        with self.assertRaises(ValueError):
            tcp_target_to_hand(target)

    def test_changed_model_requires_new_geometry_review(self):
        xml = MODEL.read_text(encoding='utf-8')
        cases = (
            xml.replace('0 0 0.0584', '0 0 0.06', 1),
            xml.replace('xyz="0 1 0"', 'xyz="1 0 0"', 1),
            xml.replace('<mimic joint="panda_finger_joint1"/>', ''),
            xml.replace('<robot name="panda">', '<robot name="panda"><link name="vision_sort_tcp"/>'),
        )
        for modified in cases:
            with self.subTest():
                self.assertNotEqual(modified, xml)
                with self.assertRaises(ValueError):
                    validate_panda_hand(modified)

    def test_unreviewed_mesh_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'differs'):
            check_finger_mesh(b'a different finger geometry')


if __name__ == '__main__':
    unittest.main()
