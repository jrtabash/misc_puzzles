"""
The eight queens puzzle is the problem of placing eight chess queens on an 8×8 chessboard
so that no two queens threaten each other; thus, a solution requires that no two queens
share the same row, column, or diagonal.
  - Wikipedia

This program solves the 8 queens puzzle.
"""

from typing import Sequence, MutableSequence, Callable, Final

Row = MutableSequence[int]
Board = Sequence[Row]
NextIndexFtn = Callable[[int], int]

SIZE: Final = 8
SPACE: Final = 0
QUEEN: Final = 1

def make_board() -> Board:
    """
    Create an 8x8 empty chess board.
    """

    return [[SPACE for _ in range(SIZE)] for _ in range(SIZE)]

def print_board(board: Board) -> None:
    """
    Print chess board.
    """

    hsep = "-" + "----" * SIZE
    print(hsep)
    for row in board:
        line = "|"
        for cell in row:
            line += " Q |" if cell == QUEEN else "   |"
        print(line)
        print(hsep)

def can_place_queen(board: Board, row: int, col: int) -> bool:
    """
    Check if possible to place a queen on board at (row, col) location.
    """

    def can_diagonal(next_row: NextIndexFtn, next_col: NextIndexFtn) -> bool:
        i: int = next_row(row)
        j: int = next_col(col)
        while 0 <= i < SIZE and 0 <= j < SIZE:
            if board[i][j] == QUEEN:
                return False
            i = next_row(i)
            j = next_col(j)
        return True

    for idx in range(SIZE):
        if QUEEN in (board[idx][col], board[row][idx]):
            return False

    incr: NextIndexFtn = lambda idx: idx + 1
    decr: NextIndexFtn = lambda idx: idx - 1

    return (can_diagonal(decr, decr) and
            can_diagonal(incr, incr) and
            can_diagonal(decr, incr) and
            can_diagonal(incr, decr))

def place_queens(board: Board, row: int = 0) -> bool:
    """
    Recursively solve the 8 queens puzzle.
    """

    if row >= SIZE:
        return True

    for col in range(SIZE):
        if can_place_queen(board, row, col):
            board[row][col] = QUEEN
            if place_queens(board, row + 1):
                return True
            board[row][col] = SPACE

    return False

def solve_puzzle():
    """
    Solve 8 queens puzzle, and display result.
    """

    board = make_board()
    if place_queens(board):
        print_board(board)
    else:
        print("Failed to solve puzzle!")

if __name__ == "__main__":
    solve_puzzle()
