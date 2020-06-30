import argparse
from random import choices, seed
from colorama import Fore, init
from copy import deepcopy
from time import sleep
from os import system

seed(42)

def random_state(width, length):
    return [choices([0, 1], k=width, weights=[1-args.thresh, args.thresh]) for _ in range(length)]


def render(board):
    b = ''
    b += Fore.WHITE + '-' * (args.scale * len(board[0])+2) + '\n'
    for row in board:
        b += Fore.WHITE + '|'
        for c in row:
            if c == 1:
                b += Fore.GREEN + '#' * args.scale
            else:
                b += Fore.RED + '#' * args.scale
        b += Fore.WHITE + '|' + '\n'
    b += Fore.WHITE + '-' * (args.scale * len(board[0])+2) + '\n'
    print(b)

def find_neighbours(brd):
    ns = [[[] for cell in row] for row in brd]
    for i, row in enumerate(brd):
        for j, _ in enumerate(row):
            if i > 0:
                ns[i][j].extend(brd[i-1][max(0, j-1):j+2])
            if i < len(brd)-1:
                ns[i][j].extend(brd[i+1][max(0, j-1):j+2])
            if j > 0:
                ns[i][j].append(brd[i][j-1])
            if j < len(brd[i])-1:
                ns[i][j].append(brd[i][j+1])
    return ns

def next_board_state(board):
    n = find_neighbours(board)
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
    'threshold': 'Higher threshold results in higher probability of alive cells in the board'}

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
        '-sl', '--sleep', help=text['sleep'], type=float, default=0.3, metavar="")
    parser.add_argument(
        '-t', '--thresh', help=text['threshold'], type=float, default=0.5, metavar="")
    args = parser.parse_args()

    # Board initialization
    b = random_state(args.width, args.length)
    i = 0
    while not (b == next_board_state(b) or b == next_board_state(next_board_state(b))):
        render(b)
        sleep(args.sleep)
        b = next_board_state(b)
        # system('cls')
        i += 1
        if i == 3: break
    # render(next_board_state(b))
    # system('cls')
    # render(next_board_state(b))

