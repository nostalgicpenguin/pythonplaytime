# Given a list of numbers and a number k, return whether any two numbers
# from the list add up to k.
# For example, given [10, 15, 3, 7] and k of 17, return True since 10 + 7 is 17
# Bonus: Can you do this in one pass?

import sys
import unittest


def two_numbers_sum_to_k(numbers, k):
    """ Returns True if any two entries in list numbers sum to k.
    """

    # Some basic sanity checking
    if len(numbers) < 2:
        print("{}: Not enough numbers!".format(sys._getframe().f_code.co_name))
        return False

    # Loop over numbers
    for i in range(len(numbers) - 1):

        # x is the entry at index i, and we'll test all the other entries
        # against it
        x = numbers[i]

        # Loop over numbers again, skipping the entry at index i
        for y in numbers[:i] + numbers[i + 1:]:

            # Test the sum of x and y and return True if equal to k
            if (x + y) == k:
                print('{}: {} and {} sum to {}'.format(
                    sys._getframe().f_code.co_name,
                    numbers[i],
                    k - numbers[i],
                    k)
                )

                return True

    else:
        print("{}: No numbers found to sum to {}".format(
            sys._getframe().f_code.co_name,
            k)
        )

        return False


# Do it in one pass!
def two_numbers_sum_to_k_single_pass(numbers, k):
    """ Returns True if any two entries in list numbers sum to k.
        Does it in a single pass!
    """

    # Some basic sanity checking
    if len(numbers) < 2:
        print("{}: Not enough numbers!".format(sys._getframe().f_code.co_name))
        return False

    for i in range(len(numbers) - 1):
        if((numbers[:i] + numbers[i + 1:]).count(k - numbers[i])):
            print('{}: {} and {} sum to {}'.format(
                sys._getframe().f_code.co_name,
                numbers[i],
                k - numbers[i],
                k)
            )

            return True

    else:
        print("{}: No numbers found to sum to {}".format(
            sys._getframe().f_code.co_name,
            k)
        )

        return False


class SimpleTest(unittest.TestCase):
    """ Basic tests for two_numbers_sum_to_k """

    def setUp(self):
        self.test_sequence = [10, 15, 3, 7]
        self.test_sum_correct = [10, 13, 17, 18, 22, 25]

    def test_multi_pass(self):
        """Test for two_numbers_sum_to_k (multi pass)"""

        for k in self.test_sum_correct:
            self.assertTrue(two_numbers_sum_to_k(self.test_sequence, k))
        self.assertFalse(two_numbers_sum_to_k(self.test_sequence, 12))

    def test_single_pass(self):
        """Test for two_numbers_sum_to_k (single pass)"""

        for k in self.test_sum_correct:
            self.assertTrue(two_numbers_sum_to_k_single_pass(
                self.test_sequence,
                k)
            )

        self.assertFalse(two_numbers_sum_to_k_single_pass(
            self.test_sequence,
            12)
        )

    def test_numbers_too_short(self):
        """Test for two_numbers_sum_to_k (single pass)"""

        sequence_short = [10]
        self.assertFalse(two_numbers_sum_to_k(sequence_short, 10))
        self.assertFalse(two_numbers_sum_to_k_single_pass(sequence_short, 10))


if __name__ == "__main__":
    unittest.main()  # run all tests
