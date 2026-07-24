import cv2


def filter_fold(candidate):

    # 작은 점 제거
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (3, 3)
    )

    cleaned = cv2.morphologyEx(
        candidate,
        cv2.MORPH_OPEN,
        kernel
    )

    # 조금 두껍게
    cleaned = cv2.dilate(
        cleaned,
        kernel,
        iterations=1
    )

    return cleaned