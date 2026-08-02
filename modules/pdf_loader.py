import fitz
import cv2
import numpy as np


def load_pdf(path):

    doc = fitz.open(path)

    page = doc.load_page(0)

    pix = page.get_pixmap(
        dpi=300,
        alpha=False
    )

    img = np.frombuffer(
        pix.samples,
        dtype=np.uint8
    )

    img = img.reshape(
        pix.height,
        pix.width,
        pix.n
    )

    img = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2BGR
    )

    doc.close()

    return img