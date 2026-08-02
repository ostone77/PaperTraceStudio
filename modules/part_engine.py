import os
import cv2

from config import PART_MARGIN

from modules.pen_layer import extract_pen
from modules.cut_detector import extract_cut
from modules.polyline import simplify
from modules.fold_candidate import extract_fold_candidate
from modules.fold_filter import filter_fold

from modules.vectorizer import vectorize
from modules.export_engine import (
    save_preview,
    save_dxf_file,
    save_svg_file,
)

from modules.pen_export import save_pen_dxf


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

    save_preview(

        points,

        cut,

        project.vector,

        f"part{index+1:03d}.png"

    )

    # ------------------------------------------
    # DXF Export
    # ------------------------------------------

    save_dxf_file(

        points,

        project.dxf,

        f"part{index+1:03d}.dxf"

    )

    # ------------------------------------------
    # SVG Export
    # ------------------------------------------

    save_svg_file(

        points,

        project.svg,

        f"part{index+1:03d}.svg"

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

    # ------------------------------------------
    # Pen DXF
    # ------------------------------------------

    save_pen_dxf(

        clean,

        project.pen_dxf,

        f"part{index+1:03d}.dxf"

    )