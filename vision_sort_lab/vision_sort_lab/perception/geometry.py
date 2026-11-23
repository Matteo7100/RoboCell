"""Calcoli geometrici dei pezzi ricostruiti."""

import cv2
import numpy as np

from vision_sort_lab.perception.config import (
    FACE_PLANE_TOLERANCE,
    MIN_FACE_POINTS,
    SQUARE_REL_TOL,
    SUPPORT_MAX_ANGLE_DEG,
)
from vision_sort_lab.perception.projection import pixel_to_world

def solid_geometry(
    face_center,
    face_sides,
    face_normal,
    support_origin,
    support_normal,
):
    """Dimensioni e centro di un parallelepipedo retto."""
    length = float(max(face_sides))
    width = float(min(face_sides))

    if (
        not np.all(np.isfinite(face_sides))
        or width <= 0
    ):
        raise ValueError("Dimensioni della faccia non valide")

    # Le normali restituite dalla stima dei piani sono unitarie.
    alignment = float(
        np.dot(support_normal, face_normal)
    )
    minimum_alignment = np.cos(
        np.deg2rad(SUPPORT_MAX_ANGLE_DEG)
    )

    if (
        not np.isfinite(alignment)
        or alignment < minimum_alignment
    ):
        raise ValueError(
            "Faccia e appoggio non sufficientemente paralleli"
        )

    # Distanza dal piano lungo la normale della faccia.
    height = float(
        np.dot(
            face_center - support_origin,
            support_normal,
        ) / alignment
    )

    if (
        not np.isfinite(height)
        or height <= FACE_PLANE_TOLERANCE
    ):
        raise ValueError("Altezza ricostruita non valida")

    center_world = (
        face_center - 0.5 * height * face_normal
    )

    return length, width, height, center_world


def face_geometry(
    depth,
    face_mask,
    normal,
    camera_info,
    camera_transform,
):
    valid = (
        (face_mask > 0)
        & np.isfinite(depth)
        & (depth > 0)
    )
    rows, columns = np.nonzero(valid)

    if rows.size < MIN_FACE_POINTS:
        raise ValueError(
            f"Punti insufficienti per la geometria: {rows.size}"
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

    plane_origin = points.mean(axis=0)
    normal = np.asarray(normal, dtype=np.float64)

    # Due assi ortogonali sul piano della faccia.
    axis_x = np.array((1.0, 0.0, 0.0))
    axis_x = axis_x - np.dot(axis_x, normal) * normal
    axis_x = axis_x / np.linalg.norm(axis_x)
    axis_y = np.cross(normal, axis_x)

    centered = points - plane_origin
    plane_points = np.column_stack(
        (centered @ axis_x, centered @ axis_y)
    ).astype(np.float32)

    rectangle = cv2.minAreaRect(plane_points)
    center_plane, sides, _ = rectangle

    if (
        not np.all(np.isfinite(sides))
        or min(sides) <= 0
    ):
        raise ValueError("Rettangolo della faccia degenere")

    length = float(max(sides))
    width = float(min(sides))

    center_world = (
        plane_origin
        + center_plane[0] * axis_x
        + center_plane[1] * axis_y
    )

    # Ricaviamo i quattro bordi dai vertici del rettangolo.
    corners = cv2.boxPoints(rectangle).astype(np.float64)
    edges_plane = (
        np.roll(corners, -1, axis=0) - corners
    )
    edge_lengths = np.linalg.norm(
        edges_plane, axis=1
    )

    # Un bordo lungo e quello opposto descrivono lo stesso asse.
    long_edge_index = int(np.argmax(edge_lengths))
    edge_plane = edges_plane[long_edge_index]

    edge_world = (
        edge_plane[0] * axis_x
        + edge_plane[1] * axis_y
    )

    relative_difference = (length - width) / length
    nearly_square = (
        relative_difference <= SQUARE_REL_TOL
    )
    yaw_period = 90 if nearly_square else 180

    yaw_deg = float(
        np.degrees(
            np.arctan2(edge_world[1], edge_world[0])
        ) % yaw_period
    )

    return (
        center_world,
        (length, width),
        yaw_deg,
        yaw_period,
    )