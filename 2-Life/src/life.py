from random import choices
from colorama import Fore, init
from copy import deepcopy
from time import sleep

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
        for j, c in enumerate(row):
            neighbours = find_neighbours(board, i, j)
            if neighbours.count(1) in [0,1]: # Underpopulation
                new_board[i][j] = 0
                continue
            if neighbours.count(1) > 3: # Overpopulation
                new_board[i][j] = 0
                continue
            if neighbours.count(1) == 3 and c == 0: # Reproduction
                new_board[i][j] = 1
    return new_board

if __name__ == '__main__':
    init() # Initializing colorama
    scale = 2
    b = random_state(20, 15)
    while True:
        render(b)
        b = next_board_state(b)
        sleep(0.3)
        if b == next_board_state(b) or b == next_board_state(next_board_state(b)):
            render(next_board_state(b))
            render(next_board_state(b))
            break
