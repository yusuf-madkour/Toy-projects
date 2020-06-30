import argparse
from random import choices
from colorama import Fore, init
from copy import deepcopy
from time import sleep
from os import system


def random_state(width, length):
    """ TODO: Change the random generation process so that it operates on a
              threshold to favor dead over alive or alive over dead"""
    return [choices([0, 1], k=width, weights=[1-args.thresh, args.thresh]) for _ in range(length)]


def render(board):
    # TODO: Refactor function so that it prints the board in one go instead of row by row
    print(Fore.WHITE + '-' * (args.scale * len(board[0])+2))
    for row in board:
        print(Fore.WHITE + '|', end='')
        for c in row:
            if c == 1:
                print(Fore.GREEN + '#' * args.scale, end='')
            else:
                print(Fore.RED + '#' * args.scale, end='')
        print(Fore.WHITE + '|')
    print(Fore.WHITE + '-' * (args.scale * len(board[0])+2))


def find_neighbours(brd, i, j):
    """ TODO: Refactor the function so that it takes the whole board and 
             returns all the neighbours in one go"""
    ns = []
    if i > 0:
        ns += brd[i-1][max(0, j-1):j+2]
    if i < len(brd)-1:
        ns += brd[i+1][max(0, j-1):j+2]
    if j > 0:
        ns.append(brd[i][j-1])
    if j < len(brd[i])-1:
        ns.append(brd[i][j+1])
    return ns


def next_board_state(board):
    # TODO: apply changes made in the find_neighbours function here
    new_board = deepcopy(board)
    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            n = find_neighbours(board, i, j)
            # Underpopulation or Overpopulation
            if n.count(1) in [0, 1] or n.count(1) > 3:
                new_board[i][j] = 0
                continue
            if n.count(1) == 3:  # Reproduction
                new_board[i][j] = 1
    return new_board


text = {
    'general': 'This is my guided implementation of "Conway\'s Game of Life", guided by Robert Heaton.',
    'scale': 'scales the width of the board by given multiplier, scale value must be of type integer',
    'width': 'specify width of the board, must be integer',
    'length': 'specify length of the board, must be integer',
    'sleep': 'specify sleep time after every board render, values are expected to be float (in seconds)',
    'threshold': 'Favor alive state over dead, higher threshold results in higher probability of alive cells in the board'}

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
        '-sl', '--sleep', help=text['sleep'], type=float, default=0.1, metavar="")
    parser.add_argument(
        '-t', '--thresh', help=text['threshold'], type=float, default=0.5, metavar="")
    args = parser.parse_args()

    # Board initialization
    b = random_state(args.width, args.length)

    while not (b == next_board_state(b) or b == next_board_state(next_board_state(b))):
        sleep(args.sleep)
        render(b)
        b = next_board_state(b)
        system('cls')
    render(next_board_state(b))
    system('cls')
    render(next_board_state(b))
