# Fibonacci.py
#
# Generate the first n entries of the Fibonacci sequence,
# e.g. for n=10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
#
# fibonacci_generator() returns the next term in the sequence, up to and
# including the nth term.
#
# fibonacci() builds a list of all the terms up to and including the nth term

import unittest


def fibonacci_generator(n):
    """ Starting at 0, returns the next term in the Fibonacci sequence until
        the nth term.
    """

    prev = 0
    next = 1

    while n > 0:

        # Yield the next term in the sequence and update prev and next
        yield prev

        prev, next = next, prev+next
        n -= 1


def fibonacci(n):
    """ Return a list of the first n terms of the Fibonacci sequence.
        While convenient, this may be impractical for large values of n.
    """

    fib = []
    for term in fibonacci_generator(n):
        fib.append(term)

    return fib


class FibonacciTest(unittest.TestCase):
    """ Test Class for Fibonacci generator"""

    def test_fibonacci(self):
        """Test the first 10 terms of the Fibonacci sequence"""

        self.assertEqual(fibonacci(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

    def test_bad_n(self):
        """Test N<=0 results in empty sequence"""

        self.assertEqual(len(fibonacci(0)), 0)
        self.assertEqual(len(fibonacci(-10)), 0)


if __name__ == "__main__":
    unittest.main()  # run all tests
