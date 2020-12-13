"""
Given an integer N, calculate the unique number of ways
you can climb a staircase with N steps if you can climb
1, 2 or 3 steps at a time.

For instance, if N=3, then there are 4 unique ways to
climb the staircase, as shown below:

1 1 1
1 2
2 1
3

"""

from puzzle_types import IntMap

def count_steps(nsteps: int) -> int:
    """
    Calculate unique number of ways to climb a staircase of
    size nsteps if one can climb 1, 2 or 3 steps at a time.
    """

    counts: IntMap = {1: 1, 2: 2, 3: 4}
    max_key: int = 3

    if nsteps > max_key:
        for i in range(4, nsteps + 1):
            counts[i] = counts[i - 1] + counts[i - 2] + counts[i - 3]
            max_key = i

    return counts[nsteps]

def test_steps() -> None:
    """
    Test count_steps function.
    """

    def test(nsteps: int, actual: int) -> None:
        uniq_cnt: int = count_steps(nsteps)
        print(f"N={nsteps} count={uniq_cnt} actual={actual}")

    test(1, 1)
    test(2, 2)
    test(3, 4)
    test(4, 7)
    test(5, 13)
    test(6, 24)

if __name__ == "__main__":
    test_steps()
