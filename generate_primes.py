"""
Given an integer N, generate all primes less
than or equal to N.
"""

import sys
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

def test_generate(to_num: int) -> None:
    """
    Generate all primes between 1 and to_num.
    """

    for prime in generate_primes(to_num):
        print(prime)

def get_to_num() -> int:
    """
    Read and return to_num value from argv if specified,
    return 100 otherwise.
    """

    to_num = 100
    if len(sys.argv) >= 2:
        to_num = int(sys.argv[1])
    return to_num

if __name__ == "__main__":
    test_generate(get_to_num())
