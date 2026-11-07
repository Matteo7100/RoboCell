from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

from pathlib import Path

import xacro
from launch_ros.parameter_descriptions import ParameterValue

from ament_index_python.packages import get_package_share_directory
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit

def generate_launch_description()-> LaunchDescription:
    gazebo = ExecuteProcess(
        cmd=["gz", "sim", "-r", "-v", "3", "empty.sdf"],
        output="screen"
    )
    clock_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        output="screen",
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"]
    )
    package_dir = Path(__file__).resolve().parent.parent
    xacro_path = package_dir / "urdf" / "panda_gazebo.urdf.xacro"
    robot_doc = xacro.process_file(str(xacro_path))
    robot_xml = robot_doc.toxml()

    state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters = [{
            "robot_description": ParameterValue(robot_xml, value_type=str),
            "use_sim_time": True
        }],
    )
    spawn_panda = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-world", "empty", "-topic", "/robot_description", "-name", "panda"]
    )

    share_dir = get_package_share_directory("moveit_resources_panda_moveit_config")
    controllers_yaml = Path(share_dir) / "config" / "ros2_controllers.yaml"

    spawn_joint_states = Node(
        package = "controller_manager",
        executable = "spawner",
        output = "screen",
        arguments = ["joint_state_broadcaster", "-c", "/controller_manager", "--controller-manager-timeout", "15"]
    )
    spawn_arm = Node(
        package = "controller_manager",
        executable = "spawner",
        output = "screen",
        arguments = ["panda_arm_controller", "-c", "/controller_manager", "--controller-manager-timeout", "15", "--param-file", str(controllers_yaml)]
    )

    def start_arm_after_broadcaster(event, context) -> list[Node]:
            if context.is_shutdown or event.returncode != 0:
                return []
            else:
                return [spawn_arm]

    arm_after_broadcaster = RegisterEventHandler(
        OnProcessExit(target_action=spawn_joint_states, on_exit=start_arm_after_broadcaster)
    )

    return LaunchDescription([gazebo, clock_bridge, state_publisher, spawn_panda, arm_after_broadcaster, spawn_joint_states])
