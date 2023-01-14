import pytest
from test.helpers import is_equal_unordered
from dlgo.gotypes import Point, Player
from dlgo.goboard_slow import Move, GoString, Board, GameState  # TODO: reference everything in terms of goboard


class TestMove:
    @pytest.fixture(scope="function")
    def row(self) -> int:
        return 1

    @pytest.fixture(scope="function")
    def col(self) -> int:
        return 2

    def test_can_play(self, row, col):
        point = Point(row, col)
        move = Move.play(point)

        assert move.is_play
        assert not move.is_pass
        assert not move.is_resign

        assert move.point == point

    def test_can_pass(self):
        move = Move.pass_turn()

        assert not move.is_play
        assert move.is_pass
        assert not move.is_resign

        assert move.point is None

    def test_can_resign(self):
        move = Move.resign_turn()

        assert not move.is_play
        assert not move.is_pass
        assert move.is_resign

        assert move.point is None


class TestGoString:
    @pytest.fixture(scope="function")
    def go_string(self) -> GoString:
        return GoString(
            color=Player.WHITE,
            stones=[Point(2, 2)],
            liberties=Point(2, 2).neighbors()
        )

    def test_num_liberties(self, go_string):

        assert go_string.num_liberties == 4

    def test_add_liberty(self, go_string):

        go_string.add_liberty(Point(5, 5))

        assert Point(5, 5) in go_string.liberties

    def test_remove_liberty(self, go_string):

        go_string.remove_liberty(Point(1, 2))

        assert Point(1, 2) not in go_string.liberties

    def test_merged_with_requires_same_color_strings(self, go_string):

        go_string_2 = GoString(
            color=Player.BLACK,
            stones=[],
            liberties=[],
        )

        with pytest.raises(Exception):
            go_string.merged_with(go_string_2)

    def test_correctly_merges_go_strings_given_same_color(self, go_string):
        """
        Given GoString X:
        - - - - -
        | 0 1 2 3 4
        | 1   L
        | 2 L P L
        | 3   L
        | 4

        And GoString Y:
        - - - - -
        | 0 1 2 3 4
        | 1     L
        | 2   L P L
        | 3     L
        | 4

        By definition, merging GoStrings X and Y should result in the following board:
        - - - - -
        | 0 1 2 3 4
        | 1   L L
        | 2 L P P L
        | 3   L L
        | 4
        """

        go_string_2 = GoString(
            color=Player.WHITE,
            stones=[Point(2, 3)],
            liberties=[
                Point(2, 2),
                Point(2, 4),
                Point(1, 3),
                Point(3, 3),
            ]
        )

        result = go_string.merged_with(go_string_2)

        expected_liberties = [
            Point(2, 1),
            Point(1, 2),
            Point(3, 2),
            Point(1, 3),
            Point(3, 3),
            Point(2, 4)
        ]

        expected_stones = [
            Point(2, 2),
            Point(2, 3)
        ]

        assert is_equal_unordered(result.liberties, expected_liberties)
        assert is_equal_unordered(result.stones, expected_stones)


# TODO: should probably split up into unit tests and integration tests
class TestBoard:
    @pytest.fixture(scope="class")
    def board(self) -> Board:
        return Board(
            num_rows=4,
            num_cols=4
        )

    @pytest.fixture(scope="class")
    def partially_captured_string_board(self) -> Board:
        board = Board(num_rows=4, num_cols=4)
        # Place white in the middle
        board.place_stone(player=Player.WHITE, point=Point(2, 2))

        # Partially surround by black stones
        board.place_stone(player=Player.BLACK, point=Point(2, 1))
        board.place_stone(player=Player.BLACK, point=Point(1, 2))
        board.place_stone(player=Player.BLACK, point=Point(3, 2))

        return board

    def test_place_single_stone(self, board):
        test_point = Point(2, 2)
        board.place_stone(Player.WHITE, test_point)

        assert board.is_point_occupied(test_point)

        go_string = board.get_go_string(test_point)

        expected_stones = [test_point]
        expected_liberties = test_point.neighbors()

        assert go_string.color == Player.WHITE
        assert is_equal_unordered(go_string.stones, expected_stones)
        assert is_equal_unordered(go_string.liberties, expected_liberties)

    def test_cannot_place_stone_on_another_stone(self, board):
        test_point = Point(2, 2)

        with pytest.raises(Exception):
            board.place_stone(test_point)

    # TODO
    def test_placing_friendly_stones_together(self, board):
        pass

    def test_can_capture_string(self, partially_captured_string_board):
        board = partially_captured_string_board

        assert board.get_player(Point(2, 2)) == Player.WHITE
        white_string = board.get_go_string(Point(2, 2))
        assert white_string is not None
        assert white_string.liberties == {Point(2, 3)}

        board.place_stone(Player.BLACK, Point(2, 3))
        assert not board.is_point_occupied(Point(2, 2))


# TODO
class TestGameState:
    pass
