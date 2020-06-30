import argparse
from random import choices
from colorama import Fore, init
from copy import deepcopy
from time import sleep
from os import system


def random_state(width, length):
    return [choices([0, 1], k=width, weights=[1-args.thresh, args.thresh]) for _ in range(length)]


def load_board_state(filename):
    try:
        with open('../patterns/' + filename, mode='r') as f:
            return [[int(c) for c in row.rstrip('\n')] for row in f.readlines()]
    except:
        print("File does not exist, generating a random pattern...")
        sleep(5)
        return random_state(args.width, args.length)

def render(board):
    b = ''
    b += Fore.WHITE + '-' * (args.scale * len(board[0])+2) + '\n'
    for row in board:
        b += Fore.WHITE + '|'
        for c in row:
            if c == 1:
                b += Fore.CYAN + pc * args.scale
            else:
                b += Fore.MAGENTA + pc * args.scale
        b += Fore.WHITE + '|' + '\n'
    b += Fore.WHITE + '-' * (args.scale * len(board[0])+2) + '\n'
    print(b)


def moore_neighbours(board):
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


text = {
    'general': 'This is my guided implementation of "Conway\'s Game of Life", guided by Robert Heaton.',
    'scale': 'scales the width of the board by given multiplier, scale value must be of type integer',
    'width': 'specify width of the board, must be integer',
    'length': 'specify length of the board, must be integer',
    'sleep': 'specify sleep time after every board render, values are expected to be float (in seconds)',
    'threshold': 'Higher threshold results in higher probability of alive cells in the board',
    'pattern': 'pass the name of a text file that holds a 2d matrix of an initial state, file must be in patterns folder'}

if __name__ == '__main__':
    init()  # Initializing colorama

    # Command line arguments' parsing
    parser = argparse.ArgumentParser(description=text['general'])
    parser.add_argument(
        '-sc', '--scale', help=text['scale'], type=int, default=2, metavar="")
    parser.add_argument(
        '-w', '--width', help=text['width'], type=int, default=30, metavar="")
    parser.add_argument(
        '-l', '--length', help=text['length'], type=int, default=30, metavar="")
    parser.add_argument(
        '-sl', '--sleep', help=text['sleep'], type=float, default=0.01, metavar="")
    parser.add_argument(
        '-t', '--thresh', help=text['threshold'], type=float, default=0.5, metavar="")
    parser.add_argument(
        '-p', '--pattern', help=text['pattern'], type=str, metavar="")
    args = parser.parse_args()

    # Board initialization
    b = load_board_state(args.pattern) if args.pattern else random_state(args.width, args.length)
    pc = '%'
    while b != next_board_state(b):
        render(b)
        sleep(args.sleep)
        b = next_board_state(b)
        system('cls')
    render(next_board_state(b))