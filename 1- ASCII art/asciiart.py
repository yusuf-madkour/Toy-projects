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

# Script parameters' defaults
inv = False
mode = 'average'
color = Fore.WHITE

# Arguments' handling
argument_list = sys.argv[1:]
short_options = "f:c:im:h"
long_options = ["file=", "color=", "inv", "mode=", "help"]
try:
    arguments, _ = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    print(str(err))
    sys.exit(2)

for current_argument, current_value in arguments:
    if current_argument in ("-f", "--file"):
        image_name = current_value  # Image name, image has to be in the same directory
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
im = np.uint16(imread(image_name))
im = resize(im, (320, 240), preserve_range=True, anti_aliasing=True)
print("Successfully loaded image!")
print(f"Image size: {im.shape}")
height, width = im.shape[0], im.shape[1]
init()  # Initializing colorama

# Inverting colors if inv flag is passed to the script
im = 255 - im if inv else im

modes = {'average': lambda p: (p[0] + p[1] + p[2]) // 3,  # Taking average of RGB values
         # Taking average of minimum and maximum RGB values
         'lightness': lambda p: (sorted(p)[2] + sorted(p)[0]) / 2,
         'luminosity': lambda p: 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]}  # Multiplying each color with a weight

print("Converting to brightness matrix...")

# This nested list comprehension maps each pixel to the suitable ascii character based on the pixel's brightness
# Refer to the commented nested for loop below if this line looks cryptic
converted_image = [[ascii[int(modes[mode](pixel) / 255 * 64)]
                    for pixel in row] for row in im]

print(f"printing image in {mode} mode")
# Printing image, one row at a time
for row in converted_image:
    print(color + "".join(2*char for char in row))
