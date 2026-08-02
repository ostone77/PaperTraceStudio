import os
import cv2

from config import PART_MARGIN

from modules.pen_layer import extract_pen
from modules.cut_detector import extract_cut
from modules.vectorizer import vectorize, draw_points
from modules.polyline import simplify
from modules.dxf_export import save_dxf
from modules.fold_candidate import extract_fold_candidate
from modules.fold_filter import filter_fold


def process_part(
    index,
    part,
    img,
    project,
):

    x = part["x"]
    y = part["y"]
    w = part["w"]
    h = part["h"]

    x1 = max(0, x - PART_MARGIN)
    y1 = max(0, y - PART_MARGIN)

    x2 = min(img.shape[1], x + w + PART_MARGIN)
    y2 = min(img.shape[0], y + h + PART_MARGIN)

    crop = img[y1:y2, x1:x2]

    # ------------------------------------------
    # Pen Layer
    # ------------------------------------------

    pen = extract_pen(crop)

    cv2.imwrite(
        os.path.join(
            project.pen,
            f"part{index+1:03d}.png"
        ),
        pen
    )

    # ------------------------------------------
    # Cut Layer
    # ------------------------------------------

    cut = extract_cut(crop)

    cv2.imwrite(
        os.path.join(
            project.cut,
            f"part{index+1:03d}.png"
        ),
        cut
    )

    # ------------------------------------------
    # Vectorize
    # ------------------------------------------

    points = vectorize(cut)
    points = simplify(points)

    print(
        f"part{index+1:03d} : {len(points)} points"
    )

    # ------------------------------------------
    # Vector Preview
    # ------------------------------------------

    preview = draw_points(
        cut,
        points
    )

    cv2.imwrite(
        os.path.join(
            project.vector,
            f"part{index+1:03d}.png"
        ),
        preview
    )

    # ------------------------------------------
    # DXF Export
    # ------------------------------------------

    if points:

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
                project.dxf,
                f"part{index+1:03d}.dxf"
            )
        )

    # ------------------------------------------
    # Fold Candidate
    # ------------------------------------------

    candidate = extract_fold_candidate(
        crop,
        cut
    )

    cv2.imwrite(
        os.path.join(
            project.fold_candidate,
            f"part{index+1:03d}.png"
        ),
        candidate
    )

    # ------------------------------------------
    # Fold Clean
    # ------------------------------------------

    clean = filter_fold(
        candidate
    )

    cv2.imwrite(
        os.path.join(
            project.fold_clean,
            f"part{index+1:03d}.png"
        ),
        clean
    )