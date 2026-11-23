"""Campionamento della profondità e proiezione RGB-D."""

import cv2
import numpy as np

from vision_sort_lab.perception.config import (
    PATCH_RADIUS,
    MIN_DEPTH_SAMPLES,
    MAX_DEPTH_SPREAD,
)
from vision_sort_lab.tcp_geometry import rotate

def depth_at(u, v, depth, region_mask):
    column = round(u)
    row = round(v)

    if region_mask[row, column] == 0:
        raise ValueError(
            "Il baricentro cade fuori dalla parte interna della regione"
        )

    left = max(0, column - PATCH_RADIUS)
    right = min(depth.shape[1], column + PATCH_RADIUS + 1)
    top = max(0, row - PATCH_RADIUS)
    bottom = min(depth.shape[0], row + PATCH_RADIUS + 1)

    patch = depth[top:bottom, left:right]
    inside = region_mask[top:bottom, left:right] > 0

    valid = inside & np.isfinite(patch) & (patch > 0)
    samples = patch[valid]

    if samples.size < MIN_DEPTH_SAMPLES:
        raise ValueError(
            f"Campioni di profondità insufficienti: {samples.size}"
        )

    low, high = np.percentile(samples, [10, 90])
    spread = float(high - low)

    if spread > MAX_DEPTH_SPREAD:
        raise ValueError(
            f"Profondità disomogenea nella zona centrale: "
            f"{spread * 1000:.1f} mm"
        )

    return float(np.median(samples)), int(samples.size), spread


def pixel_to_world(
    u,
    v,
    depth_m,
    camera_info,
    camera_transform,
):
    intrinsic = np.asarray(
        camera_info.k, dtype=np.float64
    ).reshape(3, 3)
    distortion = np.asarray(
        camera_info.d, dtype=np.float64
    )
    pixel = np.array([[[u, v]]], dtype=np.float64)

    normalized = cv2.undistortPoints(
        pixel, intrinsic, distortion
    ).reshape(2)

    # La profondità Gazebo è la coordinata Z nel frame ottico.
    point_camera = (
        float(normalized[0]) * depth_m,
        float(normalized[1]) * depth_m,
        depth_m,
    )

    point_rotated = rotate(
        camera_transform.rotation, point_camera
    )
    origin = camera_transform.translation

    return (
        origin[0] + point_rotated[0],
        origin[1] + point_rotated[1],
        origin[2] + point_rotated[2],
    )