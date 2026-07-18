from modules.loader import load_gif
from modules.preprocess import extract_black
from modules.detector import find_parts
from modules.splitter import save_parts
from modules.cut_detector import extract_cut
from modules.fold_detector import extract_fold

import cv2
import os

print("===================================")
print("Paper Trace Studio Build003-04")
print("===================================")

IMAGE_PATH = "sample/test.gif"

if not os.path.exists(IMAGE_PATH):
    print("파일이 없습니다.")
    input()
    quit()

print("GIF 읽는 중...")

img = load_gif(IMAGE_PATH)

mask = extract_black(img)

parts = find_parts(mask)

print(f"검출된 부품 : {len(parts)}")

saved = save_parts(img, parts)

import os
import cv2

os.makedirs("output/cut", exist_ok=True)

for i, part in enumerate(parts):

    x = part["x"]
    y = part["y"]
    w = part["w"]
    h = part["h"]

    margin = 20

    x1 = max(0, x - margin)
    y1 = max(0, y - margin)

    x2 = min(img.shape[1], x + w + margin)
    y2 = min(img.shape[0], y + h + margin)

    crop = img[y1:y2, x1:x2]

    cut = extract_cut(crop)

    filename = f"output/cut/part{i+1:03d}.png"

    cv2.imwrite(filename, cut)

    import os

os.makedirs("output/fold", exist_ok=True)

fold = extract_fold(crop, cut)

cv2.imwrite(
    f"output/fold/part{i+1:03d}.png",
    fold
)

print(f"저장된 부품 : {saved}")

os.makedirs("output", exist_ok=True)

cv2.imwrite("output/original.png", img)
cv2.imwrite("output/line_mask.png", mask)

# 부품 위치 표시
preview = img.copy()

for part in parts:
    x = part["x"]
    y = part["y"]
    w = part["w"]
    h = part["h"]

    cv2.rectangle(
        preview,
        (x, y),
        (x + w, y + h),
        (0, 255, 0),
        2
    )

cv2.imshow("Original", preview)
cv2.imshow("Line Mask", mask)

cv2.waitKey(0)
cv2.destroyAllWindows()