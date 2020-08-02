# Conway's game of life

life.py is a Python script that simulates [Conway's game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in terminal. It is a toy project inspired by [Robert Heaton's Programming Projects for Advanced Beginners](https://robertheaton.com/2018/12/08/programming-projects-for-advanced-beginners/).

![](https://github.com/yusuf-madkour/toy-projects/blob/master/Conway's%20game%20of%20life/demo.gif)


## Usage

life.py [-h] [-sc] [-w] [-l] [-sl] [-pb] [-p]

Run the script from terminal as shown below if you wish to use default options

```bash
python life.py
```
**Notes**

- I have only tested this script on Python 3.7.7 running on both windows 10 and pop os

### Optional arguments

-h, --help       shows help message and exit

-sc , --scale    scales the width of the board by given multiplier, scale value must be of type integer

-w , --width     specify width of the board, must be integer

-l , --length    specify length of the board, must be integer

-sl , --sleep    specify sleep time after every board render, values should be float (in seconds)

-pb , --prob     Higher probability means higher probability of alive cells being generated in the board

-p , --pattern   pass the name of a text file that holds a 2d matrix of an initial state, file must be in the patterns folder

## License

[MIT](https://choosealicense.com/licenses/mit/)
