import cv2


def extract_black(img):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    _, mask = cv2.threshold(
        gray,
        80,
        255,
        cv2.THRESH_BINARY_INV
    )

    return mask