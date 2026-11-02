import math
import rclpy

from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class ToolPoseReader(Node):
    def __init__(self):
        super().__init__('tool_pose_reader')

        self.declare_parameter('tool_frame', 'panda_hand')
        self.tool_frame = self.get_parameter('tool_frame').value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.pose_timer = self.create_timer(1.0, self.read_pose)
# ------------------------------------------------------------#
    def read_pose(self):
        try:
            # lookup_transform: Get the transform from the source frame to the target frame.
            # Parameters: target_frame – Name of the frame to transform into.
            #             source_frame – Name of the input frame.
            #             time – The time at which to get the transform (0 will get the latest).
            #             timeout – Time to wait for the target frame to become available.
            transform = self.tf_buffer.lookup_transform(
                'panda_link0', self.tool_frame, Time()
            )
        except TransformException as exc:
            self.get_logger().info(
                f"TF non ancora disponibile: {exc}"
            )   
            return

        position = transform.transform.translation
        orientation = transform.transform.rotation
        stamp = transform.header.stamp

        quaternion_norm = math.sqrt(
            orientation.x ** 2
            + orientation.y ** 2
            + orientation.z ** 2
            + orientation.w ** 2
        )

        self.get_logger().info(
            f'{transform.header.frame_id} -> {transform.child_frame_id}: |'
            f'pos=({position.x:.4f}, {position.y:.4f}, {position.z:.4f}) m |'
            f'quaternion = {orientation.x}, {orientation.y}, {orientation.z}, {orientation.w} |'
            f'timestamp: {stamp.sec}.{stamp.nanosec:09d} |'
            f'norma della rotazione: {quaternion_norm:.6f}'
        )

# ------------------------------------------------------------#

def main(args=None):
    rclpy.init(args=args)
    reader = ToolPoseReader()
    try:
        rclpy.spin(reader)
    except KeyboardInterrupt:
        pass
    finally:
        reader.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
