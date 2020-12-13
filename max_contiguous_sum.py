"""
Given a list of integers of any length, calculate the maximum
contiguous sum of all sub ranges.

For instance, given the list [1, -2, 3, 2, -1], the maximum
contiguous sum is 5, which is the sum of the sub range [3, 2].
"""

from puzzle_types import IntArray

def mcs_linear(nums: IntArray) -> int:
    """
    Calculate maximum contiguous sum for given sequence of integers.
    Complexity: O(n)
    """

    size: int = len(nums)
    if size == 0:
        return 0

    max_sum: int = nums[0]
    cur_sum: int = 0
    for i in range(size):
        cur_sum += nums[i]
        if cur_sum > max_sum:
            max_sum = cur_sum
        if cur_sum < 0:
            cur_sum = 0

    return max_sum

def mcs_quadratic(nums: IntArray) -> int:
    """
    Calculate maximum contiguous sum for given sequence of integers.
    Complexity: O(n^2)
    """

    size: int = len(nums)
    if size == 0:
        return 0

    max_sum: int = nums[0]
    for i in range(size):
        cur_sum: int = 0
        for j in range(i, size):
            cur_sum += nums[j]
            if cur_sum > max_sum:
                max_sum = cur_sum

    return max_sum

def test_mcs(nums: IntArray, mcs_actual: int) -> None:
    """
    Calculate maximum contiguous sum, using both linear and quadratic functions,
    and display actual and calculated maximums.
    """

    print("ListOfInts:", nums)
    print("MCS Actual:", mcs_actual)
    print("MCS Linear:", mcs_linear(nums))
    print("MCS Quadra:", mcs_quadratic(nums))

if __name__ == "__main__":
    test_mcs([1, -2, 3, 2, -1], 5)
    test_mcs([-3, 1, -2, 2, 3, 1, -5, 3, 2], 6)
    test_mcs([6, -5, -8, 9, 7, 10, 4, -3, 8, -5], 35)
