"""Selezione e stima dei piani osservati nella profondità."""

import numpy as np

from vision_sort_lab.perception.config import (
    FACE_RANSAC_TRIALS,
    FACE_PLANE_TOLERANCE,
    MIN_FACE_POINTS,
    MIN_FACE_FRACTION,
    MAX_FACE_TILT_DEG,
)
from vision_sort_lab.perception.projection import pixel_to_world


def select_top_face(
    depth,
    region_mask,
    camera_info,
    camera_transform,
):
    valid = (
        (region_mask > 0)
        & np.isfinite(depth)
        & (depth > 0)
    )
    rows, columns = np.nonzero(valid)

    if rows.size < MIN_FACE_POINTS:
        raise ValueError(
            f"Punti 3D insufficienti nella regione: {rows.size}"
        )

    points = np.asarray(
        [
            pixel_to_world(
                float(column),
                float(row),
                float(depth[row, column]),
                camera_info=camera_info,
                camera_transform=camera_transform,
            )
            for row, column in zip(rows, columns)
        ],
        dtype=np.float64,
    )

    required_inliers = max(
        MIN_FACE_POINTS,
        int(np.ceil(MIN_FACE_FRACTION * len(points))),
    )
    minimum_normal_z = np.cos(
        np.deg2rad(MAX_FACE_TILT_DEG)
    )

    rng = np.random.default_rng(0)
    best_inliers = None
    best_count = 0

    for _ in range(FACE_RANSAC_TRIALS):
        indices = rng.choice(len(points), size=3, replace=False)
        a, b, c = points[indices]

        normal = np.cross(b - a, c - a)
        length = np.linalg.norm(normal)

        if length < 1e-12:
            continue

        normal = normal / length

        if abs(normal[2]) < minimum_normal_z:
            continue

        distances = np.abs((points - a) @ normal)
        inliers = distances <= FACE_PLANE_TOLERANCE
        count = int(np.count_nonzero(inliers))

        if count > best_count:
            best_count = count
            best_inliers = inliers

    if best_count < required_inliers:
        raise ValueError(
            f"Piano superiore con supporto insufficiente: "
            f"{best_count}/{len(points)} punti, "
            f"richiesti almeno {required_inliers}"
        )

    face_points = points[best_inliers]
    plane_origin = face_points.mean(axis=0)
    centered = face_points - plane_origin

    _, singular_values, axes = np.linalg.svd(
        centered, full_matrices=False
    )

    if singular_values[1] < 1e-6:
        raise ValueError(
            "Punti della superficie quasi allineati"
        )

    normal = axes[-1]
    if normal[2] < 0:
        normal = -normal

    if normal[2] < minimum_normal_z:
        raise ValueError(
            "Il piano affinato supera l'inclinazione ammessa"
        )

    residuals = centered @ normal
    rms = float(np.sqrt(np.mean(residuals ** 2)))

    face_mask = np.zeros_like(region_mask)
    face_mask[
        rows[best_inliers],
        columns[best_inliers],
    ] = 255

    return face_mask, normal, rms