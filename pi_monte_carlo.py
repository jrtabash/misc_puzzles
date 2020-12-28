"""
Use Monte Carlo method to estimate the value
of pi.

To estimate the value of pi, put a circle of
radius r in a square with side length 2r.
The area of the square is 4r^2.

Generate N random (x, y) points, and count
the number of points that are inside the
circle, call this count Nc. Then we can
estimate the area of the circle as Fc * 4r^2,
where Fc = Nc / N.

Finally, utilize the area of the cirle equation,
A = pi * r^2, and substitate Fc * 4r^2 for A.
This yields Fc * 4r^2 = pi * r^2, which reduces
to pi = 4 * Fc.

Implementation will assume r = 1.
"""

import math
import random
from typing import Tuple

Point = Tuple[float, float]

def next_point() -> Point:
    """
    Generate and return a random (x, y) point, with
    both x and y in range [0.0, 2.0)
    """

    def next_coord() -> float:
        return 2.0 * random.random()

    return next_coord(), next_coord()

def in_unit_circle(pt: Point) -> bool:
    """
    Check if point is unit circle centered at (1.0, 1.0)
    """

    return math.sqrt((pt[0] - 1.0)**2 + (pt[1] - 1.0)**2) <= 1.0

def estimate_pi(samples: int = 1000000,
                experiments: int = 1,
                verbose: bool = False) -> float:
    """
    Estimate value of Pi using Monte Carlo method.

    samples: Number of random points to sample per experiment
    experiments: Number of experiments to perform

    Return: Average of all experiments
    """

    pi_sum: float = 0.0

    for sim in range(1, experiments + 1):
        in_circle_cnt: int = 0

        for _ in range(samples):
            if in_unit_circle(next_point()):
                in_circle_cnt += 1

        pi_estimate = 4.0 * in_circle_cnt / float(samples)
        pi_sum += pi_estimate

        if verbose:
            print(f"Sim {sim}: estimate {pi_estimate}")

    return pi_sum / float(experiments)

def test_pi() -> None:
    """
    Test Monte Carlo pi estimator
    """

    pi = estimate_pi(samples=1000000, experiments=100, verbose=True)
    err = abs(math.pi - pi)
    print(f"\nPi = {pi}\nEr = {err}")

if __name__ == "__main__":
    test_pi()
