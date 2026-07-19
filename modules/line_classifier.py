import cv2
import numpy as np


def classify_lines(mask):

    """
    선 굵기를 계산하기 위한 거리 변환
    """

    dist = cv2.distanceTransform(
        mask,
        cv2.DIST_L2,
        3
    )

    normalized = cv2.normalize(
        dist,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    preview = normalized.astype(np.uint8)

    return preview