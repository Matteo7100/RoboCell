"""Rigid transforms for a tool point; metres and ROS quaternions (x, y, z, w).

T_A_B describes frame B in frame A. This module has no ROS dependencies and
does not choose a Panda TCP offset: the robot model supplies that definition.
"""

from dataclasses import dataclass
import math
import xml.etree.ElementTree as ET


def _finite_tuple(values, size):
    result = tuple(float(value) for value in values)
    if len(result) != size or not all(math.isfinite(value) for value in result):
        raise ValueError(f'Expected {size} finite values')
    return result


@dataclass(frozen=True)
class RigidTransform:
    """An immutable translation and normalized quaternion."""

    translation: tuple = (0.0, 0.0, 0.0)
    rotation: tuple = (0.0, 0.0, 0.0, 1.0)

    def __post_init__(self):
        object.__setattr__(self, 'translation', _finite_tuple(self.translation, 3))
        quaternion = _finite_tuple(self.rotation, 4)
        norm = math.hypot(*quaternion)
        if norm < 1e-12 or not math.isfinite(norm):
            raise ValueError('Quaternion norm must be finite and nonzero')
        object.__setattr__(self, 'rotation', tuple(value / norm for value in quaternion))


def rotate(rotation, vector):
    """Apply a normalized quaternion to a three dimensional vector."""
    x, y, z, w = rotation
    vx, vy, vz = vector
    tx = 2.0 * (y * vz - z * vy)
    ty = 2.0 * (z * vx - x * vz)
    tz = 2.0 * (x * vy - y * vx)
    return (
        vx + w * tx + y * tz - z * ty,
        vy + w * ty + z * tx - x * tz,
        vz + w * tz + x * ty - y * tx,
    )


def compose(a_b, b_c):
    """Return T_A_C = T_A_B * T_B_C, including the rotated offset."""
    offset = rotate(a_b.rotation, b_c.translation)
    ax, ay, az, aw = a_b.rotation
    bx, by, bz, bw = b_c.rotation
    return RigidTransform(
        tuple(a + b for a, b in zip(a_b.translation, offset)),
        (
            aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
            aw * bw - ax * bx - ay * by - az * bz,
        ),
    )


def inverse(a_b):
    """Return T_B_A, the inverse of T_A_B."""
    x, y, z, w = a_b.rotation
    rotation = (-x, -y, -z, w)
    return RigidTransform(
        rotate(rotation, tuple(-value for value in a_b.translation)), rotation
    )


def hand_to_tcp(base_hand, hand_tcp):
    """Calculate the TCP pose from a hand pose and the fixed tool definition."""
    return compose(base_hand, hand_tcp)


def tcp_to_hand(base_tcp, hand_tcp):
    """Convert a desired TCP pose into the real hand link's goal pose."""
    return compose(base_tcp, inverse(hand_tcp))


def from_rpy(xyz, rpy):
    """Read URDF fixed-axis roll, pitch, yaw: Rz(yaw) Ry(pitch) Rx(roll)."""
    roll, pitch, yaw = _finite_tuple(rpy, 3)
    sr, sp, sy = (math.sin(value / 2.0) for value in (roll, pitch, yaw))
    cr, cp, cy = (math.cos(value / 2.0) for value in (roll, pitch, yaw))
    return RigidTransform(xyz, (
        sr * cp * cy - cr * sp * sy,
        cr * sp * cy + sr * cp * sy,
        cr * cp * sy - sr * sp * cy,
        cr * cp * cy + sr * sp * sy,
    ))


def fixed_transform(urdf_xml, parent_link, child_link):
    """Read an existing fixed descendant from URDF; reject movable chains.

    This deliberately does not manufacture a TCP if the requested link does
    not exist, nor use a moving finger origin as a fixed hand reference.
    """
    robot = ET.fromstring(urdf_xml)
    links = {link.attrib['name'] for link in robot.findall('link')}
    if parent_link not in links or child_link not in links:
        raise ValueError('Requested reference link is absent from the URDF')
    by_child = {}
    for joint in robot.findall('joint'):
        child = joint.find('child').attrib['link']
        if child in by_child:
            raise ValueError(f'Multiple parents for {child}')
        by_child[child] = joint
    visited = set()
    current = child_link
    result = RigidTransform()
    while current != parent_link:
        if current in visited or current not in by_child:
            raise ValueError('Requested link is not a fixed descendant')
        visited.add(current)
        joint = by_child[current]
        if joint.attrib['type'] != 'fixed':
            raise ValueError(f'Movable joint in TCP chain: {joint.attrib["name"]}')
        origin = joint.find('origin')
        xyz = '0 0 0' if origin is None else origin.get('xyz', '0 0 0')
        rpy = '0 0 0' if origin is None else origin.get('rpy', '0 0 0')
        result = compose(from_rpy(xyz.split(), rpy.split()), result)
        current = joint.find('parent').attrib['link']
    return result
