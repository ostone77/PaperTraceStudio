import cv2

from modules.preprocess import extract_black, clean_mask


def extract_pen(img):
    """
    모든 검은선을 Pen Layer로 추출
    """

    pen = extract_black(img)
    pen = clean_mask(pen)

    return pen