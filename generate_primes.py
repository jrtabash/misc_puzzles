"""
Given an integer N, generate all primes less
than or equal to N.
"""

import math
from puzzle_types import IntArray, IntGenerator

def is_multiple_of(primes: IntArray, num: int) -> bool:
    """
    Check if given num is a multiple of any of the given primes.
    Assumes primes sorted in increasing order.
    """

    sqrt_num: int = math.ceil(math.sqrt(num))
    for prime in primes:
        if prime > sqrt_num:
            break
        if num % prime == 0:
            return True
    return False

def generate_primes(max_int: int) -> IntGenerator:
    """
    Generate primes up to a maximum specified integer.
    """

    if max_int >= 2:
        yield 2

        cur_int: int = 1
        primes: IntArray = []

        while (cur_int := cur_int + 2) <= max_int:
            if is_multiple_of(primes, cur_int):
                continue
            primes.append(cur_int)
            yield cur_int

def test_generate() -> None:
    """
    Generate all primes between 1 and 100.
    """

    for prime in generate_primes(100):
        print(prime)

if __name__ == "__main__":
    test_generate()
