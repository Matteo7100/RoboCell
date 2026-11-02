"""Nominal Panda tool reference, kept separate from the existing robot links.

The point is 45 mm beyond the finger joint origins: 58.4 + 45 = 103.4 mm
from panda_hand. Axes match panda_hand: Y closes/opens, +Z points to the tips.
This is a nominal geometric convention, not a contact or grasp calibration.
"""

from copy import deepcopy
import hashlib
import math
import xml.etree.ElementTree as ET

from vision_sort_lab.tcp_geometry import RigidTransform, from_rpy, hand_to_tcp, tcp_to_hand


HAND_FRAME = 'panda_hand'
TCP_FRAME = 'vision_sort_tcp'
HAND_TCP = RigidTransform((0.0, 0.0, 0.1034))
FINGER_MESH_GIT_SHA = '3b87289fea8128bcec3e0b4d174b169124e8e444'


def pose_transform(stamped_pose):
    """Read a PoseStamped-compatible value without modifying its fields."""
    p = stamped_pose.pose.position
    q = stamped_pose.pose.orientation
    if not stamped_pose.header.frame_id:
        raise ValueError('A reference frame is required')
    return RigidTransform((p.x, p.y, p.z), (q.x, q.y, q.z, q.w))


def _with_transform(stamped_pose, transform):
    result = deepcopy(stamped_pose)
    p = result.pose.position
    q = result.pose.orientation
    p.x, p.y, p.z = transform.translation
    q.x, q.y, q.z, q.w = transform.rotation
    return result


def tcp_target_to_hand(target_tcp):
    """Return the panda_hand goal for a desired TCP pose in the same base frame."""
    return _with_transform(target_tcp, tcp_to_hand(pose_transform(target_tcp), HAND_TCP))


def hand_pose_to_tcp(actual_hand):
    """Return the nominal TCP pose from a measured/FK panda_hand pose."""
    return _with_transform(actual_hand, hand_to_tcp(pose_transform(actual_hand), HAND_TCP))


def check_finger_mesh(data):
    """Require the collision mesh whose pad region was reviewed for this TCP."""
    digest = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
    if digest != FINGER_MESH_GIT_SHA:
        raise ValueError(f'Finger mesh differs from the reviewed model: {digest}')
    return digest


def validate_panda_hand(urdf_xml):
    """Guard the finger geometry assumptions and return the collision mesh URIs.

    Callers must also check both actual mesh contents with check_finger_mesh.
    The virtual TCP is calculated by this package, not requested as a MoveIt
    link and not assumed to exist in the input URDF.
    """
    robot = ET.fromstring(urdf_xml)
    links = {item.attrib['name']: item for item in robot.findall('link')}
    joints = {item.attrib['name']: item for item in robot.findall('joint')}
    if TCP_FRAME in links:
        raise ValueError('Virtual TCP name already exists in the robot model')
    meshes = []
    for index, link_name, sign in (
        (1, 'panda_leftfinger', 1.0), (2, 'panda_rightfinger', -1.0),
    ):
        try:
            joint = joints[f'panda_finger_joint{index}']
            link = links[link_name]
            if joint.attrib['type'] != 'prismatic':
                raise ValueError('Finger joint must be prismatic')
            if joint.find('parent').get('link') != HAND_FRAME or joint.find('child').get('link') != link_name:
                raise ValueError('Unexpected finger link relation')
            origin = joint.find('origin')
            transform = from_rpy(origin.get('xyz', '0 0 0').split(), origin.get('rpy', '0 0 0').split())
            if any(abs(a - b) > 1e-10 for a, b in zip(transform.translation, (0, 0, 0.0584))):
                raise ValueError('Unexpected finger joint origin')
            if abs(transform.rotation[3]) < 1 - 1e-10:
                raise ValueError('Unexpected finger joint rotation')
            axis = tuple(float(value) for value in joint.find('axis').get('xyz').split())
            if axis != (0, sign, 0):
                raise ValueError('Unexpected finger axis')
            limit = joint.find('limit')
            if float(limit.get('lower')) != 0.0 or float(limit.get('upper')) != 0.04:
                raise ValueError('Unexpected finger stroke')
            mimic = joint.find('mimic')
            if index == 1 and mimic is not None:
                raise ValueError('Unexpected master finger mimic')
            if index == 2 and (
                mimic is None or mimic.get('joint') != 'panda_finger_joint1'
                or float(mimic.get('multiplier', '1')) != 1
                or float(mimic.get('offset', '0')) != 0
            ):
                raise ValueError('Unexpected finger mimic relation')
            collisions = link.findall('collision')
            if len(collisions) != 1:
                raise ValueError('Expected one reviewed finger collision mesh')
            collision = collisions[0]
            origin = collision.find('origin')
            xyz = '0 0 0' if origin is None else origin.get('xyz', '0 0 0')
            rpy = '0 0 0' if origin is None else origin.get('rpy', '0 0 0')
            shape = from_rpy(xyz.split(), rpy.split())
            expected = from_rpy((0, 0, 0), (0, 0, 0 if index == 1 else math.pi))
            if any(abs(value) > 1e-10 for value in shape.translation):
                raise ValueError('Unexpected finger mesh displacement')
            dot = sum(a * b for a, b in zip(shape.rotation, expected.rotation))
            if abs(dot) < 1 - 1e-10:
                raise ValueError('Unexpected finger mesh rotation')
            mesh = collision.find('geometry/mesh')
            if tuple(float(value) for value in mesh.get('scale', '1 1 1').split()) != (1, 1, 1):
                raise ValueError('Unexpected finger mesh scale')
            meshes.append(mesh.attrib['filename'])
        except (KeyError, AttributeError, TypeError) as exc:
            raise ValueError('Incomplete Panda finger model') from exc
    return meshes
