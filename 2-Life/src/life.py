from random import choices
from colorama import Fore, init
from copy import deepcopy
from time import sleep
from os import system

def random_state(width, height):
    """TODO: Change the random generation process so that it operates on a
            threshold to favor dead over alive or alive over dead"""
    return [choices([0, 1], k = width) for _ in range(height)]

def render(board):
    print(Fore.WHITE + '-' * (scale * len(board[0])+2))
    for row in board:
        print(Fore.WHITE + '|', end='')
        for c in row:
            if c == 1:
                print(Fore.GREEN + '#' * scale, end='')
            else:
                print(Fore.RED + '#' * scale, end='')
        print(Fore.WHITE + '|')
    print(Fore.WHITE + '-' * (scale * len(board[0])+2))

def find_neighbours(brd, i, j):
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
    new_board = deepcopy(board)
    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            n = find_neighbours(board, i, j)
            if n.count(1) in [0,1] or n.count(1) > 3: # Underpopulation or Overpopulation
                new_board[i][j] = 0
                continue
            if n.count(1) == 3: # Reproduction
                new_board[i][j] = 1
    return new_board

if __name__ == '__main__':
    init() # Initializing colorama
    scale = 2
    b = random_state(20, 15)
    while True:
        system('cls')
        render(b)
        b = next_board_state(b)
        if b == next_board_state(b) or b == next_board_state(next_board_state(b)):
            system('cls')
            render(next_board_state(b))
            system('cls')
            render(next_board_state(b))
            break
