import cv2
import numpy as np


def extract_cut(part_img):

    gray = cv2.cvtColor(
        part_img,
        cv2.COLOR_BGR2GRAY
    )

    _, mask = cv2.threshold(
        gray,
        80,
        255,
        cv2.THRESH_BINARY_INV
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    canvas = np.full_like(mask, 255)

    if len(contours) == 0:
        return canvas

    biggest = max(
        contours,
        key=cv2.contourArea
    )

    cv2.drawContours(
        canvas,
        [biggest],
        -1,
        0,
        2
    )

    return canvas