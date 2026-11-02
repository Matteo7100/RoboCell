"""Geometric checks with independent, known poses; no Panda offset assumed."""

import math
import unittest

from vision_sort_lab.tcp_geometry import (
    RigidTransform, compose, fixed_transform, from_rpy, hand_to_tcp,
    inverse, tcp_to_hand,
)


class GeometryTests(unittest.TestCase):
    """Verify directions, rotated offsets and quaternion conventions."""

    def assertTransformClose(self, actual, expected):
        for a, b in zip(actual.translation, expected.translation):
            self.assertAlmostEqual(a, b, places=12)
        dot = sum(a * b for a, b in zip(actual.rotation, expected.rotation))
        self.assertAlmostEqual(abs(dot), 1.0, places=12)

    def test_identity(self):
        value = RigidTransform((1, 2, 3), (1, 0, 0, 1))
        self.assertTransformClose(compose(value, RigidTransform()), value)
        self.assertTransformClose(compose(RigidTransform(), value), value)

    def test_downward_hand_requires_hand_above_tcp(self):
        # Synthetic 10 cm offset; this is not a calibrated Panda TCP.
        hand_tcp = RigidTransform((0, 0, 0.1))
        base_tcp = RigidTransform((0.45, -0.20, 0.02), (1, 0, 0, 0))
        self.assertTransformClose(
            tcp_to_hand(base_tcp, hand_tcp),
            RigidTransform((0.45, -0.20, 0.12), (1, 0, 0, 0)),
        )

    def test_offset_rotates_with_hand(self):
        hand = from_rpy((1, 2, 3), (0, math.pi / 2, 0))
        self.assertTransformClose(
            hand_to_tcp(hand, RigidTransform((0, 0, 0.1))),
            RigidTransform((1.1, 2, 3), hand.rotation),
        )

    def test_nontrivial_tcp_orientation_is_removed_from_hand_goal(self):
        hand_tcp = from_rpy((0.1, 0, 0), (0, 0, math.pi / 2))
        base_tcp = RigidTransform((1, 0, 0))
        self.assertTransformClose(
            tcp_to_hand(base_tcp, hand_tcp),
            from_rpy((1, 0.1, 0), (0, 0, -math.pi / 2)),
        )

    def test_round_trip_and_inverse_for_many_orientations(self):
        for angle in (-2, -0.3, 0, 0.8, 2.9):
            value = from_rpy((0.4, -0.2, 0.7), (angle, -0.2, 0.6))
            offset = from_rpy((0.01, -0.02, 0.1), (0.1, angle, -0.4))
            self.assertTransformClose(compose(value, inverse(value)), RigidTransform())
            self.assertTransformClose(tcp_to_hand(hand_to_tcp(value, offset), offset), value)

    def test_rpy_rotation_order(self):
        # Rx(90), then Rz(90) sends the local Z axis to world +X.
        value = from_rpy((0, 0, 0), (math.pi / 2, 0, math.pi / 2))
        result = hand_to_tcp(value, RigidTransform((0, 0, 1)))
        for a, b in zip(result.translation, (1, 0, 0)):
            self.assertAlmostEqual(a, b, places=12)

    def test_normalization_and_quaternion_sign(self):
        self.assertTransformClose(RigidTransform(rotation=(0, 0, 0, -2)), RigidTransform())

    def test_invalid_numeric_values_are_rejected(self):
        for xyz, quaternion in (
            ((0, 0), (0, 0, 0, 1)),
            ((0, 0, float('nan')), (0, 0, 0, 1)),
            ((0, 0, 0), (0, 0, 0, 0)),
            ((0, 0, 0), (0, float('inf'), 0, 1)),
            ((0, 0, 0), (0, 0, 1)),
        ):
            with self.subTest(xyz=xyz, quaternion=quaternion):
                with self.assertRaises(ValueError):
                    RigidTransform(xyz, quaternion)


class URDFTests(unittest.TestCase):
    """Read actual link relations and reject invented or moving references."""

    urdf = '''<robot name="synthetic">
      <link name="hand"/><link name="adapter"/><link name="tcp"/>
      <joint name="a" type="fixed"><parent link="hand"/><child link="adapter"/>
        <origin xyz="0 0 0.1" rpy="0 0 1.5707963267948966"/></joint>
      <joint name="b" type="fixed"><parent link="adapter"/><child link="tcp"/>
        <origin xyz="0.02 0 0"/></joint>
    </robot>'''

    def test_fixed_chain_rotates_child_offset(self):
        value = fixed_transform(self.urdf, 'hand', 'tcp')
        for a, b in zip(value.translation, (0, 0.02, 0.1)):
            self.assertAlmostEqual(a, b, places=12)

    def test_identity_link(self):
        self.assertEqual(fixed_transform(self.urdf, 'hand', 'hand'), RigidTransform())

    def test_absent_moving_and_reverse_links_are_rejected(self):
        for xml, parent, child in (
            (self.urdf, 'hand', 'imaginary_tcp'),
            (self.urdf, 'tcp', 'hand'),
            (self.urdf.replace('type="fixed"', 'type="prismatic"', 1), 'hand', 'tcp'),
        ):
            with self.subTest(parent=parent, child=child):
                with self.assertRaises(ValueError):
                    fixed_transform(xml, parent, child)


if __name__ == '__main__':
    unittest.main()
