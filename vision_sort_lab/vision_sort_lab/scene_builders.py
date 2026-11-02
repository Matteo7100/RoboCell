from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive
from geometry_msgs.msg import Pose
from moveit_msgs.msg import ObjectColor
from vision_sort_lab.mesh_builders import load_stl_mesh


def build_table_object():
    table = CollisionObject()
    table.pose.orientation.w = 1.0
    table.id = "work_table"
    table.header.frame_id = "panda_link0"
    table.operation = CollisionObject.ADD
    
    box = SolidPrimitive()
    box.type = SolidPrimitive.BOX
    box.dimensions = [0.8, 0.8, 0.1]

    box_pose = Pose()
    box_pose.position.x = 0.6
    box_pose.position.y = 0.0
    box_pose.position.z = -0.05

    box_pose.orientation.w = 1.0

    table.primitives.append(box)
    table.primitive_poses.append(box_pose)

    return table
#----------------------------------------#

def build_box_object(object_id, dimensions, center):
    new_box = CollisionObject()
    new_box.pose.orientation.w = 1.0
    new_box.id = object_id
    new_box.header.frame_id = "panda_link0"
    new_box.operation = CollisionObject.ADD

    box = SolidPrimitive()
    box.type = SolidPrimitive.BOX

    box.dimensions = list(dimensions)

    box_pose = Pose()
    box_pose.position.x = center[0]
    box_pose.position.y = center[1]
    box_pose.position.z = center[2]

    box_pose.orientation.w = 1.0
    new_box.primitives.append(box)
    new_box.primitive_poses.append(box_pose)

    return new_box
#----------------------------------------#

def build_sorting_objects():
    objects = []

    objects.append(
        build_box_object(
            'piece_red_1',
            [0.04, 0.04, 0.04],
            (0.45, -0.20, 0.02),
        )
    )

    objects.append(
        build_box_object(
            'piece_blue_1',
            [0.04, 0.04, 0.04],
            (0.55, 0.0, 0.02),
        )
    )

    objects.append(
        build_box_object(
            'piece_red_2',
            [0.04, 0.04, 0.04],
            (0.45, 0.20, 0.02),
        )
    )

    return objects
#----------------------------------------#

def build_object_color(object_id, r, g, b):

    color = ObjectColor()
    color.id = object_id

    color.color.r = r
    color.color.a = 1.0
    color.color.g = g
    color.color.b = b

    return color
#----------------------------------------#

def build_bin_object(object_id, position, mesh_path):
    container = CollisionObject()
    container.id = object_id
    container.header.frame_id = "panda_link0"
    container.operation = CollisionObject.ADD
    container.pose.orientation.w = 1.0

    container.pose.position.x = position[0]
    container.pose.position.y = position[1]
    container.pose.position.z = position[2]

    container.meshes.append(load_stl_mesh(mesh_path))

    mesh_pose = Pose()
    mesh_pose.orientation.w = 1.0
    container.mesh_poses.append(mesh_pose)

    return container