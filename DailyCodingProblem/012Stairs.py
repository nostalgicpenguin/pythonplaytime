# This problem was asked by Amazon.
# There exists a staircase with N steps, and you can climb up either 1 or 2
# steps at a time.
# Given N, write a function that returns the number of unique ways you can
# climb the staircase.
# The order of the steps matters.
#
# For example, if N is 4, then there are 5 unique ways:
# •	1, 1, 1, 1
# •	2, 1, 1
# •	1, 2, 1
# •	1, 1, 2
# •	2, 2
# What if, instead of being able to climb 1 or 2 steps at a time, you could
# climb any number from a
# set of positive integers X? For example, if X = {1, 3, 5}, you could climb
# 1, 3, or 5 steps at a time.


# Unique sets:
# N = 2: (1, 1), (2)
# N = 3: (1, 1, 1), (1, 2)
# N = 4: (1, 1, 1, 1) (1, 1, 2) (2, 2)
import unittest
from math import factorial
from collections import Counter


def get_unique_sets(N):
    """
    Return a list of the possible sets of 1s and 2s which sum to N
    Note that there is only one ordering given for each set.
    Each set is returned as a Counter object
    """
    unique_sets = []
    num_ones = N

    while(num_ones >= 0):
        num_twos = int((N-num_ones)/2)
        new_set = Counter({'1': num_ones, '2': num_twos})

        # Assure the 1s and 2s sum to N
        assert (sum(int(i) for i in new_set.elements()) == N)
        unique_sets.append(new_set)
        num_ones -= 2
        yield new_set


def num_different_arrangements(unique_set):
    """
    Given a set such as [1, 1, 1, 1, 1, 2, 2], return the number of unique
    arrangements
    :param unique_set:
    :return: int
    """

    n = len(sorted(unique_set.elements()))
    r = unique_set['1']
    return int(factorial(n) / (factorial(r) * factorial(n - r)))


def get_number_of_unique_ways(N):
    num_unique_ways = 0
    for unique_set in get_unique_sets(N):
        num_arrangements_for_set \
            = num_different_arrangements(unique_set)
        num_unique_ways += num_arrangements_for_set

    print("N = {}, Number of unique ways of climbing stairs = {}"
          .format(N, num_unique_ways))
    return num_unique_ways


class SimpleTest(unittest.TestCase):

    def test_stairs(self):
        self.assertEqual(1, get_number_of_unique_ways(1))
        self.assertEqual(2, get_number_of_unique_ways(2))
        self.assertEqual(3, get_number_of_unique_ways(3))
        self.assertEqual(5, get_number_of_unique_ways(4))
        self.assertEqual(8, get_number_of_unique_ways(5))
        self.assertEqual(13, get_number_of_unique_ways(6))


if __name__ == "__main__":
    unittest.main()  # run all tests
