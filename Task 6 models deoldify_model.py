import cv2


def colorize_image(path):

    image = cv2.imread(path)

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    colorized = cv2.applyColorMap(
        gray,
        cv2.COLORMAP_AUTUMN
    )

    cv2.imwrite(
        "result.png",
        colorized
    )