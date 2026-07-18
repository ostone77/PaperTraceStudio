from modules.loader import load_gif
from modules.preprocess import extract_black, clean_mask
from modules.detector import find_parts
from modules.splitter import save_parts
from modules.cut_detector import extract_cut
from modules.fold_detector import extract_fold

from config import PART_MARGIN

import cv2
import os


print("===================================")
print("Paper Trace Studio Build006.1")
print("===================================")

IMAGE_PATH = "sample/test.gif"

if not os.path.exists(IMAGE_PATH):
    print("파일이 없습니다.")
    input()
    quit()

print("GIF 읽는 중...")

# --------------------------------------------------
# GIF 로드
# --------------------------------------------------

img = load_gif(IMAGE_PATH)

# --------------------------------------------------
# 검은선 추출
# --------------------------------------------------

mask = extract_black(img)
mask = clean_mask(mask)

# --------------------------------------------------
# 부품 검출
# --------------------------------------------------

parts = find_parts(mask)

print(f"검출된 부품 : {len(parts)}")

# --------------------------------------------------
# 부품 저장
# --------------------------------------------------

saved = save_parts(img, parts)

print(f"저장된 부품 : {saved}")

# --------------------------------------------------
# 출력 폴더 생성
# --------------------------------------------------

os.makedirs("output", exist_ok=True)
os.makedirs("output/cut", exist_ok=True)
os.makedirs("output/fold", exist_ok=True)

# --------------------------------------------------
# Cut / Fold 저장
# --------------------------------------------------

for i, part in enumerate(parts):

    x = part["x"]
    y = part["y"]
    w = part["w"]
    h = part["h"]

    x1 = max(0, x - PART_MARGIN)
    y1 = max(0, y - PART_MARGIN)

    x2 = min(img.shape[1], x + w + PART_MARGIN)
    y2 = min(img.shape[0], y + h + PART_MARGIN)

    crop = img[y1:y2, x1:x2]

    # Cut
    cut = extract_cut(crop)

    cv2.imwrite(
        f"output/cut/part{i+1:03d}.png",
        cut
    )

    # Fold
    fold = extract_fold(crop, cut)

    cv2.imwrite(
        f"output/fold/part{i+1:03d}.png",
        fold
    )

# --------------------------------------------------
# Debug 저장
# --------------------------------------------------

cv2.imwrite("output/original.png", img)
cv2.imwrite("output/line_mask.png", mask)

# --------------------------------------------------
# Preview
# --------------------------------------------------

preview = img.copy()

for part in parts:

    cv2.rectangle(
        preview,
        (part["x"], part["y"]),
        (part["x"] + part["w"], part["y"] + part["h"]),
        (0, 255, 0),
        2
    )

cv2.imshow("Original", preview)
cv2.imshow("Line Mask", mask)

cv2.waitKey(0)
cv2.destroyAllWindows()