"""Avvia sort_lab con una camera RGB-D fissa sopra work_table."""

import atexit
from math import pi
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET

from gz.math7 import Pose3d
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


SENSOR_TOPIC = "/sort_camera"
IMAGE = "/sort_camera/image_raw"
DEPTH = "/sort_camera/depth_image"
CAMERA_INFO = "/sort_camera/camera_info"
OPTICAL_FRAME = "sort_camera_optical_frame"
MOUNT_HEIGHT = 0.85


def sdf_pose(element):
    return Pose3d(
        *map(float, element.findtext("pose", "0 0 0 0 0 0").split())
    )


def start_camera_cell(context):
    package = Path(__file__).resolve().parent.parent

    source = (package / "worlds" / "sort_lab.sdf").read_text(
        encoding="utf-8"
    )
    # Il commento storico contiene "--", rifiutato dal parser XML.
    source = re.sub(r"<!--.*?-->", "", source, flags=re.DOTALL)
    tree = ET.ElementTree(ET.fromstring(source))

    world = tree.find("./world[@name='sort_lab']")
    if world is None:
        raise ValueError("Mondo sort_lab assente nel file SDF")

    table = world.find("model[@name='work_table']")
    top = world.find("model[@name='work_table']/link[@name='top']")
    if table is None or top is None:
        raise ValueError("Manca il supporto della camera work_table::top")

    world_optical = (
        sdf_pose(table)
        * sdf_pose(top)
        * Pose3d(0, 0, MOUNT_HEIGHT, pi, 0, 0)
    )
    position = world_optical.pos()
    rotation = world_optical.rot()

    sensors = ET.SubElement(
        world,
        "plugin",
        {
            "filename": "gz-sim-sensors-system",
            "name": "gz::sim::systems::Sensors",
        },
    )
    ET.SubElement(sensors, "render_engine").text = "ogre2"

    # L'asse +X del sensore Gazebo guarda verso il basso.
    # Nel frame ottico: destra=+X world, basso=-Y world, avanti=-Z world.
    top.append(ET.fromstring(f"""
      <sensor name="sort_rgbd" type="rgbd_camera">
        <pose>0 0 {MOUNT_HEIGHT} 0 {pi / 2} {pi / 2}</pose>
        <always_on>true</always_on>
        <update_rate>5</update_rate>
        <topic>{SENSOR_TOPIC}</topic>
        <camera name="sort_rgbd">
          <camera_info_topic>{CAMERA_INFO}</camera_info_topic>
          <horizontal_fov>1.2870022175865687</horizontal_fov>
          <image>
            <width>1280</width>
            <height>960</height>
            <format>R8G8B8</format>
          </image>
          <clip>
            <near>0.03</near>
            <far>3.0</far>
          </clip>
        </camera>
      </sensor>
    """))

    directory = TemporaryDirectory(prefix="robocell_sort_rgbd_")
    atexit.register(directory.cleanup)
    camera_world = Path(directory.name) / "sort_lab.sdf"
    tree.write(camera_world, encoding="utf-8", xml_declaration=True)

    bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(package / "launch" / "panda_gazebo_bringup.launch.py")
        ),
        launch_arguments={"world_file": str(camera_world)}.items(),
    )

    gazebo_image = f"{SENSOR_TOPIC}/image"
    camera_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="sort_camera_bridge",
        arguments=[
            f"{gazebo_image}@sensor_msgs/msg/Image[gz.msgs.Image",
            f"{DEPTH}@sensor_msgs/msg/Image[gz.msgs.Image",
            f"{CAMERA_INFO}@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo",
        ],
        remappings=[(gazebo_image, IMAGE)],
        parameters=[{
            "override_frame_id": OPTICAL_FRAME,
            "use_sim_time": True,
        }],
        output="screen",
    )

    optical_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="sort_camera_tf",
        arguments=[
            "--x", str(position.x()),
            "--y", str(position.y()),
            "--z", str(position.z()),
            "--qx", str(rotation.x()),
            "--qy", str(rotation.y()),
            "--qz", str(rotation.z()),
            "--qw", str(rotation.w()),
            "--frame-id", "world",
            "--child-frame-id", OPTICAL_FRAME,
        ],
        parameters=[{"use_sim_time": True}],
        output="screen",
    )

    return [bringup, camera_bridge, optical_tf]


def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function=start_camera_cell)
    ])