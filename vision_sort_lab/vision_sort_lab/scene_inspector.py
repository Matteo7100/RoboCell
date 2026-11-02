import rclpy
from rclpy.node import Node
from moveit_msgs.msg import PlanningSceneComponents
from moveit_msgs.srv import GetPlanningScene

class SceneInspector(Node):
    def __init__(self):
        super().__init__('scene_inspector')

        self.scene_client = self.create_client(GetPlanningScene, '/get_planning_scene')

        while rclpy.ok() and not (self.scene_client.wait_for_service(timeout_sec=1.0)):
            self.get_logger().info(
                'In attesa del servizio di lettura della scena…'
            )
        
        if rclpy.ok():
                self.get_logger().info(
                    'Servizio di lettura della scena disponibile'    
                )
                self.request_scene()
#----------------------------------------------------#
    def request_scene(self):
        request = GetPlanningScene.Request()
        request.components.components = (
            PlanningSceneComponents.WORLD_OBJECT_NAMES
            | PlanningSceneComponents.WORLD_OBJECT_GEOMETRY
        )        
        self.get_logger().info(
            "Richiesta di lettura della scena inviata"
        )
        self.scene_future = self.scene_client.call_async(request)
        self.scene_future.add_done_callback(self.on_scene_response)
#----------------------------------------------------#
    def on_scene_response(self, future):
        try:
            response = future.result()
        except Exception as exc:
            self.get_logger().error(
                f"Errore nella lettura della scena: {exc}"
            )
            return

        objects = response.scene.world.collision_objects
        self.get_logger().info(
            f"Numero oggetti: {len(objects)}"
        )
        for obj in objects:
            self.get_logger().info(
                f"Oggetto: {obj.id}"
            )
            self.get_logger().info(
                f'{obj.id}: primitive={len(obj.primitives)}, mesh={len(obj.meshes)}'
            )
            for mesh in obj.meshes:
                self.get_logger().info(
                    f'Triangoli della mesh: {len(mesh.triangles)}'
                )
#----------------------------------------------------#

def main(args=None):
    scene = None
    rclpy.init(args=args)
    try: 
        scene = SceneInspector()   
        rclpy.spin(scene)
    except KeyboardInterrupt:
        pass
    finally:
        if scene is not None:
            scene.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()



