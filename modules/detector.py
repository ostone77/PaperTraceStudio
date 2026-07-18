import cv2

from config import (
    MIN_PART_WIDTH,
    MIN_PART_HEIGHT,
    MIN_PART_AREA
)


def find_parts(mask):
    """
    부품 영역 검출
    """

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    parts = []

    for contour in contours:

        area = cv2.contourArea(contour)

        if area < MIN_PART_AREA:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        if w < MIN_PART_WIDTH:
            continue

        if h < MIN_PART_HEIGHT:
            continue

        parts.append({
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "area": area
        })

    parts = sorted(parts, key=lambda p: (p["y"], p["x"]))

    return parts