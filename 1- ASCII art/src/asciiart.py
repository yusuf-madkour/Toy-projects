"""
Created on Mon Jun 15 04:48:22 2020

@author: Yusuf Madkour
"""
# Imports
import getopt
import sys
import numpy as np
from colorama import Fore, init
from skimage.io import imread
from skimage.transform import resize

if __name__ == "__main__":
    # Script parameters' defaults
    inv = False
    mode = 'average'
    color = Fore.WHITE

    # Arguments' handling
    argument_list = sys.argv[1:]
    short_options = "f:c:im:"
    long_options = ["file=", "color=", "inv", "mode="]
    try:
        arguments, _ = getopt.getopt(
            argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    for current_argument, current_value in arguments:
        if current_argument in ("-f", "--file"):
            image_path = current_value  # Image name, image has to be in the same directory if full path was not passed
        elif current_argument in ("-c", "--color"):
            colors = {'white': Fore.WHITE, 'green': Fore.GREEN,
                      'red': Fore.RED, 'blue': Fore.BLUE}
            color = colors.get(current_value.lower(),
                               Fore.WHITE)  # Colorama's color
        elif current_argument in ("-i", "--inv"):
            inv = True
        elif current_argument in ("-m", "--mode"):
            mode = current_value.lower()

    # Converting images' pixels to ASCII characters
    # These are ASCII characters sorted in ascending order from least to most bright
    ascii = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    # Converting to avoid overflow warning when computing pixel brightness values
    pixel_array = np.uint16(imread(image_path))
    # Double check that preserve_range and anti_aliasing actually do something
    pixel_array = resize(pixel_array, (320, 240),
                         preserve_range=True, anti_aliasing=True)
    print("Successfully loaded image!")
    print(f"Image size: {pixel_array.shape}")
    height, width = pixel_array.shape[0], pixel_array.shape[1]
    init()  # Initializing colorama

    # Inverting colors if inv flag is passed to the script
    pixel_array = 255 - pixel_array if inv else pixel_array

    modes = {'average': lambda p: (p[0] + p[1] + p[2]) // 3,  # Taking average of RGB values
             # Taking average of minimum and maximum RGB values
             'lightness': lambda p: (sorted(p)[2] + sorted(p)[0]) / 2,
             # Multiplying each color with a weight
             'luminosity': lambda p: 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]
             }

    print("Converting to brightness matrix...")

    # This nested list comprehension maps each pixel to the suitable ascii character based on the pixel's brightness
    converted_image = [[ascii[int(modes[mode](pixel) / 255 * 64)]
                        for pixel in row] for row in pixel_array]

    print(f"printing image in {mode} mode")
    # Printing image, one row at a time
    for row in converted_image:
        print(color + "".join(char for char in row))
