# This problem was asked by Amazon.
# Given an integer k and a string s, find the length of the longest substring
# that contains at most k distinct characters.
# For example, given s = "abcba" and k = 2, the longest substring with k
# distinct characters is "bcb".
import unittest


class SubStr:

    def __init__(self):
        self.substr = []
        self.distinct_chars = set()

    def get(self):
        return self.substr

    def append(self, s):
        self.substr.append(s)
        self.distinct_chars.add(s)

    def num_distinct_chars(self):
        return len(self.distinct_chars)

    def contains_char(self, s):
        return s in self.distinct_chars

    def len(self):
        return len(self.substr)


def find_longest_substr(string, k):
    substrs = []
    max_substr = SubStr()

    for s in string:

        # Look through all current substrs to see if this char should be added
        keep = []
        for substr in substrs:

            if substr.contains_char(s) or substr.num_distinct_chars() < k:
                # Either char in substr or not in, but haven't hit k limit
                substr.append(s)
                keep.append(substr)
                if substr.len() > max_substr.len():
                    max_substr = substr
            else:
                # char cannot be added, so discard substr
                pass

        # Now create a new substr for current char
        new_substr = SubStr()
        new_substr.append(s)
        keep.append(new_substr)

        substrs = keep.copy()

    return "".join(max_substr.get())


class SimpleTest(unittest.TestCase):

    def test_longest_substring(self):

        self.assertEqual('bcb', find_longest_substr('abcba', 2))
        self.assertEqual('abcba', find_longest_substr('abcba', 3))
        self.assertEqual('cdcdcdcdc', find_longest_substr('abcbcdcdcdcdca', 2))
        self.assertEqual('ab', find_longest_substr('abcde', 2))
        self.assertEqual('ccc', find_longest_substr('abcccd', 1))


if __name__ == "__main__":
    unittest.main()  # run all tests
