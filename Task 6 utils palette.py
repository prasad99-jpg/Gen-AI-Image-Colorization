import cv2
import numpy as np


def apply_historical_palette(
        image,
        era
):

    img = image.copy().astype(
        np.float32
    )

    if era == "1920s":

        img[:,:,2] *= 1.15
        img[:,:,1] *= 0.90
        img[:,:,0] *= 0.80

    elif era == "WWII":

        img[:,:,1] *= 1.20
        img[:,:,2] *= 0.90
        img[:,:,0] *= 0.85

    elif era == "1950s":

        img[:,:,0] *= 1.15
        img[:,:,1] *= 1.10
        img[:,:,2] *= 1.10

    img = np.clip(
        img,
        0,
        255
    )

    return img.astype(
        np.uint8
    )