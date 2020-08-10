import curses
import argparse
from copy import deepcopy
from random import choices

PC = "$"  # This is the Printed Character that represents a single cell


def random_state(width, length, prob):
    """
    Builds a board with the state of cells pseudo-randomly set.
    The board is represented as a list of lists throughout the script.

    Parameters
    ----------
    width: width of the board\n
    length: length of the board\n
    prob: probability of a cell being alive

    Returns
    -------
    A board of dimension width x length with specific probability of cells
    being alive
    """
    weights = [1 - prob, prob]
    return [choices([0, 1], k=width, weights=weights) for _ in range(length)]


def load_board_state(filepath):
    """
    Tries to load the initial state of a board from a text file where a dead
    cell is represented by 0 and a live cell is represented by 1.
    If the file does not exist, it returns a random board instead.

    Parameters
    ----------
    filepath: The path to the text file to load the board from

    Returns
    -------
    The board loaded from the text file represented as a list of lists
    """
    try:
        with open(filepath, mode="r") as f:
            lines = f.readlines()
            return [[int(c) for c in row.rstrip("\n")] for row in lines]
    except FileNotFoundError:
        args.pattern = False
        print("File does not exist")
        i = input("Would you like to use a random pattern instead?")
        if i in ["y", "Y", "Yes", "yes"]:
            return random_state(args.width, args.length, args.prob)
        else:
            exit()


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
    screen.clear()
    screen.addstr("=" * (args.scale * len(board[0]) + 2) + "\n", curses.A_BOLD)
    for row in board:
        screen.addstr("|", curses.A_BOLD)
        for c in row:
            if c == 1:
                screen.addstr(PC * args.scale, curses.color_pair(2))
            else:
                screen.addstr(PC * args.scale, curses.color_pair(1))
        screen.addstr("|" + "\n", curses.A_BOLD)
    screen.addstr("=" * (args.scale * len(board[0]) + 2) + "\n", curses.A_BOLD)
    screen.refresh()
    curses.napms(int(args.sleep * 1000))


def moore_neighbours(board):
    """
    Finds neighbours of each cell in the board

    Parameters
    ----------
    board: A list of lists representing the board state

    Returns
    -------
    Neighbours of all cells, it returns a list of lists with the same
    dimensions of the board but containing lists of neighbours instead of
    cell values
    """
    neighbours = [[[] for _ in row] for row in board]
    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            if i > 0:
                neighbours[i][j].extend(board[i - 1][max(0, j - 1) : j + 2])
            if i < len(board) - 1:
                neighbours[i][j].extend(board[i + 1][max(0, j - 1) : j + 2])
            if j > 0:
                neighbours[i][j].append(board[i][j - 1])
            if j < len(board[i]) - 1:
                neighbours[i][j].append(board[i][j + 1])
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
            underpopulation = neighbours[i][j].count(1) in [0, 1]
            overpopulation = neighbours[i][j].count(1) > 3
            if underpopulation or overpopulation:
                new_board[i][j] = 0
                continue
            if neighbours[i][j].count(1) == 3:  # Reproduction
                new_board[i][j] = 1
    return new_board


def prob(x):
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
        raise argparse.ArgumentTypeError("Probability should be between 0 and 1")
    return x


def parse_arguments():
    txt = {
        "general": 'This is my guided implementation of "Conway\'s \
                Game of Life", guided by Robert Heaton',
        "scale": "Scales the width of the board by given multiplier",
        "width": "The width of the board",
        "length": "The length of the board",
        "sleep": "Waiting time after each state render in seconds,\
                can be float",
        "proba": "Probability of each cell being alive",
        "pattern": "The path to a text file containing a 2d matrix\
                    of an initial state",
    }

    parser = argparse.ArgumentParser(description=txt["general"])

    parser.add_argument(
        "-sc", "--scale", help=txt["scale"], type=int, default=2, metavar=""
    )
    parser.add_argument(
        "-w", "--width", help=txt["width"], type=int, default=15, metavar=""
    )
    parser.add_argument(
        "-l", "--length", help=txt["length"], type=int, default=15, metavar=""
    )
    parser.add_argument(
        "-sl", "--sleep", help=txt["sleep"], default=0.1, type=float, metavar=""
    )
    parser.add_argument(
        "-pb", "--prob", help=txt["proba"], type=prob, default=0.3, metavar=""
    )
    parser.add_argument("-p", "--pattern", help=txt["pattern"], metavar="")
    return parser.parse_args()


def init_screen():
    """
    This function initializes the screen and prepares the colors for printing
    dead and live cells

    Parameters
    ----------
    None

    Returns
    -------
    curses screen object
    """
    screen = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.curs_set(0)
    return screen


def play(board, screen):
    """
    This function runs Conway's game of life

    Parameters
    ----------
    board: A list of lists representing the current board state\n
    screen: curses screen object

    Returns
    -------
    Nothing
    """
    while True:
        try:
            render(board)
        except curses.error:
            curses.endwin()
            print("Enlrage the terminal window or choose smaller dimensions")
            exit()
        # Run the game as long as the generated board is not repeating
        if (
            board in [next_state(board), next_state(next_state(board))]
            and not args.pattern
        ):
            break
        board = next_state(board)


if __name__ == "__main__":
    # Parsing script arguments
    args = parse_arguments()
    # Board initialization
    if args.pattern:
        board = load_board_state(args.pattern)
    else:
        board = random_state(args.width, args.length, args.prob)
    screen = init_screen()
    play(board, screen)
    screen.addstr("Press any character to exit...")
    screen.refresh()
    curses.curs_set(1)
    screen.getch()
    curses.endwin()
