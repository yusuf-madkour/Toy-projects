from random import choice
from colorama import Fore, init
from os import system
from time import sleep
import argparse

map_ = {'1': (0, 0), '2': (0, 1), '3': (0, 2),
        '4': (1, 0), '5': (1, 1), '6': (1, 2),
        '7': (2, 0), '8': (2, 1), '9': (2, 2)}

# Colorama colors used in rendering the board
CYAN = Fore.CYAN
RED = Fore.RED
GREEN = Fore.GREEN

WAIT = 0.2  # Wait time after each algorithm move


def new_board():
    return [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]


def full_board(board):
    return all([i in ['X', 'O'] for row in board for i in row])


def get_lines(board):
    return [
        board[0], board[1], board[2],             # All rows
        [board[0][0], board[1][0], board[2][0]],  # First column
        [board[0][1], board[1][1], board[2][1]],  # Second column
        [board[0][2], board[1][2], board[2][2]],  # Third column
        [board[0][0], board[1][1], board[2][2]],  # First diagonal
        [board[0][2], board[1][1], board[2][0]]   # Second diagonal
    ]


def render(board):
    print(CYAN + '+-----+')
    for row in board:
        print(CYAN + '|', end='')
        for i, c in enumerate(row):
            if c == 'X':
                print(RED + 'X', end='')
            elif c == 'O':
                print(GREEN + 'O', end='')
            else:
                print(c, end='')
            if i != 2:
                print(' ', end="")
        print(CYAN + '|')
    print(CYAN + '+-----+')


def human_player(board, player):
    render(board)
    print(f"Player {player}, what is your move?")
    n = input()
    while n not in map_:
        render(board)
        print("Input must be a number between 1 and 9, please try again.")
        print(f"Player {player}, what is your move?")
        n = input()
    return map_[n]


def finds_winning_and_losing_moves_ai(board, player):
    lines = get_lines(board)
    enemy = 'X' if player == 'O' else 'O'
    for line in lines:
        if line.count(player) == 2 and line.count(enemy) == 0:
            [winning_move] = [i for i in line if i != player]
            return map_[winning_move]
    for line in lines:
        if line.count(enemy) == 2 and line.count(player) == 0:
            [blocking_move] = [i for i in line if i != enemy]
            return map_[blocking_move]
    return random_ai(board, player)


def finds_winning_moves_ai(board, player):
    lines = get_lines(board)
    for line in lines:
        if line.count(player) == 2 and any(i.isnumeric() for i in line):
            [winning_move] = [i for i in line if i.isnumeric()]
            return map_[winning_move]
    return random_ai(board, player)


def random_ai(board, player):
    legal = [i for row in board for i in row if i not in ["X", "O"]]
    return map_[choice(legal)]


def make_move(board, coord, player):
    while board[coord[0]][coord[1]] in ['X', 'O']:
        render(board)
        print('Cell already full, please try again.')
        coord = human_player(board, player)
    board[coord[0]][coord[1]] = player
    render(board)
    return board


def get_winner(board):
    lines = get_lines(board)
    for line in lines:
        if all(i == 'X' for i in line):
            return 'X'
        if all(i == 'O' for i in line):
            return 'O'
    return None


def parse_arguments():
    parser = argparse.ArgumentParser(description='A Tic Tac Toe game that can be played in terminal in 2-player mode,\
                                                  1-player mode or you can sit back and watch 2 algorithms play against each other.\
                                                  Player options are: human, 0, 1 and 2. The numbers 0 through 2 represent the sophistication\
                                                  level of algorithm.')
    parser.add_argument('-o', '--playerO', type=str, metavar="",
                        help='Choose strategy of player O')
    parser.add_argument('-x', '--playerX', type=str, metavar="",
                        help='Choose strategy of player X')
    return parser.parse_args()


def play(x, o):
    player = choice(['X', 'O'])  # Randomly choose who plays first
    board = new_board()
    while True:
        if player == 'O':
            sleep(WAIT)
            coords = o(board, player)
        else:
            sleep(WAIT)
            coords = x(board, player)
        board = make_move(board, coords, player)
        if get_winner(board):
            return player
        if full_board(board):
            return 'Draw'
        player = 'O' if player == 'X' else 'X'


if __name__ == "__main__":
    init(autoreset=True)  # Initializing Colorama

    players = {'human': human_player, '0': random_ai, '1': finds_winning_moves_ai,
               '2': finds_winning_and_losing_moves_ai}
    args = parse_arguments()
    x = players.get(args.playerX, random_ai)
    o = players.get(args.playerO, finds_winning_and_losing_moves_ai)

    result = play(x, o)
    print(result) if result == 'Draw' else print(f"{result} wins")
