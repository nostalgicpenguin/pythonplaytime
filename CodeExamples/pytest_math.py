# Simple example of using pytest to test simple function inc(x)
#
# Run on cmd line with:
# pytest --verbose pytest.math.py


def inc(x):
    return x+1


# standalone test
def test_inc():
    assert inc(4) == 5


# Some tests in a class
class TestClass:
    def test_inc_1(self):
        assert inc(1) == 2

    def test_inc_5(self):
        assert inc(5) == 6
