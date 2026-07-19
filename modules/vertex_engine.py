import math


def distance(p1, p2):
    return math.hypot(
        p2[0] - p1[0],
        p2[1] - p1[1]
    )


def angle(p1, p2, p3):

    ax = p2[0] - p1[0]
    ay = p2[1] - p1[1]

    bx = p3[0] - p2[0]
    by = p3[1] - p2[1]

    cross = ax * by - ay * bx
    dot = ax * bx + ay * by

    return math.degrees(
        math.atan2(cross, dot)
    )


def simplify(points,
             min_length=3,
             angle_threshold=8):

    if len(points) < 3:
        return points

    result = [points[0]]

    last = points[0]

    for i in range(1, len(points)-1):

        p = points[i]
        n = points[i+1]

        if distance(last, p) < min_length:
            continue

        a = abs(angle(last, p, n))

        if a > angle_threshold:
            result.append(p)
            last = p

    result.append(points[-1])

    return result