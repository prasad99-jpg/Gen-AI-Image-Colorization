from deoldify.visualize import *

# Load DeOldify model
colorizer = get_image_colorizer(artistic=True)


def colorize_image(path):

    colorizer.plot_transformed_image(
        path,
        render_factor=35,
        compare=False
    )