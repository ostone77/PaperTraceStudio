import cv2

from config import (
    BLACK_THRESHOLD,
    MIN_COMPONENT_AREA
)


def extract_black(img):
    """
    검은 선만 추출
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, mask = cv2.threshold(
        gray,
        BLACK_THRESHOLD,
        255,
        cv2.THRESH_BINARY_INV
    )

    return mask


def clean_mask(mask):
    """
    작은 노이즈 제거
    """

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask)

    cleaned = mask.copy()

    for i in range(1, num_labels):

        area = stats[i, cv2.CC_STAT_AREA]

        if area < MIN_COMPONENT_AREA:

            cleaned[labels == i] = 0

    return cleaned