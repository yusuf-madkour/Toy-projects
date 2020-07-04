## Imports ##
import argparse
import numpy as np
from colorama import Fore, init
from skimage.io import imread
from skimage.transform import resize

text = {
    'general': 'This is my guided implementation of ASCII image renderer, guided by Robert Heaton.',
    'file': 'path to the image you want to render',
    'mode': 'Choose brightness mode, available options are average, lightness and luminosity. Default is average.',
    'inverted': 'Render the image inverted',
    'color': 'Choose a color you want the image to be rendered in, default is green.'}

if __name__ == "__main__":

    ## Arguments' handling ##
    parser = argparse.ArgumentParser(description=text['general'])
    parser.add_argument(
        '-m', '--mode', help=text['mode'], type=str, default='luminosity', metavar="")
    parser.add_argument('-i',
                        '--inverted', help=text['inverted'], action='store_true')
    parser.add_argument(
        '-c', '--color', help=text['color'], type=str, default='white', metavar="")
    parser.add_argument('file', help=text['file'], type=str, metavar="")
    args = parser.parse_args()

    colors = {'white': Fore.WHITE, 'green': Fore.GREEN,
              'red': Fore.RED, 'blue': Fore.BLUE}
    color = colors.get(args.color.lower(),
                       Fore.GREEN)  # Colorama's color

    ## Converting images' pixels to ASCII characters ##

    # These are ASCII characters sorted in ascending order from least to most bright
    ascii = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

    # Converting to avoid overflow warning when computing pixel brightness values
    pixel_array = np.uint16(imread(args.file))

    # pixel_array = resize(pixel_array, (120, 240),
    #                      preserve_range=True, anti_aliasing=True)

    print("Successfully loaded image!")

    height, width = pixel_array.shape[0], pixel_array.shape[1]
    init()  # Initializing colorama

    # Inverting colors if inv flag is passed to the script
    pixel_array = 255 - pixel_array if args.inverted else pixel_array

    modes = {'average': lambda p: (p[0] + p[1] + p[2]) // 3,  # Taking average of RGB values
             # Taking average of minimum and maximum RGB values
             'lightness': lambda p: (sorted(p)[2] + sorted(p)[0]) / 2,
             # Multiplying each color with a weight
             'luminosity': lambda p: 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]
             }

    print("Converting to brightness matrix...")

    # This nested list comprehension maps each pixel to the suitable ascii character based on the pixel's brightness and mode
    mode = modes.get(args.mode, modes['average'])
    converted_image = [[ascii[int(mode(pixel) / 255 * 64)]
                        for pixel in row] for row in pixel_array]

    ## Printing image to terminal ##
    print(f"printing image in {mode} mode")
    # Printing image, one row at a time
    for row in converted_image:
        print(color + "".join(char for char in row))
