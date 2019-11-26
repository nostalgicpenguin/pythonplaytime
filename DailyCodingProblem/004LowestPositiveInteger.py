# This problem was asked by Stripe.
# Given an array of integers, find the first missing positive integer in
# linear time and constant space.
# In other words, find the lowest positive integer that does not exist in
# the array.
# The array can contain duplicates and negative numbers as well.
# For example:
# the input [3, 4, -1, 1] should give 2
# the input [1, 2, 0] should give 3
# You can modify the input array in-place.

import unittest


def swap(arr, idx1, idx2):
    for idx in [idx1, idx2]:
        assert(idx >= 0 and idx < len(arr))
    arr[idx1], arr[idx2] = arr[idx2], arr[idx1]


def move_non_positive_values_to_front(arr):

    # Move all non-positive (<=0) numbers to the start of the array
    num_zero_or_less = 0
    for i in range(len(arr)):
        if arr[i] <= 0 and i > num_zero_or_less:
            # this is negative, swap it
            swap(arr, i, num_zero_or_less)
            num_zero_or_less += 1

    return num_zero_or_less


def lowest_positive_integer_not_in_array(arr):

    print('Original array: {}'.format(arr))
    # First move all non-positive (<=0) numbers to the start of the array
    idx_of_first_positive = move_non_positive_values_to_front(arr)

    print('Segregated array: {}, idx of first positive val: {}'
          .format(arr,
                  idx_of_first_positive))

    # Now for all positive elements (at index >= num_zero_or_less), iterate
    # over the array and for each value, v, mark the value at index v
    # as negative (if it exists within the bounds of the array)

    for idx in range(idx_of_first_positive, len(arr)):
        val = abs(arr[idx])
        if idx_of_first_positive + val - 1 < len(arr):
            # num_zero_or_less + val - 1 is now the index
            # of the value to negate
            idx_to_negate = idx_of_first_positive + val - 1
            arr[idx_to_negate] = - arr[idx_to_negate]

    print('Negated array: {}'.format(arr))

    # Iterate through the array to find the first positive index
    idx = idx_of_first_positive
    while idx < len(arr):
        if arr[idx] > 0:
            break
        idx += 1

    print('First non-negated index: {}'.format(idx))
    print('First missing positive value: {}\n'
          .format(idx - idx_of_first_positive + 1))
    return idx - idx_of_first_positive + 1


class SimpleTest(unittest.TestCase):
    """ Basic tests for lowest_positive_integer_not_in_array """

    def test_lowest_positive_integer_not_in_array(self):

        self.assertEqual(lowest_positive_integer_not_in_array(
            [3, 4, -1, -6, -9, 1]), 2)

        self.assertEqual(lowest_positive_integer_not_in_array(
            [3, 4, -1, 1, -4, -6, 2]), 5)

        self.assertEqual(lowest_positive_integer_not_in_array(
            [1, 2, 0]), 3)

        self.assertEqual(lowest_positive_integer_not_in_array(
            [5, 4, 2, 1]), 3)

        self.assertEqual(lowest_positive_integer_not_in_array(
            [2, 5, 7, 3, 4, 1, 9, 8]), 6)


if __name__ == "__main__":
    unittest.main()  # run all tests
