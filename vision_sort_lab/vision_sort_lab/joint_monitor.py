import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import JointState


class JointMonitor(Node):
    def __init__(self):
        super().__init__('joint_monitor')
        self.joint_positions = {}
        self.subscription = self.create_subscription(JointState, '/joint_states', self.joint_state_callback, qos_profile_sensor_data)

    def joint_state_callback(self, msg: JointState):
        if not msg.position:
            return

        if len(msg.name) != len(msg.position):
            self.get_logger().warning(
                'Nomi e posizioni hanno lunghezze diverse'
            )
            return

        self.joint_positions = dict(zip(msg.name, msg.position))

        if 'panda_joint3' in self.joint_positions:
            valore = self.joint_positions['panda_joint3']
            testo = f'panda_joint3 = {valore:.3f} rad'
            self.get_logger().info(testo, throttle_duration_sec=1.0)


def main(args=None):
    rclpy.init(args=args)
    monitor = JointMonitor()
    try:
        rclpy.spin(monitor)
    except KeyboardInterrupt:
        pass
    finally:
        monitor.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()

