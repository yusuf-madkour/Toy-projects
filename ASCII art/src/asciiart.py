import argparse
import sys

import numpy as np
from colorama import Fore, init
from skimage.io import imread
from skimage.transform import resize

# These are ASCII characters sorted in ascending order from least to most bright
ASCII = '`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'

MODES = {
    "average": lambda p: (p[0] + p[1] + p[2]) // 3,  # Taking average of RGB values
    # Taking average of minimum and maximum RGB values
    "lightness": lambda p: (sorted(p)[2] + sorted(p)[0]) / 2,
    # Multiplying each color with a weight
    "luminosity": lambda p: 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2],
}

TXT = {
    "general": "This is my guided implementation of ASCII image renderer, \
                guided by Robert Heaton",
    "file": "The absolute path to the image you want to render",
    "mode": "Choose brightness mode",
    "inverted": "Render the image inverted",
    "color": "Choose a color you want the image to be rendered in",
}


def parse_arguments():
    """
    Parses the arguments from CLI

    Parameters
    ----------
    None

    Returns
    -------
    Parsed arguments
    """
    parser = argparse.ArgumentParser(description=TXT["general"])
    parser.add_argument("file", help=TXT["file"], type=str)
    parser.add_argument(
        "-m",
        "--mode",
        help=TXT["mode"],
        type=str,
        default="luminosity",
        metavar="",
        choices=MODES,
    )
    parser.add_argument("-i", "--inverted", help=TXT["inverted"], action="store_true")
    parser.add_argument(
        "-c",
        "--color",
        help=TXT["color"],
        default="white",
        choices=[
            "white",
            "red",
            "blue",
            "cyan",
            "magenta",
            "green",
            "yellow",
            "black",
        ],
        metavar="",
    )
    return parser.parse_args()


def load_image(path):
    """
    Tries to load the image using the passed path.
    If the image does not exist, it stops the execution of the script.

    Parameters
    ----------
    filepath: The path to the image

    Returns
    -------
    The image pixels as a numpy array with data type of uint16
    """
    # Trying to read the image
    try:
        image = imread(args.file)
    except FileNotFoundError:
        print("Image path is invalid")
        sys.exit(2)
    # Converting to avoid overflow warning when computing pixel brightness values
    return np.uint16(image)


if __name__ == "__main__":
    args = parse_arguments()
    image = load_image(args.file)

    # Resizing the image to fit the terminal window
    image = resize(image, (120, 240), preserve_range=True, anti_aliasing=True)

    # Inverting colors if inv flag is passed to the script
    image = 255 - image if args.inverted else image

    # mode is the brightness mode used to convert a pixel into an ascii character
    mode = MODES[args.mode]

    # color used to render the image in terminal
    color = getattr(Fore, args.color.upper())

    # This nested list comprehension maps each pixel to the closest ascii character
    converted_image = [
        [ASCII[int(mode(pixel) / 255 * 64)] for pixel in row] for row in image
    ]
    # Initializing colorama
    init(autoreset=True)

    # Printing image, one row at a time
    for row in converted_image:
        print(color + "".join(char for char in row))
