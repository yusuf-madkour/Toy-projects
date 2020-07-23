from argparse import ArgumentParser
from random import choices
from colorama import Fore, init
from copy import deepcopy
from time import sleep
import os
import platform


def random_state(width, length, prob):
    """
    Builds a board with all cells pseudo-randomly set. The board is
    represented as a list of lists throughout the script.

    Parameters
    ----------
    width: width of the board, in cells
    length: length of the board, in cells
    prob: probability of alive cells in the board

    Returns
    -------
    A board of dimension width x length with specific probability of alive cells in the board
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
        sleep(5)
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
    b = ''
    b += Fore.WHITE + '-' * (args.scale * len(board[0])+2) + '\n'
    for row in board:
        b += Fore.WHITE + '|'
        for c in row:
            if c == 1:
                b += Fore.CYAN + PC * args.scale
            else:
                b += Fore.MAGENTA + PC * args.scale
        b += Fore.WHITE + '|' + '\n'
    b += Fore.WHITE + '-' * (args.scale * len(board[0])+2) + '\n'
    print(b)


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
    ns = [[[] for _ in row] for row in board]
    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            if i > 0:
                ns[i][j].extend(board[i-1][max(0, j-1):j+2])
            if i < len(board)-1:
                ns[i][j].extend(board[i+1][max(0, j-1):j+2])
            if j > 0:
                ns[i][j].append(board[i][j-1])
            if j < len(board[i])-1:
                ns[i][j].append(board[i][j+1])
    return ns


def next_board_state(board):
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
    n = moore_neighbours(board)
    new_board = deepcopy(board)
    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            # Underpopulation or Overpopulation
            if n[i][j].count(1) in [0, 1] or n[i][j].count(1) > 3:
                new_board[i][j] = 0
                continue
            if n[i][j].count(1) == 3:  # Reproduction
                new_board[i][j] = 1
    return new_board


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
        '-w', '--width', help=txt['width'], type=int, default=30, metavar="")
    parser.add_argument(
        '-l', '--length', help=txt['length'], type=int, default=30, metavar="")
    parser.add_argument(
        '-sl', '--sleep', help=txt['sleep'], type=float, default=0, metavar="")
    parser.add_argument(
        '-pb', '--prob', help=txt['prob'], type=float, default=0.5, metavar="")
    parser.add_argument(
        '-p', '--pattern', help=txt['pattern'], type=str, metavar="")

    return parser.parse_args()


if __name__ == '__main__':
    init(autoreset=True)  # Initializing colorama

    args = parse_arguments()

    CLEAR_COMMAND = 'cls' if platform.system() == 'Windows' else 'clear'

    # Board initialization
    b = load_board_state(args.pattern) if args.pattern else random_state(
        args.width, args.length, args.prob)
    PC = '%'  # This is the Printed Character that represents a single cell
    while b != next_board_state(b):
        render(b)
        sleep(args.sleep)
        b = next_board_state(b)
        os.system(CLEAR_COMMAND)
    render(next_board_state(b))
