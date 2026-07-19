import cv2


def extract_fold_candidate(crop, cut):

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    _, line = cv2.threshold(
        gray,
        200,
        255,
        cv2.THRESH_BINARY_INV
    )

    candidate = cv2.subtract(
        line,
        cut
    )

    return candidate