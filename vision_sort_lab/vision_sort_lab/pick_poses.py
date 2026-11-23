from geometry_msgs.msg import PoseStamped
from copy import deepcopy

def build_pregrasp_tcp(
    cube_center: tuple[float, float, float],
    cube_side: float,
    clearance: float,
) -> PoseStamped:
    x, y, z = cube_center

    target = PoseStamped()
    target.header.frame_id = "panda_link0"
    target.pose.position.x = x
    target.pose.position.y = y
    target.pose.position.z = z + cube_side / 2 + clearance

    target.pose.orientation.x = 1.0
    target.pose.orientation.y = 0.0
    target.pose.orientation.z = 0.0
    target.pose.orientation.w = 0.0

    return target

def build_approach_tcp(current_tcp: PoseStamped, target_z: float) -> PoseStamped:
    target_tcp = deepcopy(current_tcp)
    target_tcp.pose.position.z = target_z
    return target_tcp