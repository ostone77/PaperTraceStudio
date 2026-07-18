import cv2
import os

def save_parts(img, parts):

    os.makedirs("output/parts", exist_ok=True)

    margin = 20

    count = 1

    for part in parts:

        x = part["x"]
        y = part["y"]
        w = part["w"]
        h = part["h"]

        x1 = max(0, x - margin)
        y1 = max(0, y - margin)

        x2 = min(img.shape[1], x + w + margin)
        y2 = min(img.shape[0], y + h + margin)

        crop = img[y1:y2, x1:x2]

        filename = f"output/parts/part{count:03d}.png"

        cv2.imwrite(filename, crop)

        count += 1

    print("저장된 부품 :", count - 1)