from random import choice
from colorama import Fore, init
import os
import platform
from time import sleep
from argparse import ArgumentParser


MAP_ = {'1': (0, 0), '2': (0, 1), '3': (0, 2),
        '4': (1, 0), '5': (1, 1), '6': (1, 2),
        '7': (2, 0), '8': (2, 1), '9': (2, 2)}

# Colorama colors used in rendering the board
CYAN = Fore.CYAN
RED = Fore.RED
GREEN = Fore.GREEN

WAIT = 0.2  # Wait time after each algorithm move
CLEAR_COMMAND = 'cls' if platform.system() == 'Windows' else 'clear'


def new_board():
    """
    Builds a new Tic Tac Toe board, where each position in the board is
    represented by a number.

    Parameters
    ----------
    None

    Returns
    -------
    A new game board as a list of lists, each list represents a row.
    """
    return [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]


def full_board(board):
    """
    Checks if the Tic Tac Toe board is full. Full in the sense that no legal
    moves are available.

    Parameters
    ----------
    board: game board

    Returns
    -------
    True if the board is full and false otherwise
    """
    return all([i in ['X', 'O'] for row in board for i in row])


def get_lines(board):
    """
    Retrieves the current state of all lines in the game board.

    Parameters
    ----------
    board: game board

    Returns
    -------
    A list of all lines in the board.
    """
    rows = [board[0], board[1], board[2]]
    columns = [[board[row][col] for row in range(3)] for col in range(3)]
    diagonals = [[board[0][0], board[1][1], board[2][2]]] +\
                [[board[0][2], board[1][1], board[2][0]]]
    return rows + columns + diagonals


def render(board):
    """
    Prints the board in terminal

    Parameters
    ----------
    board: game board

    Returns
    -------
    None
    """
    os.system(CLEAR_COMMAND)
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


def get_input(board, player):
    """
    Waits for the move from the human player, it will only return the move if
    it is a legal one.

    Parameters
    ----------
    board: game board
    player: current player (X or O)

    Returns
    -------
    Legal move
    """
    print(f"Player {player}, what is your move?")
    move = input()
    legal = [i for row in board for i in row if i not in ["X", "O"]]
    while move not in legal:
        render(board)
        print("Move is illegal, please try again.")
        print(f"Player {player}, what is your move?")
        move = input()
    return move


def human_player(board, player):
    """
    Accepts current board state and current player and returns the coordinates
    of the move chosen by a human player.

    Parameters
    ----------
    board: game board
    player: current player (X or O)

    Returns
    -------
    Board coordinates of chosen move.
    """
    move = get_input(board, player)
    coord = MAP_[move]
    return coord


def finds_winning_and_losing_moves_ai(board, player):
    """
    Returns the coordinates of a move based on the following priorities:
    1- Winning move
    2- Blocking move
    3- Random legal move

    Parameters
    ----------
    board: game board
    player: current player (X or O)

    Returns
    -------
    Board coordinates of chosen move.
    """
    lines = get_lines(board)
    opponent = 'X' if player == 'O' else 'O'
    for line in lines:
        if line.count(player) == 2 and line.count(opponent) == 0:
            [winning_move] = [i for i in line if i != player]
            return MAP_[winning_move]
    for line in lines:
        if line.count(opponent) == 2 and line.count(player) == 0:
            [blocking_move] = [i for i in line if i != opponent]
            return MAP_[blocking_move]
    return random_ai(board, player)


def finds_winning_moves_ai(board, player):
    """
    Returns the coordinates of a winning move if available. It returns a random
    legal move if there is no winning move avaialable.

    Parameters
    ----------
    board: game board
    player: current player (X or O)

    Returns
    -------
    Board coordinates of chosen move.
    """
    lines = get_lines(board)
    for line in lines:
        if line.count(player) == 2 and any(i.isnumeric() for i in line):
            [winning_move] = [i for i in line if i.isnumeric()]
            return MAP_[winning_move]
    return random_ai(board, player)


def random_ai(board, player):
    """
    Checks for legal moves in the board and randomly returns
    the coordinates of one of them.

    Parameters
    ----------
    board: game board
    player: current player (X or O)

    Returns
    -------
    Board coordinates of chosen move.
    """
    legal = [i for row in board for i in row if i not in ["X", "O"]]
    return MAP_[choice(legal)]


def make_move(board, coord, player):
    """
    Updates the board state with the legal move chosen by the player.

    Parameters
    ----------
    board: game board
    coord: coordinates of the chosen move
    player: current player (X or O)

    Returns
    -------
    The updated game board
    """
    board[coord[0]][coord[1]] = player
    return board


def get_winner(board):
    """
    Scans the board for a winner.

    Parameters
    ----------
    board: game board

    Returns
    -------
    The winner if there is one or None if there is no winner
    """
    lines = get_lines(board)
    for line in lines:
        if all(i == 'X' for i in line):
            return 'X'
        if all(i == 'O' for i in line):
            return 'O'
    return None


def parse_arguments():
    """
    Parses the arguments from CLI

    Parameters
    ----------
    None

    Returns
    -------
    Parsed arguments
    """
    parser = ArgumentParser(
        description='A Tic Tac Toe game that can be played in terminal in\
                     2player mode, 1player mode or you can sit back and watch\
                     2 algorithms play against each other. Strategy options\
                     are: "human", "0", "1" and "2". The numbers 0 through 2\
                     represent the sophistication level of the algorithm.')
    parser.add_argument('-o', '--playerO', choices=strategies, metavar="",
                        help='Choose strategy of player O')
    parser.add_argument('-x', '--playerX', choices=strategies, metavar="",
                        help='Choose strategy of player X')
    return parser.parse_args()


def play(x, o):
    """
    Runs a full Tic Tac Toe game

    Parameters
    ----------
    x: A function representing player x
    o: A function representing player o
    Each of the two functions above should accept board state and current
    player and return the coordinates of a legal move.

    Returns
    -------
    The outcome of the game
    """
    players = {'X': x, 'O': o}
    # Randomly choose who plays first
    current_player = choice(list(players.keys()))
    board = new_board()
    while True:
        render(board)
        coords = players[current_player](board, current_player)
        if players[current_player] != human_player:
            sleep(WAIT)
        board = make_move(board, coords, current_player)
        render(board)
        if get_winner(board):
            return current_player
        if full_board(board):
            return 'Draw'
        current_player = 'O' if current_player == 'X' else 'X'


if __name__ == "__main__":
    init(autoreset=True)  # Initializing Colorama

    strategies = {'human': human_player, '0': random_ai,
                  '1': finds_winning_moves_ai,
                  '2': finds_winning_and_losing_moves_ai}
    args = parse_arguments()
    x = strategies[args.playerX]
    o = strategies[args.playerO]

    result = play(x, o)
    print(result) if result == 'Draw' else print(f"{result} wins")
