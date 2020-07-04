# ASCII art

asciiart.py is a Python script that renders an image in terminal using ASCII characters. It is a toy project inspired by [Robert Heaton's Programming Projects for Advanced Beginners](https://robertheaton.com/2018/12/08/programming-projects-for-advanced-beginners/).

![](https://github.com/yusuf-madkour/toy-projects/blob/master/ASCII%20art/demo.gif)

## Installation

Install requirements as shown below and download the script.

```bash
pip install -r requirements.txt
```

## Usage

Run the script from terminal, replace /path/to/file with the path to your image.

```bash
python asciiart.py /path/to/file
```
**Notes**

- I have only tested this script on Python 3.7.7 running on both windows 10 and pop os.
- You may need to zoom out in your terminal window for the full image to be shown.
### Options

asciiart.py [-h] [-m] [-i] [-c]

Required arguments: The path to the image you want to render.

Optional arguments:
  -h, --help      Show this help message and exit
  
  -m , --mode     Choose brightness mode, available options are average,
                  lightness and luminosity. Default is average.
                  
  -i, --inverted  Render the image inverted.
  
  -c , --color    Choose a color you want the image to be rendered in, default
                  is white.

## License

[MIT](https://choosealicense.com/licenses/mit/)
