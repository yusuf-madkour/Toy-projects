# ASCII art

asciiart.py is a Python script that draws an image in terminal using ASCII characters. It is a toy project inspired by [Robert Heaton's Programming Projects for Advanced Beginners](https://robertheaton.com/2018/12/08/programming-projects-for-advanced-beginners/).

![](https://github.com/yusuf-madkour/toy-projects/blob/master/ASCII%20art/demo.gif)

## Installation

Install requirements as shown below and download the script.

```bash
pip install -r requirements.txt
```

## Usage

Run the script from terminal, replace /path/to/file with the path to your image. If the image exists in the same directory as your script, then you only need to provide the name of the image.

```bash
python asciiart.py -f /path/to/file
```
**Notes**

- I have only tested this script on Python 3.7.7 running on both windows 10 and pop os
- You may need to zoom out in your terminal window for the full image to be shown.
### Options

**--file**
Use this option to pass the full path of the image (or the name only if the image exists in the same path). This is required to be able to run the script.

**--color**
Use this option to choose the color you wish the image to be printed in. Available colors are white, green, red and blue. Default color is white. (Optional)

**--inv**
Pass this flag if you wish to invert the colors of your image. Default behavior is not inverting the image. (Optional)

**--mode**
Choose brightness mode using the -m option, available modes are average, lightness and luminosity. Average is the default mode. (Optional)

## License

[MIT](https://choosealicense.com/licenses/mit/)
