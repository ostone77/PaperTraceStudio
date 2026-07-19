import cv2
import numpy as np


def simplify(points, epsilon=2.0):

    if len(points) < 3:
        return points

    contour = np.array(points, dtype=np.int32)
    contour = contour.reshape((-1, 1, 2))

    approx = cv2.approxPolyDP(
        contour,
        epsilon,
        True
    )

    result = []

    for p in approx:
        x = int(p[0][0])
        y = int(p[0][1])
        result.append((x, y))

    return result