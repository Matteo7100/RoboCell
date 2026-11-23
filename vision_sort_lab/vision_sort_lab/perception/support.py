"""Verifica geometrica dell'appoggio dei pezzi."""

import cv2
import numpy as np

from vision_sort_lab.perception.config import (
    FACE_PLANE_TOLERANCE,
    SUPPORT_GAP_PX,
    SUPPORT_OUTER_PX,
    SUPPORT_MIN_SECTOR_POINTS,
    SUPPORT_MIN_SECTORS,
    SUPPORT_MAX_ANGLE_DEG,
    MIN_CONTACT_SAMPLES,
    MAX_CONTACT_P10_GAP,
)
from vision_sort_lab.perception.planes import select_top_face
from vision_sort_lab.perception.projection import pixel_to_world

def support_contact(
    depth,
    region_mask,
    objects_mask,
    face_center,
    face_normal,
    support_origin,
    support_normal,
    camera_info,
    camera_transform,
):
    kernel = np.ones((3, 3), dtype=np.uint8)

    # Fascia di pixel esterni immediatamente vicini al pezzo.
    outside_band = cv2.subtract(
        cv2.dilate(region_mask, kernel),
        objects_mask,
    )
    outside_valid = (
        (outside_band > 0)
        & np.isfinite(depth)
        & (depth > 0)
    )
    rows, columns = np.nonzero(outside_valid)

    if rows.size == 0:
        raise ValueError(
            "Profondità esterna al bordo indisponibile"
        )

    outside_points = np.asarray(
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

    distances = np.abs(
        (outside_points - support_origin) @ support_normal
    )
    on_plane = distances <= FACE_PLANE_TOLERANCE

    plane_neighbors = np.zeros_like(region_mask)
    plane_neighbors[
        rows[on_plane],
        columns[on_plane],
    ] = 255

    # Qui l'erosione serve soltanto a estrarre il bordo.
    boundary = cv2.subtract(
        region_mask,
        cv2.erode(region_mask, kernel),
    )
    adjacent_to_plane = cv2.dilate(
        plane_neighbors, kernel
    )

    edge_valid = (
        (boundary > 0)
        & (adjacent_to_plane > 0)
        & np.isfinite(depth)
        & (depth > 0)
    )
    rows, columns = np.nonzero(edge_valid)

    if rows.size == 0:
        raise ValueError(
            "Bordo rosso adiacente al piano non osservabile"
        )

    edge_points = np.asarray(
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

    below_top = (
        (face_center - edge_points) @ face_normal
    ) > FACE_PLANE_TOLERANCE

    if not np.any(below_top):
        raise ValueError(
            "Il bordo osservato appartiene soltanto "
            "alla zona della faccia superiore"
        )

    gaps = (
        edge_points[below_top] - support_origin
    ) @ support_normal

    return (
        int(gaps.size),
        float(np.min(gaps)),
        float(np.percentile(gaps, 10)),
        float(np.median(gaps)),
    )


def support_plane(
    depth,
    region_mask,
    objects_mask,
    face_center,
    face_normal,
    camera_info,
    camera_transform,
    logger,
):
    outer_kernel = np.ones(
        (2 * SUPPORT_OUTER_PX + 1,) * 2,
        dtype=np.uint8,
    )
    gap_kernel = np.ones(
        (2 * SUPPORT_GAP_PX + 1,) * 2,
        dtype=np.uint8,
    )

    outer = cv2.dilate(region_mask, outer_kernel)
    excluded = cv2.dilate(objects_mask, gap_kernel)
    search_mask = cv2.subtract(outer, excluded)

    plane_mask, normal, rms = select_top_face(
        depth,
        search_mask,
        camera_info=camera_info,
        camera_transform=camera_transform,
    )

    rows, columns = np.nonzero(plane_mask)

    moments = cv2.moments(region_mask, binaryImage=True)
    center_u = moments["m10"] / moments["m00"]
    center_v = moments["m01"] / moments["m00"]

    sectors = (
        2 * (rows >= center_v).astype(np.int32)
        + (columns >= center_u).astype(np.int32)
    )
    sector_counts = np.bincount(sectors, minlength=4)
    covered_sectors = int(np.count_nonzero(
        sector_counts >= SUPPORT_MIN_SECTOR_POINTS
    ))

    if covered_sectors < SUPPORT_MIN_SECTORS:
        raise ValueError(
            f"Piano vicino osservato in pochi settori: "
            f"{sector_counts.tolist()}"
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

    alignment = float(np.dot(normal, face_normal))
    minimum_alignment = np.cos(
        np.deg2rad(SUPPORT_MAX_ANGLE_DEG)
    )

    if alignment < minimum_alignment:
        raise ValueError(
            "Piano vicino e faccia superiore "
            "superano l'angolo ammesso"
        )

    separation = float(
        np.dot(face_center - plane_origin, normal)
    )

    if separation <= FACE_PLANE_TOLERANCE:
        raise ValueError(
            "Separazione insufficiente fra faccia e piano vicino"
        )

    samples, minimum_gap, p10_gap, median_gap = support_contact(
        depth,
        region_mask,
        objects_mask,
        face_center,
        face_normal,
        plane_origin,
        normal,
        camera_info=camera_info,
        camera_transform=camera_transform,
    )

    logger.info(
        f"BORDO_INFERIORE_CANDIDATO | "
        f"campioni={samples} | "
        f"distanza_min={minimum_gap * 1000:.2f} mm | "
        f"p10={p10_gap * 1000:.2f} mm | "
        f"mediana={median_gap * 1000:.2f} mm"
    )

    if samples < MIN_CONTACT_SAMPLES:
        raise ValueError(
            f"Campioni del bordo insufficienti: {samples}, "
            f"richiesti almeno {MIN_CONTACT_SAMPLES}"
        )

    if abs(p10_gap) > MAX_CONTACT_P10_GAP:
        raise ValueError(
            f"Bordo incompatibile con il piano candidato: "
            f"p10={p10_gap * 1000:.2f} mm, "
            f"limite={MAX_CONTACT_P10_GAP * 1000:.2f} mm"
        )

    return (
        plane_mask,
        plane_origin,
        normal,
        rms,
        separation,
        sector_counts,
    )