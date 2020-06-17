# asciiart

asciiart.py is a Python script that draws an image in command prompt using ASCII characters. It is a toy project inspired by [Robert Heaton's Programming Projects for Advanced Beginners](https://robertheaton.com/2018/12/08/programming-projects-for-advanced-beginners/).

![](https://github.com/yusuf-madkour/toy-projects/blob/master/demo.gif)

## Installation

Install requirements as shown below and download script.

```bash
pip install -r requirements.txt
```

## Usage

Run the script from terminal, replace filename with the name of the image you wish to draw. Image must be in the same directory as this script.

```bash
python asciiart.py -f filename
```

### Options

**--file**
Use this option to pass file name of image. This is required to be able to run the script.

**--color**
Use this option to choose the color you wish the image to be printed in. Available colors are white, green, red and blue. Default color is white. (Optional)

**--inv**
Pass this flag if you wish to invert the colors of your image. Default behavior is not inverting the image. (Optional)

**--mode**
Choose brightness mode using the -m option, available modes are average, lightness and luminosity. Average is the default mode. (Optional)

## License

[MIT](https://choosealicense.com/licenses/mit/)
