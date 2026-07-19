import cv2
import numpy as np


def skeletonize(mask):
    """
    OpenCV Morphology 기반 Skeleton 생성
    """

    img = cv2.bitwise_not(mask)

    img = (img > 0).astype(np.uint8) * 255

    skel = np.zeros(img.shape, np.uint8)

    kernel = cv2.getStructuringElement(
        cv2.MORPH_CROSS,
        (3, 3)
    )

    while True:

        opened = cv2.morphologyEx(
            img,
            cv2.MORPH_OPEN,
            kernel
        )

        temp = cv2.subtract(img, opened)

        eroded = cv2.erode(
            img,
            kernel
        )

        skel = cv2.bitwise_or(
            skel,
            temp
        )

        img = eroded.copy()

        if cv2.countNonZero(img) == 0:
            break

    return skel