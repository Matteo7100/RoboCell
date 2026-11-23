"""Misura punti 3D sulle regioni rosse usando RGB e profondità."""

from time import monotonic

import cv2
from cv_bridge import CvBridge
from message_filters import Subscriber, TimeSynchronizer
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.time import Time
from sensor_msgs.msg import CameraInfo, Image
from tf2_ros import Buffer, TransformListener

from vision_sort_lab.tcp_geometry import RigidTransform

from vision_sort_lab.perception.config import (
    IMAGE,
    DEPTH,
    CAMERA_INFO,
    WORLD,
)
from vision_sort_lab.perception.geometry import (
    face_geometry,
    solid_geometry,
)
from vision_sort_lab.perception.projection import (
    depth_at,
    pixel_to_world,
)
from vision_sort_lab.perception.planes import select_top_face
from vision_sort_lab.perception.support import support_plane


class RedImageProbe(Node):
    def __init__(self):
        super().__init__("red_image_probe")

        self.message = None
        self.depth_message = None
        self.camera_info = None

        self.subscription = Subscriber(
            self,
            Image,
            IMAGE,
            qos_profile=qos_profile_sensor_data,
        )
        self.depth_subscription = Subscriber(
            self,
            Image,
            DEPTH,
            qos_profile=qos_profile_sensor_data,
        )
        self.camera_info_subscription = Subscriber(
            self,
            CameraInfo,
            CAMERA_INFO,
            qos_profile=qos_profile_sensor_data,
        )

        self.synchronizer = TimeSynchronizer(
            [
                self.subscription,
                self.depth_subscription,
                self.camera_info_subscription,
            ],
            queue_size=10,
        )
        self.synchronizer.registerCallback(self.on_observation)

        self.tf_buffer = Buffer(node=self)
        self.tf_listener = TransformListener(self.tf_buffer, self)
#--------------------------------------------------------------#    
    def on_observation(self, message, depth_message, camera_info):
        self.message = message
        self.depth_message = depth_message
        self.camera_info = camera_info
#--------------------------------------------------------------#    
    def observation_ready(self):
        if self.message is None:
            return False

        return self.tf_buffer.can_transform(
            WORLD,
            self.message.header.frame_id,
            Time.from_msg(self.message.header.stamp),
        )
#--------------------------------------------------------------#    
    def pixel_to_world(self, u, v, depth_m, camera_transform):
        return pixel_to_world(
            u,
            v,
            depth_m,
            camera_info=self.camera_info,
            camera_transform=camera_transform,
        )
#--------------------------------------------------------------#    
    def select_top_face(self, depth, region_mask, camera_transform):
        return select_top_face(
            depth,
            region_mask,
            camera_info=self.camera_info,
            camera_transform=camera_transform,
        )
#--------------------------------------------------------------#   
    def face_geometry(
        self, depth, face_mask, normal, camera_transform
        ):
        return face_geometry(
            depth,
            face_mask,
            normal,
            camera_info=self.camera_info,
            camera_transform=camera_transform,
        )
#----------------------------------------------------------#
    def support_plane(
        self,
        depth,
        region_mask,
        objects_mask,
        face_center,
        face_normal,
        camera_transform,
        ):
        return support_plane(
            depth,
            region_mask,
            objects_mask,
            face_center,
            face_normal,
            camera_info=self.camera_info,
            camera_transform=camera_transform,
            logger=self.get_logger(),
        )
#----------------------------------------------------------#
    def analyze_image(self):
        message = self.message
        depth_message = self.depth_message
        info = self.camera_info

        for current in (message, depth_message):
            if current.header.frame_id != info.header.frame_id:
                raise ValueError(
                    "RGB, profondità e CameraInfo hanno frame diversi"
                )
            if (current.width, current.height) != (
                info.width, info.height
            ):
                raise ValueError(
                    "RGB, profondità e CameraInfo hanno dimensioni diverse"
                )

        if not np.all(np.isfinite(info.k)):
            raise ValueError("Intrinseci con valori non finiti")
        if info.k[0] <= 0 or info.k[4] <= 0:
            raise ValueError("Intrinseci della camera non validi")
        if info.distortion_model not in (
            "plumb_bob", "rational_polynomial"
        ):
            raise ValueError(
                f"Modello di distorsione inatteso: {info.distortion_model}"
            )
        if depth_message.encoding != "32FC1":
            raise ValueError(
                f"Profondità attesa 32FC1 in metri, "
                f"ricevuta {depth_message.encoding}"
            )

        transform = self.tf_buffer.lookup_transform(
            WORLD,
            message.header.frame_id,
            Time.from_msg(message.header.stamp),
        ).transform

        translation = transform.translation
        rotation = transform.rotation
        camera_transform = RigidTransform(
            (translation.x, translation.y, translation.z),
            (rotation.x, rotation.y, rotation.z, rotation.w),
        )

        bridge = CvBridge()
        image = bridge.imgmsg_to_cv2(
            message, desired_encoding="bgr8"
        )
        depth = bridge.imgmsg_to_cv2(
            depth_message, desired_encoding="passthrough"
        )

        stamp = message.header.stamp
        self.get_logger().info(
            f"Osservazione RGB-D {stamp.sec}.{stamp.nanosec:09d} | "
            f"frame={message.header.frame_id} | "
            f"dimensioni={message.width}x{message.height} | "
            f"depth={depth_message.encoding}"
        )

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        red_low = cv2.inRange(
            hsv, (0, 80, 40), (10, 255, 255)
        )
        red_high = cv2.inRange(
            hsv, (170, 80, 40), (179, 255, 255)
        )
        mask = cv2.bitwise_or(red_low, red_high)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        annotated = image.copy()
        top_faces_mask = np.zeros_like(mask)
        support_planes_mask = np.zeros_like(mask)
        kernel = np.ones((3, 3), dtype=np.uint8)
        candidates = 0
        valid_measurements = 0
        support_candidates = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 100:
                continue

            candidates += 1
            moments = cv2.moments(contour)
            u = moments["m10"] / moments["m00"]
            v = moments["m01"] / moments["m00"]
            _, _, width, height = cv2.boundingRect(contour)

            cv2.drawContours(
                annotated, [contour], -1, (0, 255, 0), 2
            )
            center = (round(u), round(v))
            cv2.circle(
                annotated, center, 4, (0, 255, 255), -1
            )
            cv2.putText(
                annotated,
                str(candidates),
                (center[0] + 8, center[1] - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
            )

            self.get_logger().info(
                f"Regione {candidates} | "
                f"centro=({u:.1f}, {v:.1f}) px | "
                f"ingombro={width}x{height} px | "
                f"area={area:.1f} px^2"
            )

            region_mask = np.zeros_like(mask)
            cv2.drawContours(
                region_mask, [contour], -1, 255, -1
            )
            region_mask = cv2.bitwise_and(region_mask, mask)

            try:
                face_mask, normal, rms = self.select_top_face(
                    depth, region_mask, camera_transform
                )

                face_moments = cv2.moments(
                    face_mask, binaryImage=True
                )
                face_u = (
                    face_moments["m10"] / face_moments["m00"]
                )
                face_v = (
                    face_moments["m01"] / face_moments["m00"]
                )

                face_interior = cv2.erode(face_mask, kernel)
                depth_m, samples, spread = depth_at(
                    face_u, face_v, depth, face_interior
                )
                x, y, z = self.pixel_to_world(
                    face_u, face_v, depth_m, camera_transform
                )

                (
                    geometric_center,
                    face_sides,
                    face_yaw,
                    face_yaw_period,
                ) = self.face_geometry(
                    depth,
                    face_mask,
                    normal,
                    camera_transform,
                )

            except (ValueError, np.linalg.LinAlgError) as exc:
                self.get_logger().warning(
                    f"Regione {candidates} | MISURA_INCERTA | "
                    f"faccia: {exc}"
                )
                continue

            valid_measurements += 1
            top_faces_mask = cv2.bitwise_or(
                top_faces_mask, face_mask
            )

            face_contours, _ = cv2.findContours(
                face_mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE,
            )
            cv2.drawContours(
                annotated, face_contours, -1, (255, 0, 255), 1
            )
            cv2.circle(
                annotated,
                (round(face_u), round(face_v)),
                4,
                (255, 255, 0),
                -1,
            )

            self.get_logger().info(
                f"Regione {candidates} | FACCIA_CANDIDATA | "
                f"centro=({face_u:.1f}, {face_v:.1f}) px | "
                f"pixel={int(np.count_nonzero(face_mask))} | "
                f"normale_world=("
                f"{normal[0]:.4f}, "
                f"{normal[1]:.4f}, "
                f"{normal[2]:.4f}) | "
                f"RMS piano={rms * 1000:.3f} mm"
            )
            self.get_logger().info(
                f"Regione {candidates} | PUNTO_SUPERFICIE | "
                f"{WORLD}=({x:.5f}, {y:.5f}, {z:.5f}) m | "
                f"profondità={depth_m:.5f} m | "
                f"campioni={samples} | "
                f"dispersione={spread * 1000:.2f} mm"
            )
            self.get_logger().info(
                f"Regione {candidates} | RETTANGOLO_FACCIA | "
                f"{WORLD}=("
                f"{geometric_center[0]:.5f}, "
                f"{geometric_center[1]:.5f}, "
                f"{geometric_center[2]:.5f}) m | "
                f"lati=("
                f"{face_sides[0] * 1000:.2f}, "
                f"{face_sides[1] * 1000:.2f}) mm | "
                f"yaw_mod{face_yaw_period}={face_yaw:.2f} deg"
            )

            try:
                (
                    support_mask,
                    support_origin,
                    support_normal,
                    support_rms,
                    separation,
                    sector_counts,
                ) = self.support_plane(
                    depth,
                    region_mask,
                    mask,
                    geometric_center,
                    normal,
                    camera_transform,
                )

            except (ValueError, np.linalg.LinAlgError) as exc:
                self.get_logger().warning(
                    f"Regione {candidates} | MISURA_INCERTA | "
                    f"appoggio: {exc}"
                )
                continue

            support_candidates += 1
            support_planes_mask = cv2.bitwise_or(
                support_planes_mask, support_mask
            )

            # Quota del piano alla XY del centro della faccia.
            support_z = support_origin[2] - (
                support_normal[0]
                * (geometric_center[0] - support_origin[0])
                + support_normal[1]
                * (geometric_center[1] - support_origin[1])
            ) / support_normal[2]

            self.get_logger().info(
                f"Regione {candidates} | PIANO_APPOGGIO_CANDIDATO | "
                f"z_sotto_centro={support_z:.5f} m | "
                f"normale_world=("
                f"{support_normal[0]:.4f}, "
                f"{support_normal[1]:.4f}, "
                f"{support_normal[2]:.4f}) | "
                f"RMS piano={support_rms * 1000:.3f} mm | "
                f"distanza_faccia={separation * 1000:.2f} mm | "
                f"settori={sector_counts.tolist()}"
            )
            try:
                (
                    piece_length,
                    piece_width,
                    piece_height,
                    volume_center,
                ) = solid_geometry(
                    geometric_center,
                    face_sides,
                    normal,
                    support_origin,
                    support_normal,
                )

            except ValueError as exc:
                self.get_logger().warning(
                    f"Regione {candidates} | MISURA_INCERTA | "
                    f"geometria: {exc}"
                )
                continue

            self.get_logger().info(
                f"Regione {candidates} | GEOMETRIA_PEZZO | "
                f"lunghezza={piece_length * 1000:.2f} mm | "
                f"larghezza={piece_width * 1000:.2f} mm | "
                f"altezza={piece_height * 1000:.2f} mm | "
                f"centro_world=("
                f"{volume_center[0]:.5f}, "
                f"{volume_center[1]:.5f}, "
                f"{volume_center[2]:.5f}) m"
            )

        self.get_logger().info(
            f"Regioni rosse: {candidates} | "
            f"facce 3D valide: {valid_measurements} | "
            f"piani d'appoggio candidati: {support_candidates}"
        )

        cv2.imshow("Regioni rosse", annotated)
        cv2.imshow("Maschera del rosso", mask)
        cv2.imshow("Facce candidate", top_faces_mask)
        cv2.imshow("Appoggi candidati", support_planes_mask)
        cv2.waitKey(0)


def main():
    rclpy.init()
    node = RedImageProbe()

    try:
        deadline = monotonic() + 10.0

        while rclpy.ok() and not node.observation_ready():
            if monotonic() >= deadline:
                raise TimeoutError(
                    "RGB, profondità, CameraInfo sincronizzati "
                    "o TF indisponibili dopo 10 secondi"
                )

            rclpy.spin_once(node, timeout_sec=0.1)

        if rclpy.ok():
            node.analyze_image()

    except KeyboardInterrupt:
        pass

    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()