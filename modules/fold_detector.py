import cv2
import numpy as np


def extract_fold(part_img, cut_mask):

    gray = cv2.cvtColor(part_img, cv2.COLOR_BGR2GRAY)

    _, line_mask = cv2.threshold(
        gray,
        80,
        255,
        cv2.THRESH_BINARY_INV
    )

    # Cut은 흰색(255), 배경은 검정(0)
    cut = cv2.bitwise_not(cut_mask)

    # Cut 제거
    fold = cv2.subtract(line_mask, cut)

    # 작은 점 제거
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(fold)

    clean = np.zeros_like(fold)

    for i in range(1, num_labels):

        area = stats[i, cv2.CC_STAT_AREA]

        if area > 10:
            clean[labels == i] = 255

    return clean