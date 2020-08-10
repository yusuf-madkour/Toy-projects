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

-h , --help      Shows help message and exit

-sc , --scale    Scales the width of the board by given multiplier

-w , --width     The width of the board

-l , --length    The length of the board

-sl , --sleep    Waiting time after each state render in seconds, can be float

-pb , --prob     Probability of each cell being alive

-p , --pattern   The path to a text file containing a 2d matrix of an initial state

## License

[MIT](https://choosealicense.com/licenses/mit/)
