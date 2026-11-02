import rclpy
from rclpy.node import Node
from moveit_msgs.srv import ApplyPlanningScene
from vision_sort_lab.scene_builders import build_table_object
from vision_sort_lab.scene_builders import build_sorting_objects
from vision_sort_lab.scene_builders import build_object_color
from vision_sort_lab.scene_builders import build_bin_object
from pathlib import Path
from ament_index_python.packages import get_package_share_directory

class SceneLoader(Node):
    def __init__(self):
        super().__init__('scene_loader')
        self.scene_client = self.create_client(ApplyPlanningScene,'/apply_planning_scene')

        while rclpy.ok() and not (self.scene_client.wait_for_service(timeout_sec=1.0)):
            self.get_logger().info(
                'In attesa del servizio di caricamento della scena…'
            )
        
        if rclpy.ok():
            self.get_logger().info(
                'Servizio di caricamento della scena disponibile'    
            )
            self.apply_scene()
#----------------------------------------#

    def apply_scene(self):

        mesh_path = (
            Path(get_package_share_directory('vision_sort_lab'))
            / 'meshes'
            / 'open_bin.stl'
        )      
        request = ApplyPlanningScene.Request()

        request.scene.is_diff = True
        request.scene.robot_state.is_diff = True

        request.scene.world.collision_objects.append(
            build_table_object()
        )
        request.scene.world.collision_objects.extend(
            build_sorting_objects()
        )
        request.scene.object_colors.append(
            build_object_color('piece_red_1', 1.0, 0.0, 0.0)
        )
        request.scene.object_colors.append(
            build_object_color('piece_red_2', 1.0, 0.0, 0.0)
        )
        request.scene.object_colors.append(
            build_object_color('piece_blue_1', 0.0, 0.0, 1.0)
        )

        request.scene.world.collision_objects.append(
            build_bin_object(
                'bin_red',
                (0.75, -0.22, 0.0),
                mesh_path,
            )
        )
        request.scene.object_colors.append(
            build_object_color('bin_red', 1.0, 0.0, 0.0)
        )
        request.scene.world.collision_objects.append(
            build_bin_object(
                'bin_blue',
                (0.75, 0.22, 0.0),
                mesh_path,
            )
        )
        request.scene.object_colors.append(
            build_object_color('bin_blue', 0.0, 0.0, 1.0)
        )

        self.scene_future = self.scene_client.call_async(request)
        
        self.get_logger().info(
            "Richiesta di caricamento della scena inviata"
        )
        self.scene_future.add_done_callback(self.on_apply_scene_response)
#----------------------------------------#

    def on_apply_scene_response(self, future):
        try:
            response = future.result()
        except Exception as exc:
            self.get_logger().error(
                f"Errore nel caricamento della scena: {exc}"
            )
            return

        if response.success:
            self.get_logger().info(
                "Aggiornamento applicato"
            )
        else:
            self.get_logger().error(
                "Aggiornamento non applicato"
            )
#----------------------------------------#



def main(args=None):
    scene = None
    rclpy.init(args=args)
    try: 
        scene = SceneLoader()   
        rclpy.spin(scene)
    except KeyboardInterrupt:
        pass
    finally:
        if scene is not None:
            scene.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
