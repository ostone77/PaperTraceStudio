import cv2


def find_parts(mask):

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    parts = []

    for contour in contours:

        area = cv2.contourArea(contour)

        # 너무 작은 객체 제거
        if area < 800:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        # 숫자 제거
        if w < 40:
            continue

        if h < 40:
            continue

        # 번호 제거
        if w * h < 2500:
            continue

        parts.append({
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "area": area,
            "contour": contour
        })

    # 큰 부품부터 정렬
    parts = sorted(
        parts,
        key=lambda p: p["area"],
        reverse=True
    )

    return parts