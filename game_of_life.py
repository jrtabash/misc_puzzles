"""
The Game of Life, also known simply as Life, is a cellular automaton
devised by the British mathematician John Horton Conway in 1970.
  - Wikipedia

This program simulates game of life.
"""

import sys
import os
from time import sleep
from typing import MutableSequence, Sequence, Final, Optional

Row = MutableSequence[int]
Grid = Sequence[Row]

SIZE: Final = 32
ON: Final = 1
OFF: Final = 0

def make_grid() -> Grid:
    """
    Create game of life grid.
    """

    return [[OFF for _ in range(SIZE)] for _ in range(SIZE)]

def init_grid(grid: Grid) -> None:
    """
    Set initial live cells.
    """

    for i, j in [(5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16),
                 (6, 10), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16),
                 (7, 11), (7, 12), (7, 13), (7, 14), (7, 15),
                 (8, 11), (8, 12), (8, 13), (8, 14), (8, 15),
                 (9, 12), (9, 13), (9, 14),
                 (10, 12), (10, 13), (10, 14),
                 (11, 12), (11, 13), (11, 14),
                 (12, 12), (12, 13), (12, 14)]:
        grid[i][j] = ON

def print_grid(grid: Grid, gen: Optional[int] = None) -> None:
    """
    Print game of life grid.
    """

    os.system("clear")

    for row in grid:
        for cell in row:
            sys.stdout.write('o' if cell == ON else '.')
        sys.stdout.write('\n')

    if gen is not None:
        sys.stdout.write(f"Generation: {gen}\n")

def count_neighbors(grid: Grid, i: int, j: int) -> int:
    """
    Calculate the number of live cells around grid[i][j] neighbors.
    """

    def check_and_count(ni: int, nj: int) -> int:
        if 0 <= ni < SIZE and 0 <= nj < SIZE:
            if grid[ni][nj] == ON:
                return 1
        return 0

    count: int = 0

    count += check_and_count(i, j - 1)
    count += check_and_count(i, j + 1)

    count += check_and_count(i - 1, j)
    count += check_and_count(i - 1, j - 1)
    count += check_and_count(i - 1, j + 1)

    count += check_and_count(i + 1, j)
    count += check_and_count(i + 1, j - 1)
    count += check_and_count(i + 1, j + 1)

    return count

def next_cell(grid: Grid, i: int, j: int) -> int:
    """
    Calculate next generation cell value for grid[i][j].
    This function encodes game of life transition rules.
    """

    live_neighbors: int = count_neighbors(grid, i, j)
    if grid[i][j] == ON and live_neighbors in (2, 3):
        return ON
    if grid[i][j] == OFF and live_neighbors == 3:
        return ON
    return OFF

def next_generation(grid: Grid) -> Grid:
    """
    Calculate next generation grid.
    """

    next_grid = make_grid()
    for i in range(SIZE):
        for j in range(SIZE):
            next_grid[i][j] = next_cell(grid, i, j)
    return next_grid

def simulate_game(ngen: int, delay: float = 0.5) -> None:
    """
    Simulate game of life ngen generations.
    """

    grid = make_grid()
    init_grid(grid)
    print_grid(grid, 0)
    sleep(delay)

    for gen in range(1, ngen + 1):
        grid = next_generation(grid)
        print_grid(grid, gen)
        sleep(delay)

if __name__ == "__main__":
    simulate_game(30)
