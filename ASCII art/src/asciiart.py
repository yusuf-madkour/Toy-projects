import argparse
import numpy as np
from colorama import Fore, init
from skimage.io import imread
from skimage.transform import resize
import pyautogui as pag
import ctypes
import os
import sys

text = {
    'general': 'This is my guided implementation of ASCII image renderer, guided by Robert Heaton',
    'file': 'The absolute path to the image you want to render',
    'mode': 'Choose brightness mode, available options are average, lightness and luminosity. Default is average',
    'inverted': 'Render the image inverted',
    'color': 'Choose a color you want the image to be rendered in, default is white'}

user32 = ctypes.WinDLL('user32')


def resize_cmd(size):
    fore_window = user32.GetForegroundWindow()
    user32.ShowWindow(fore_window, size)


if __name__ == "__main__":

    ## Arguments' handling ##
    parser = argparse.ArgumentParser(description=text['general'])
    parser.add_argument('file', help=text['file'], type=str)
    parser.add_argument(
        '-m', '--mode', help=text['mode'], type=str, default='luminosity', metavar="")
    parser.add_argument('-i',
                        '--inverted', help=text['inverted'], action='store_true')
    parser.add_argument(
        '-c', '--color', help=text['color'], type=str, default='white', metavar="")
    args = parser.parse_args()

    colors = {'white': Fore.WHITE, 'green': Fore.GREEN,
              'red': Fore.RED, 'blue': Fore.BLUE}
    color = colors.get(args.color.lower(),
                       Fore.WHITE)  # Colorama's color

    ## Converting images' pixels to ASCII characters ##

    # These are ASCII characters sorted in ascending order from least to most bright
    ascii = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

    # Trying to read image
    try:
        im = imread(args.file)
    except FileNotFoundError:
        print("Image path is invalid")
        sys.exit(2)

    # Converting to avoid overflow warning when computing pixel brightness values
    pixel_array = np.uint16(im)
    pixel_array = resize(pixel_array, (128, 256),
                         preserve_range=True, anti_aliasing=True)

    init()  # Initializing colorama

    # Inverting colors if inv flag is passed to the script
    pixel_array = 255 - pixel_array if args.inverted else pixel_array

    modes = {'average': lambda p: (p[0] + p[1] + p[2]) // 3,  # Taking average of RGB values
             # Taking average of minimum and maximum RGB values
             'lightness': lambda p: (sorted(p)[2] + sorted(p)[0]) / 2,
             # Multiplying each color with a weight
             'luminosity': lambda p: 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]
             }

    # This nested list comprehension maps each pixel to the suitable ascii character based on the pixel's brightness and mode
    mode = modes.get(args.mode, modes['average'])
    converted_image = [[ascii[int(mode(pixel) / 255 * 64)]
                        for pixel in row] for row in pixel_array]

    ## Printing image to terminal ##

    # Printing image, one row at a time
    for row in converted_image:
        print(color + "".join(char for char in row))

    ## Resizing cmd window to fit the image ##
    if os.name == 'nt':
        # Maximize
        resize_cmd(3)

        # Zoom out
        pag.keyDown('ctrl')
        for _ in range(4):
            pag.scroll(-1000)
        pag.keyUp('ctrl')

        # Minimize
        resize_cmd(1)

        # Maximize
        resize_cmd(3)

        # Scroll up
        pag.scroll(4500)
