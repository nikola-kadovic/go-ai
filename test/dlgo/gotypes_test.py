import pytest
from dlgo.gotypes import Player, Point
from test.helpers import is_equal_unordered


class TestPlayer:
    @pytest.fixture(scope="function")
    def white(self) -> Player:
        return Player.WHITE

    @pytest.fixture(scope="function")
    def black(self) -> Player:
        return Player.BLACK

    def test_proper_attributes(self):
        assert hasattr(Player, "WHITE")
        assert hasattr(Player, "BLACK")

    def test_other(self, white, black):
        assert white.other == black
        assert black.other == white


class TestPoint:
    @pytest.fixture(scope="function")
    def test_row(self) -> int:
        return 1

    @pytest.fixture(scope="function")
    def test_col(self) -> int:
        return 2

    @pytest.fixture(scope="function")
    def test_point(self) -> Point:
        return Point(1, 2)

    def test_proper_attributes(self, test_point, test_row, test_col):
        assert hasattr(test_point, "row")
        assert hasattr(test_point, "col")

        assert test_point.row == test_row
        assert test_point.col == test_col

    def test_neighbors(self, test_point, test_row, test_col):
        point = Point(test_row, test_col)

        # from definition of neighbors of a point
        expected_output = [
            Point(test_row - 1, test_col),
            Point(test_row + 1, test_col),
            Point(test_row, test_col - 1),
            Point(test_row, test_col + 1)
        ]

        assert is_equal_unordered(expected_output, point.neighbors())

    def test_corners(self, test_point, test_row, test_col):
        # from definition of corners of a point
        expected_output = [
            Point(test_row - 1, test_col - 1),
            Point(test_row - 1, test_col + 1),
            Point(test_row + 1, test_col - 1),
            Point(test_row + 1, test_col + 1)
        ]

        assert is_equal_unordered(expected_output, test_point.corners())
