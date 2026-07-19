import cv2
import numpy as np


def detect_width(mask):

    dist = cv2.distanceTransform(
        mask,
        cv2.DIST_L2,
        5
    )

    if dist.max() > 0:
        dist = dist / dist.max() * 255

    return dist.astype(np.uint8)