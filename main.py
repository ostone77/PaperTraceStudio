from modules.loader import load_gif
from modules.pdf_loader import load_pdf

from modules.part_engine import process_part

from modules.preprocess import extract_black, clean_mask
from modules.detector import find_parts
from modules.splitter import save_parts

from modules.pen_layer import extract_pen
from modules.cut_detector import extract_cut

from modules.vectorizer import vectorize, draw_points
from modules.polyline import simplify
from modules.dxf_export import save_dxf

from modules.fold_candidate import extract_fold_candidate
from modules.fold_filter import filter_fold

from config import PART_MARGIN

import cv2
import os


print("======================================================")
print("Paper Trace Studio Build012A - Extract part processing")
print("======================================================")


# --------------------------------------------------
# Input
# --------------------------------------------------

def find_input_file():

    input_dir = "input"

    if not os.path.exists(input_dir):
        return None

    exts = [".pdf", ".gif"]

    for file in sorted(os.listdir(input_dir)):

        ext = os.path.splitext(file)[1].lower()

        if ext in exts:
            return os.path.join(input_dir, file)

    return None


print("현재 작업 폴더 :", os.getcwd())

IMAGE_PATH = find_input_file()

if IMAGE_PATH is None:

    print("input 폴더에 PDF 또는 GIF가 없습니다.")
    input()
    quit()


PROJECT_NAME = os.path.splitext(
    os.path.basename(IMAGE_PATH)
)[0]


OUTPUT_DIR = os.path.join(
    "output",
    PROJECT_NAME
)


print(f"입력 파일 : {IMAGE_PATH}")


ext = os.path.splitext(
    IMAGE_PATH
)[1].lower()


if ext == ".gif":

    print("GIF 읽는 중...")
    img = load_gif(IMAGE_PATH)

elif ext == ".pdf":

    print("PDF 읽는 중...")
    img = load_pdf(IMAGE_PATH)

else:

    raise Exception("지원하지 않는 파일 형식입니다.")


# --------------------------------------------------
# Output Folder
# --------------------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

PEN_DIR = os.path.join(OUTPUT_DIR, "pen")
CUT_DIR = os.path.join(OUTPUT_DIR, "cut")
VECTOR_DIR = os.path.join(OUTPUT_DIR, "vector_preview")
DXF_DIR = os.path.join(OUTPUT_DIR, "dxf")
FOLD_CANDIDATE_DIR = os.path.join(OUTPUT_DIR, "fold_candidate")
FOLD_CLEAN_DIR = os.path.join(OUTPUT_DIR, "fold_clean")

os.makedirs(PEN_DIR, exist_ok=True)
os.makedirs(CUT_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)
os.makedirs(DXF_DIR, exist_ok=True)
os.makedirs(FOLD_CANDIDATE_DIR, exist_ok=True)
os.makedirs(FOLD_CLEAN_DIR, exist_ok=True)


# --------------------------------------------------
# Preprocess
# --------------------------------------------------

mask = extract_black(img)
mask = clean_mask(mask)


# --------------------------------------------------
# Part Detection
# --------------------------------------------------

parts = find_parts(mask)

print(f"검출된 부품 : {len(parts)}")


saved = save_parts(
    img,
    parts
)

print(f"저장된 부품 : {saved}")

print(
    "vector_preview 존재 :",
    os.path.exists(VECTOR_DIR)
)


# --------------------------------------------------
# Process Parts
# --------------------------------------------------

output_dirs = {
    "pen": PEN_DIR,
    "cut": CUT_DIR,
    "vector": VECTOR_DIR,
    "dxf": DXF_DIR,
    "fold_candidate": FOLD_CANDIDATE_DIR,
    "fold_clean": FOLD_CLEAN_DIR,
}

for i, part in enumerate(parts):

    process_part(

        i,

        part,

        img,

        PEN_DIR,

        CUT_DIR,

        VECTOR_DIR,

        DXF_DIR,

        FOLD_CANDIDATE_DIR,

        FOLD_CLEAN_DIR

    )

# --------------------------------------------------
# Debug Save
# --------------------------------------------------

cv2.imwrite(

    os.path.join(

        OUTPUT_DIR,

        "original.png"

    ),

    img

)

cv2.imwrite(

    os.path.join(

        OUTPUT_DIR,

        "line_mask.png"

    ),

    mask

)


# --------------------------------------------------
# Preview
# --------------------------------------------------

preview = img.copy()

for part in parts:

    cv2.rectangle(

        preview,

        (part["x"], part["y"]),

        (

            part["x"] + part["w"],

            part["y"] + part["h"]

        ),

        (0, 255, 0),

        2

    )


print()
print("===================================")
print("Processing Complete")
print("===================================")
print(f"Project : {PROJECT_NAME}")
print(f"Parts   : {len(parts)}")
print(f"Output  : {OUTPUT_DIR}")
print()


cv2.imshow(

    "Original",

    preview

)

cv2.imshow(

    "Line Mask",

    mask

)

cv2.waitKey(0)
cv2.destroyAllWindows()