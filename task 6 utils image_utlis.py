import cv2


def save_output(
        image,
        path
):

    cv2.imwrite(
        path,
        image
    )