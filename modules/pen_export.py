import os

from modules.vectorizer import vectorize
from modules.polyline import simplify
from modules.dxf_export import save_dxf


def save_pen_dxf(mask, output_dir, filename):
    """
    Fold Clean 이미지로부터
    Pen DXF 생성
    """

    points = vectorize(mask)
    points = simplify(points)

    if not points:
        return

    min_x = min(x for x, y in points)
    min_y = min(y for x, y in points)

    normalized = [
        (
            x - min_x,
            y - min_y
        )
        for x, y in points
    ]

    save_dxf(
        normalized,
        os.path.join(
            output_dir,
            filename
        )
    )