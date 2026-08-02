import os
import cv2

from modules.vectorizer import draw_points
from modules.dxf_export import save_dxf


def save_preview(points, cut, output_dir, filename):

    preview = draw_points(
        cut,
        points
    )

    cv2.imwrite(
        os.path.join(
            output_dir,
            filename
        ),
        preview
    )


def save_dxf_file(points, output_dir, filename):

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