import cv2

from config import VECTOR_EPSILON


def vectorize(mask):
    """
    Cut 마스크에서 외곽선을 추출하고
    꼭짓점(Vertex)만 반환한다.
    """
    mask = cv2.bitwise_not(mask)

    cv2.imwrite("output/debug_vector_mask.png", mask)
    
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    if not contours:
        return []

    contour = max(contours, key=cv2.contourArea)

    approx = cv2.approxPolyDP(
        contour,
        VECTOR_EPSILON,
        True
    )

    vertices = []

    for p in approx:

        x = int(p[0][0])
        y = int(p[0][1])

        vertices.append((x, y))

    return vertices


def draw_points(mask, points):

    preview = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    preview[mask > 0] = (180, 180, 180)

    for i, (x, y) in enumerate(points):

        cv2.circle(
            preview,
            (x, y),
            4,
            (0, 0, 255),
            -1
        )

        cv2.putText(
            preview,
            str(i),
            (x + 4, y - 4),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (255, 0, 0),
            1
        )

    # 꼭짓점을 선으로 연결
    if len(points) > 1:

        for i in range(len(points)):

            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]

            cv2.line(
                preview,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                1
            )

    return preview