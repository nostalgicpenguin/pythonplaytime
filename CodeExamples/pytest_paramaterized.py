import pytest


def add(x, y):
    return x+y


def subtract(x, y):
    return x-y

#
# Standalone tests
#


@pytest.fixture
def n():
    # highly artificial example of using a fixture to set up some context
    i = 5
    return i


@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (5, 6, 11),
    (-1, 1, 0)
])
def test_add(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    (1, 2, -1),
    (5, 6, -1),
    (-1, 1, -2)
])
def test_subtract(a, b, expected):
    assert subtract(a, b) == expected


@pytest.mark.parametrize("a, expected", [
    (1, 6),
    (5, 10)
])
def test_add_n(a, n, expected):  # n is a function defined by the fixture
    assert add(a, n) == expected


#
# Tests in a class
#

class TestMathUnitTest():
    @pytest.mark.parametrize("a, b, expected", [
        (1, 2, 3),
        (5, 6, 11),
        (-1, 1, 0)
    ])
    def test_add(self, a, b, expected):
        assert add(a, b) == expected

    @pytest.mark.parametrize("a, b, expected", [
        (1, 2, -1),
        (5, 6, -1),
        (-1, 1, -2)
    ])
    def test_subtract(self, a, b, expected):
        assert subtract(a, b) == expected
