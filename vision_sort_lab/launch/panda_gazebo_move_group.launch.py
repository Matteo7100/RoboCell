from pathlib import Path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def launch_move_group(context):
    urdf_value = LaunchConfiguration("urdf_file").perform(context)
    urdf_path = Path(urdf_value).expanduser().resolve()

    if not urdf_path.is_file():
        raise RuntimeError(f"Il percorso URDF non indica un file: {urdf_path}")

    config = MoveItConfigsBuilder(
        "panda",
        package_name="moveit_resources_panda_moveit_config",
    )
    config.robot_description(file_path=str(urdf_path))
    config.robot_description_semantic(file_path="config/panda.srdf")
    config.planning_pipelines(
        pipelines=["ompl"],
        default_planning_pipeline="ompl",
    )
    config.trajectory_execution(
        file_path="config/moveit_controllers.yaml",
        moveit_manage_controllers=False,
    )
    config.planning_scene_monitor(
        publish_robot_description=False,
        publish_robot_description_semantic=True,
    )
    config.to_moveit_configs()


    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            config.to_dict(),
            {"use_sim_time": True, "allow_trajectory_execution": True},
        ],
    )

    return [move_group_node]
# ----------------------------------------------------- #
def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("urdf_file"),
        OpaqueFunction(function=launch_move_group),
    ])
# ----------------------------------------------------- #
