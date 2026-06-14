import cv2


def apply_palette(image, era):

    img = image.copy()

    # 1900s
    if era == "1900s":

        img[:,:,2] *= 1.15
        img[:,:,1] *= 0.90
        img[:,:,0] *= 0.80

    # 1920s
    elif era == "1920s":

        img[:,:,2] *= 1.10
        img[:,:,1] *= 0.95

    # WWII
    elif era == "WWII":

        img[:,:,1] *= 1.20
        img[:,:,2] *= 0.90

    # 1950s
    elif era == "1950s":

        img[:,:,0] *= 1.15
        img[:,:,1] *= 1.10
        img[:,:,2] *= 1.10

    img = cv2.convertScaleAbs(img)

    return img