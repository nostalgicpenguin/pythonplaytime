import unittest
from unittest.mock import patch

# Wrapper calls _real1() and _real2(), but must mock these out so that
# they aren't called from the unittest


def _real1():
    # Could raise FileNotFoundError or EOFError
    assert(False)  # Make sure this is never called!


def _real2():
    # Could raise BrokenPipeError
    assert(False)  # Make sure this is never called!


def wrapper():

    try:
        _real1()
        _real2()

    except FileNotFoundError:
        return False
    except EOFError:
        return False
    except BrokenPipeError:
        return False

    return True


class SimpleTest(unittest.TestCase):

    # Mock out _real1() and _real2() using patch() decorator
    # Each _real function now appears as an additional arg to test function

    @patch('__main__._real1')
    @patch('__main__._real2')
    def test_wrapper_success(self, _real1_func, _real2_func):
        self.assertEqual(wrapper(), True)

    @patch('__main__._real1')
    @patch('__main__._real2')
    def test_wrapper_success2(self, _real1_func, _real2_func):
        self.assertEqual(wrapper(), True)

    @patch('__main__._real1', side_effect=FileNotFoundError)
    @patch('__main__._real2')
    def test_wrapper_fail_file_not_found(self,  _real1_func, _real2_func):
        self.assertEqual(wrapper(), False)

    @patch('__main__._real1', side_effect=EOFError)
    @patch('__main__._real2')
    def test_wrapper_fail_eof(self,  _real1_func, _real2_func):
        self.assertEqual(wrapper(), False)

    @patch('__main__._real1')
    @patch('__main__._real2', side_effect=BrokenPipeError)
    def test_wrapper_fail_broken_pipe(self, _real1_func, _real2_func):
        self.assertEqual(wrapper(), False)


if __name__ == "__main__":
    unittest.main()  # run all tests
