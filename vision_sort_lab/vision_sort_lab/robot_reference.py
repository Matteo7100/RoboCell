"""Inspect the robot descriptions exported by the running Panda demo.

This is an offline report: it cannot send a trajectory or alter a ROS model.
"""

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from vision_sort_lab.tcp_geometry import fixed_transform, _finite_tuple


def find_parameter(document, name):
    """Find one unambiguous string parameter inside a ros2 param dump."""
    found = []

    def visit(value):
        if not isinstance(value, dict):
            return
        parameters = value.get('ros__parameters', {})
        if isinstance(parameters, dict) and name in parameters:
            found.append(parameters[name])
        for key, child in value.items():
            if key != 'ros__parameters':
                visit(child)

    visit(document)
    if not found or any(not isinstance(value, str) or not value.strip() for value in found):
        raise ValueError(f'Missing or invalid parameter: {name}')
    if len(set(found)) != 1:
        raise ValueError(f'Ambiguous parameter: {name}')
    return found[0]


def kinematic_signature(urdf_xml):
    """Compare link names and joint kinematics independently of XML formatting."""
    robot = ET.fromstring(urdf_xml)
    if robot.tag != 'robot':
        raise ValueError('Expected a robot URDF')
    links = tuple(sorted(link.attrib['name'] for link in robot.findall('link')))
    joints = []
    for joint in robot.findall('joint'):
        origin = joint.find('origin')
        xyz = '0 0 0' if origin is None else origin.get('xyz', '0 0 0')
        rpy = '0 0 0' if origin is None else origin.get('rpy', '0 0 0')
        axis = joint.find('axis')
        axis_xyz = '1 0 0' if axis is None else axis.get('xyz', '1 0 0')
        limit = joint.find('limit')
        mimic = joint.find('mimic')
        joints.append((
            joint.attrib['name'], joint.attrib['type'],
            joint.find('parent').attrib['link'], joint.find('child').attrib['link'],
            _finite_tuple(xyz.split(), 3), _finite_tuple(rpy.split(), 3),
            _finite_tuple(axis_xyz.split(), 3),
            None if limit is None else tuple(sorted(limit.attrib.items())),
            None if mimic is None else tuple(sorted(mimic.attrib.items())),
        ))
    return links, tuple(sorted(joints))


def inspect_models(move_group_dump, state_publisher_dump, tcp_link=None):
    """Check shared kinematics and report existing hand/finger/TCP references.

    A named TCP is accepted only if already present as a fixed hand descendant.
    Otherwise the report exposes geometry references for an explicit definition;
    it does not infer a pad centre from a finger joint origin.
    """
    moveit_urdf = find_parameter(move_group_dump, 'robot_description')
    tf_urdf = find_parameter(state_publisher_dump, 'robot_description')
    if kinematic_signature(moveit_urdf) != kinematic_signature(tf_urdf):
        raise ValueError('MoveIt and robot_state_publisher have different kinematics')
    semantic = ET.fromstring(find_parameter(move_group_dump, 'robot_description_semantic'))
    group = semantic.find("group[@name='panda_arm']")
    chains = [] if group is None else [chain.attrib for chain in group.findall('chain')]
    if len(chains) != 1 or chains[0].get('base_link') != 'panda_link0':
        raise ValueError('Expected one panda_arm chain rooted at panda_link0')
    tip = chains[0]['tip_link']
    tip_hand = fixed_transform(moveit_urdf, tip, 'panda_hand')
    robot = ET.fromstring(moveit_urdf)
    candidates = []
    fingers = []
    for link in robot.findall('link'):
        name = link.attrib['name']
        if any(word in name.lower() for word in ('tcp', 'grasp')):
            candidates.append(name)
        if 'finger' in name:
            fingers.append(ET.tostring(link, encoding='unicode'))
    finger_joints = [
        ET.tostring(joint, encoding='unicode') for joint in robot.findall('joint')
        if 'finger' in joint.attrib['name']
    ]
    result = {
        'kinematics_match': True,
        'base_link': 'panda_link0',
        'planning_group': 'panda_arm',
        'chain_tip': tip,
        'controlled_link': 'panda_hand',
        'tip_to_hand': {'xyz_m': tip_hand.translation, 'quaternion_xyzw': tip_hand.rotation},
        'existing_tcp_candidates': sorted(candidates),
        'finger_links_xml': fingers,
        'finger_joints_xml': finger_joints,
        'tcp_definition': None,
        'status': 'TCP not selected; geometry still needs review',
    }
    if tcp_link:
        hand_tcp = fixed_transform(moveit_urdf, 'panda_hand', tcp_link)
        result['tcp_definition'] = {
            'link': tcp_link, 'xyz_m': hand_tcp.translation,
            'quaternion_xyzw': hand_tcp.rotation, 'source': 'existing URDF fixed chain',
        }
        result['status'] = 'Existing fixed TCP read; pad geometry still needs review'
    return result


def main():
    """Print an offline JSON report from two actual parameter dumps."""
    import yaml

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--move-group', required=True, type=Path)
    parser.add_argument('--state-publisher', required=True, type=Path)
    parser.add_argument('--tcp-link', help='An existing fixed URDF link, if already verified')
    args = parser.parse_args()
    try:
        move_group = yaml.safe_load(args.move_group.read_text(encoding='utf-8'))
        state_publisher = yaml.safe_load(args.state_publisher.read_text(encoding='utf-8'))
        report = inspect_models(move_group, state_publisher, args.tcp_link)
    except (OSError, ValueError, KeyError, AttributeError, ET.ParseError, yaml.YAMLError) as exc:
        parser.exit(1, f'Robot reference failed: {exc}\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
