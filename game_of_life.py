"""
The Game of Life, also known simply as Life, is a cellular automaton
devised by the British mathematician John Horton Conway in 1970.
  - Wikipedia

This program simulates game of life.
"""

import sys
import os
import random
import time
from puzzle_types import Grid, OptIntPair, Final

SIZE: Final = 48
ON: Final = 1
OFF: Final = 0

FUNNEL: Final = 1
DIAMOND: Final = 2
XCROSS: Final = 3

def make_grid() -> Grid:
    """
    Create game of life grid.
    """

    return [[OFF for _ in range(SIZE)] for _ in range(SIZE)]

def init_grid(grid: Grid) -> None:
    """
    Set initial live cells.
    """

    which: Final = random.choice([FUNNEL, DIAMOND, XCROSS])
    if which == FUNNEL:
        for i, j in [(5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16),
                     (6, 10), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16),
                     (7, 11), (7, 12), (7, 13), (7, 14), (7, 15),
                     (8, 11), (8, 12), (8, 13), (8, 14), (8, 15),
                     (9, 12), (9, 13), (9, 14),
                     (10, 12), (10, 13), (10, 14),
                     (11, 12), (11, 13), (11, 14),
                     (12, 12), (12, 13), (12, 14)]:
            grid[i][j] = ON
    elif which == DIAMOND:
        for i, j in [(11, 15), (11, 16),
                     (12, 13), (12, 14), (12, 17), (12, 18),
                     (13, 11), (13, 12), (13, 19), (13, 20),
                     (14, 9), (14, 10), (14, 21), (14, 22),
                     (15, 9), (15, 10), (15, 21), (15, 22),
                     (16, 11), (16, 12), (16, 19), (16, 20),
                     (17, 13), (17, 14), (17, 17), (17, 18),
                     (18, 15), (18, 16)]:
            grid[i][j] = ON
    elif which == XCROSS:
        for i, j in [(16, 8), (16, 9), (16, 10), (16, 20), (16, 21), (16, 22),
                     (17, 10), (18, 10), (18, 20), (17, 20),
                     (18, 11), (18, 12), (18, 18), (18, 19),
                     (19, 12), (20, 12), (20, 18), (19, 18),
                     (20, 13), (20, 14), (20, 16), (20, 17),
                     (21, 14), (22, 14), (22, 16), (21, 16),
                     (22, 15), (22, 16), (23, 14), (24, 14),
                     (23, 16), (24, 16), (24, 13), (24, 12),
                     (24, 17), (24, 18), (25, 12), (26, 12),
                     (25, 18), (26, 18), (26, 11), (26, 10),
                     (26, 19), (26, 20), (27, 10), (28, 10),
                     (27, 20), (28, 20), (28, 9), (28, 8),
                     (28, 21), (28, 21), (28, 22)]:
            grid[i][j] = ON


def print_grid(grid: Grid, gen_info: OptIntPair = None) -> None:
    """
    Print game of life grid.
    """

    os.system("clear")

    for row in grid:
        for cell in row:
            sys.stdout.write('o' if cell == ON else '.')
        sys.stdout.write('\n')

    if gen_info:
        sys.stdout.write(f"Generation: {gen_info[0]}/{gen_info[1]}\n")

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
    print_grid(grid, (0, ngen))
    time.sleep(max(delay, 2.0))

    for gen in range(1, ngen + 1):
        grid = next_generation(grid)
        print_grid(grid, (gen, ngen))
        time.sleep(delay)

if __name__ == "__main__":
    random.seed(int(time.time()))
    simulate_game(random.randint(20, 50))
