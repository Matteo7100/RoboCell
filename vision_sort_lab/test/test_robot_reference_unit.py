"""Use synthetic models to exercise the offline description comparison."""

import unittest

from vision_sort_lab.robot_reference import find_parameter, inspect_models


URDF = '''<robot name="synthetic">
  <link name="panda_link0"/><link name="panda_link8"/>
  <link name="panda_hand"/><link name="test_tcp"/>
  <joint name="arm" type="revolute"><parent link="panda_link0"/>
    <child link="panda_link8"/><axis xyz="0 0 1"/>
    <limit lower="-1" upper="1" effort="1" velocity="1"/></joint>
  <joint name="hand" type="fixed"><parent link="panda_link8"/>
    <child link="panda_hand"/><origin rpy="0 0 -0.7853981633974483"/></joint>
  <joint name="tool" type="fixed"><parent link="panda_hand"/>
    <child link="test_tcp"/><origin xyz="0 0 0.1"/></joint>
</robot>'''
SRDF = '''<robot name="synthetic"><group name="panda_arm">
  <chain base_link="panda_link0" tip_link="panda_link8"/>
</group></robot>'''


def dump(**parameters):
    return {'/example_node': {'ros__parameters': parameters}}


class ReferenceTests(unittest.TestCase):
    """Fail on model disagreement and never silently invent a TCP."""

    def models(self):
        return (
            dump(robot_description=URDF, robot_description_semantic=SRDF),
            dump(robot_description=URDF),
        )

    def test_matching_models_leave_tcp_unselected(self):
        report = inspect_models(*self.models())
        self.assertTrue(report['kinematics_match'])
        self.assertIsNone(report['tcp_definition'])
        self.assertEqual(report['existing_tcp_candidates'], ['test_tcp'])

    def test_existing_fixed_tcp_can_be_read_explicitly(self):
        report = inspect_models(*self.models(), tcp_link='test_tcp')
        self.assertEqual(report['tcp_definition']['xyz_m'], (0, 0, 0.1))

    def test_nonexistent_tcp_is_rejected(self):
        with self.assertRaises(ValueError):
            inspect_models(*self.models(), tcp_link='panda_hand_tcp')

    def test_changed_joint_origin_is_rejected(self):
        move_group, publisher = self.models()
        publisher['/example_node']['ros__parameters']['robot_description'] = URDF.replace(
            'xyz="0 0 0.1"', 'xyz="0 0 0.2"'
        )
        with self.assertRaisesRegex(ValueError, 'different kinematics'):
            inspect_models(move_group, publisher)

    def test_changed_semantic_base_is_rejected(self):
        move_group, publisher = self.models()
        move_group['/example_node']['ros__parameters']['robot_description_semantic'] = SRDF.replace(
            'base_link="panda_link0"', 'base_link="other"'
        )
        with self.assertRaises(ValueError):
            inspect_models(move_group, publisher)

    def test_empty_and_ambiguous_dumps_are_rejected(self):
        for document in (
            None, {}, dump(robot_description=''),
            {'a': dump(robot_description='one'), 'b': dump(robot_description='two')},
        ):
            with self.subTest(document=document):
                with self.assertRaises(ValueError):
                    find_parameter(document, 'robot_description')


if __name__ == '__main__':
    unittest.main()
