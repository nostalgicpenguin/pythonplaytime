# Daily Coding Problem 002:
#
# Given an array of integers, return a new array such that each element at
# index i of the new array is the product of all the numbers in the original
# array except the one at i.
# For example, if our input was [1, 2, 3, 4, 5], the expected output would
# be [120, 60, 40, 30, 24].
# If our input was [3, 2, 1], the expected output would be [2, 3, 6].
#
# Follow-up: what if you can't use division?

import unittest


def product_of_all_except_k(arr, k):
    """ Given an array and an index k, return the product of all entries
        in the array, excluding the entry at k
    """

    prod = 1
    for i in arr[:k] + arr[k+1:]:
        prod *= i
    return prod


def product_of_array(arr):
    """ Given an array, return a new array where each entry at index i is
        the product of the all the entries in the original array except
        the one at i
        """

    result = []
    for i, j in enumerate(arr):
        result.append(product_of_all_except_k(arr, i))

    return result


class SimpleTest(unittest.TestCase):
    """ Basic tests for product_of_array """

    def test_product_of_array(self):
        """Test test_product_of_array"""

        self.assertEqual(product_of_array([3, 2, 1]),
                         [2, 3, 6]
                         )

        self.assertEqual(product_of_array([1, 2, 3, 4, 5]),
                         [120, 60, 40, 30, 24]
                         )
