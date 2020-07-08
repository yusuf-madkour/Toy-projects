from random import choice

def new_board():
    return [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def render(board):
    print('-------')
    for row in board:
        print('|', end="")
        print(*row, sep=' ', end='')
        print('|')
    print('-------')


def get_move(board):
    maps = {'1': (0, 0), '2': (0, 1), '3': (0, 2),
            '4': (1, 0), '5': (1, 1), '6': (1, 2),
            '7': (2, 0), '8': (2, 1), '9': (2, 2)}
    render(board)
    n = input()
    while n not in list(maps.keys()):
        print("Input must be a number between 1 and 9, please try again.")
        n = input()
    return maps[n]


def make_move(board, coord, player):
    while board[coord[0]][coord[1]] in ['X', 'O']:
        print('Cell already full, please try again.')
        coord = get_move(board)
    board[coord[0]][coord[1]] = player
    render(board)
    return board


def full_board(board):
    return all([i in ['X', 'O'] for row in board for i in row])


def get_winner(board):
    lines = [
             board[0], board[1], board[2],             # All rows
             [board[0][0], board[1][0], board[2][0]],  # First column
             [board[0][1], board[1][1], board[2][1]],  # Second column
             [board[0][2], board[1][2], board[2][2]],  # Third column
             [board[0][0], board[1][1], board[2][2]],  # First diagonal
             [board[0][2], board[1][1], board[2][0]]   # Second diagonal
             ]
    for line in lines:
        if all(i == 'X' for i in line):
            return 'X'
        if all(i == 'O' for i in line):
            return 'O'
    return None


if __name__ == "__main__":
    player = choice(['O', 'X'])
    board = new_board()
    while True:
        print(f"Player {player}, what is your move?")
        coords = get_move(board)
        board = make_move(board, coords, player)
        if get_winner(board):
            print(f"Player {get_winner(board)} is the champion")
            break
        if full_board(board):
            print('We have a draw')
            break
        player = 'O' if player == 'X' else 'X'
