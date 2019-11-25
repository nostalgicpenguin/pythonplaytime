# This problem was asked by Jane Street.
# cons(a, b) constructs a pair, and car(pair) and cdr(pair) returns the first
# and last element of that pair.
# For example, car(cons(3, 4)) returns 3, and cdr(cons(3, 4)) returns 4.
# Given this implementation of cons:
# def cons(a, b):
#     def pair(f):
#         return f(a, b)
#     return pair
# Implement car and cdr.

import unittest


def cons(a, b):
    """ cons() takes two parameters and returns a function which calls
        those params """
    def pair(f):
        return f(a, b)
    return pair


def car(f):
    """ f is a function taking two params, return the first of
        those params """
    def foo(x, _):
        return x
    return f(foo)


# Can do the same as car, but using a lambda!
def cdr(f):
    """ f is a function taking two params, return the second of
        those params """
    return f(lambda x, y: y)


class SimpleTest(unittest.TestCase):

    def test_pairs(self):
        self.assertEqual(car(cons(3, 4)), 3)
        self.assertEqual(cdr(cons(3, 4)), 4)


if __name__ == "__main__":
    unittest.main()  # run all tests
