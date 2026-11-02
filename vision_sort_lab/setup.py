from setuptools import find_packages, setup

package_name = 'vision_sort_lab'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/vision_sort_lab/meshes', ['meshes/open_bin.stl']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='matteo',
    maintainer_email='matteo@todo.todo',
    description='Guided robotic vision sorting and recovery project',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
		'joint_monitor = vision_sort_lab.joint_monitor:main',
        'motion_commander = vision_sort_lab.motion_commander:main',
        'scene_inspector = vision_sort_lab.scene_inspector:main',
        'scene_loader = vision_sort_lab.scene_loader:main',
        'tool_pose_reader = vision_sort_lab.tool_pose_reader:main',
        'pose_planner = vision_sort_lab.pose_planner:main',
        'timeout_probe = vision_sort_lab.timeout_probe:main',
        'robot_reference = vision_sort_lab.robot_reference:main',
       ],
    },
)

