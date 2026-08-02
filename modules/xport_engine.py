import os
import cv2


def save_image(folder, name, image):

    cv2.imwrite(
        os.path.join(folder, name),
        image
    )


def save_part(folder, index, image):

    save_image(
        folder,
        f"part{index+1:03d}.png",
        image
    )