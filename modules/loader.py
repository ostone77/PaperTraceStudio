from PIL import Image
import numpy as np
import cv2


def load_gif(path):

    pil = Image.open(path)
    pil.seek(0)
    pil = pil.convert("RGB")

    img = cv2.cvtColor(
        np.array(pil),
        cv2.COLOR_RGB2BGR
    )

    return img