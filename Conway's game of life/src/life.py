import curses
from argparse import ArgumentParser, ArgumentTypeError
from copy import deepcopy
from random import choices
from time import sleep

PC = '$'  # This is the Printed Character that represents a single cell


def random_state(width, length, prob):
    """
    Builds a board with all cells pseudo-randomly set. The board is
    represented as a list of lists throughout the script.

    Parameters
    ----------
    width: width of the board, in cells
    length: length of the board, in cells
    prob: probability of a cell being alive

    Returns
    -------
    A board of dimension width x length with specific probability of cells
    being alive
    """
    return [choices([0, 1], k=width, weights=[1-prob, prob]) for _ in range(length)]


def load_board_state(filename):
    """
    Tries to load the initial state of a board from a text file where a dead
    cell is represented by 0 and a live cell is represented by 1.
    If the file does not exist, it returns a random board instead.

    Parameters
    ----------
    filename: name of the text file to load the board from

    Returns
    -------
    The board loaded from the text file represented as a list of lists
    """
    try:
        with open('../patterns/' + filename, mode='r') as f:
            return [[int(c) for c in row.rstrip('\n')] for row in f.readlines()]
    except FileNotFoundError:
        print("File does not exist, generating a random pattern...")
        sleep(3)
        return random_state(args.width, args.length, args.prob)


def render(board):
    """
    Renders the board to terminal

    Parameters
    ----------
    board: A list of lists representing the board state.

    Returns
    -------
    Nothing
    """
    screen.addstr(
        '=' * (args.scale * len(board[0])+2) + '\n', curses.A_BOLD)
    for row in board:
        screen.addstr('|', curses.A_BOLD)
        for c in row:
            if c == 1:
                screen.addstr(PC * args.scale, curses.color_pair(2))
            else:
                screen.addstr(PC * args.scale, curses.color_pair(1))
        screen.addstr('|' + '\n', curses.A_BOLD)
    screen.addstr(
        '=' * (args.scale * len(board[0])+2) + '\n', curses.A_BOLD)
    screen.refresh()
    curses.napms(int(args.sleep*1000))
    screen.clear()


def moore_neighbours(board):
    """
    Finds neighbours of each cell in the board

    Parameters
    ----------
    board: A list of lists representing the board state

    Returns
    -------
    Neighbours of all cells, it returns a list of lists with the same
    dimensions of the board but containing lists of neighbours instead of cell values
    """
    neighbours = [[[] for _ in row] for row in board]
    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            if i > 0:
                neighbours[i][j].extend(board[i-1][max(0, j-1):j+2])
            if i < len(board)-1:
                neighbours[i][j].extend(board[i+1][max(0, j-1):j+2])
            if j > 0:
                neighbours[i][j].append(board[i][j-1])
            if j < len(board[i])-1:
                neighbours[i][j].append(board[i][j+1])
    return neighbours


def next_state(board):
    """
    Calculates the next state of the board based on the current state.
    Effectively takes a single step in the game of life.

    Parameters
    ----------
    board: A list of lists representing the current board state

    Returns
    -------
    The next state of the board represented as a list of lists
    """
    neighbours = moore_neighbours(board)
    new_board = deepcopy(board)
    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            # Underpopulation or Overpopulation
            if neighbours[i][j].count(1) in [0, 1] or neighbours[i][j].count(1) > 3:
                new_board[i][j] = 0
                continue
            if neighbours[i][j].count(1) == 3:  # Reproduction
                new_board[i][j] = 1
    return new_board


def probability(x):
    """
    This is a custom type function for the argument parser, it checks the
    passed probability value and verifies that it is a valid probability
    between 0 and 1.

    Parameters
    ----------
    x: parsed probability value

    Returns
    -------
    The value if it is a valid probability and raises an exception if it isn't.
    """
    x = float(x)
    if not 0 < x < 1:
        raise ArgumentTypeError("Not a valid probability")
    return x


def parse_arguments():
    txt = {
        'general': 'This is my guided implementation of "Conway\'s \
                Game of Life", guided by Robert Heaton.',
        'scale': 'scales the width of the board by given multiplier,\
              scale value must be of type integer',
        'width': 'specify width of the board, must be integer',
        'length': 'specify length of the board, must be integer',
        'sleep': 'specify sleep time after every board render,\
              values are expected to be float (in seconds)',
        'prob': 'Probability of alive cells being generated in the board',
        'pattern': 'pass the name of a text file that holds a 2d matrix\
                of an initial state, file must be in patterns folder'}

    parser = ArgumentParser(description=txt['general'])

    parser.add_argument(
        '-sc', '--scale', help=txt['scale'], type=int, default=2, metavar="")
    parser.add_argument(
        '-w', '--width', help=txt['width'], type=int, default=20, metavar="")
    parser.add_argument(
        '-l', '--length', help=txt['length'], type=int, default=20, metavar="")
    parser.add_argument(
        '-sl', '--sleep', help=txt['sleep'], type=float, default=0.05, metavar="")
    parser.add_argument(
        '-pb', '--prob', help=txt['prob'], type=probability, default=0.3, metavar="")
    parser.add_argument(
        '-p', '--pattern', help=txt['pattern'], type=str, metavar="")
    return parser.parse_args()


def init_curses():
    """
    This function initializes the screen and prepares the colors for printing
    dead and live cells

    Parameters
    ----------
    None

    Returns
    -------
    curses screen
    """
    screen = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
    return screen


if __name__ == '__main__':
    args = parse_arguments()
    screen = init_curses()
    # Board initialization
    if args.pattern:
        board = load_board_state(args.pattern)
    else:
        board = random_state(args.width, args.length, args.prob)

    while board != next_state(board):
        render(board)
        board = next_state(board)
    render(board)
