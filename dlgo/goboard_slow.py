from __future__ import annotations
from typing import Iterable
import copy
from dlgo.gotypes import Point, Player


class Move:
    def __init__(self, point: Point | None, is_pass: bool = False, is_resign: bool = False) -> None:
        assert (point is not None) ^ is_pass ^ is_resign

        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, move: Point):
        return Move(move)

    @classmethod
    def pass_turn(cls):
        return Move(None, is_pass=True)

    @classmethod
    def resign_turn(cls):
        return Move(None, is_resign=True)


class GoString:
    def __init__(self, color: Player, stones: Iterable[Point], liberties: Iterable[Point]) -> None:
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def add_liberty(self, point: Point) -> None:
        self.liberties.add(point)

    def remove_liberty(self, point: Point) -> None:
        self.liberties.remove(point)

    def merged_with(self, go_string: GoString) -> GoString:
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        combined_liberties = (
                                     self.liberties | go_string.liberties) - combined_stones

        return GoString(self.color, combined_stones, combined_liberties)

    @property
    def num_liberties(self) -> int:
        return len(self.liberties)

    def __eq__(self, __o: GoString) -> bool:
        return self.color == __o.color and self.stones == __o.stones and self.liberties == __o.liberties


class Board:
    def __init__(self, num_rows: int, num_cols: int) -> None:
        self.num_rows = num_rows
        self.num_cols = num_cols

        self._grid: dict[Point, GoString | None] = {}

    def place_stone(self, player: Player, point: Point) -> None:
        """
        To place a stone, do the following:

        1. merge any adjacent strings of the same color
        2. reduce liberties of any adjacent strings of opposite color
        3. if any opposite-color strings have zero liberties, remove them.
        """
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None

        adjacent_same_color: list[GoString] = []
        adjacent_opposite_color: list[GoString] = []
        liberties: list[Point] = []

        # sort neighbors into categories: same color, opposite color, unoccupied (liberty)
        for neighbor_point in point.neighbors():
            if not self.is_on_grid(neighbor_point):
                continue
            neighbor_string = self._grid.get(neighbor_point)
            if neighbor_string is None:
                liberties.append(neighbor_point)
            elif neighbor_string.color == player and neighbor_string not in adjacent_same_color:
                adjacent_same_color.append(neighbor_string)
            elif neighbor_string.color != player and neighbor_string not in adjacent_opposite_color:
                adjacent_opposite_color.append(neighbor_string)

        # create initial GoString of placed stone
        new_string = GoString(color=player, stones=[point], liberties=liberties)

        # merge all same-colored GoStrings together
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)

        # map all points the new_string covers to new_string
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string

        # remove liberties of neighbors that aren't the same color. If no more liberties for a GoString, remove it
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)

            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)

    def is_on_grid(self, point: Point) -> bool:
        return 1 <= point.row <= self.num_rows and 1 <= point.col <= self.num_cols

    def get_player(self, point: Point) -> Player | None:
        string = self._grid.get(point)

        if string is None:
            return None

        return string.color

    def get_go_string(self, point: Point) -> GoString | None:
        return self._grid.get(point)

    def is_point_occupied(self, point: Point) -> bool:
        string = self._grid.get(point)

        return string is not None

    def _remove_string(self, string: GoString):
        for point in string.stones:

            # for all neighboring points, add the removed point as a liberty if it is part of a GoString
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)
            self._grid[point] = None


class GameState:
    def __init__(self, board: Board, next_player: Player, previous_state: GameState | None, last_move: Move | None):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous_state
        self.last_move = last_move

    @classmethod
    def new_game(cls, board_size: int) -> GameState:
        return GameState(Board(board_size, board_size), Player.BLACK, None, None)

    def apply_move(self, move: Move) -> GameState:
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    def is_over(self) -> bool:
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        if self.previous_state.last_move is None:
            return False
        return self.last_move.is_pass and self.previous_state.last_move.is_pass

    def is_move_self_capture(self, player: Player, move: Move) -> bool:
        """
        A move can be considered self-capture iff you have a GoString that has 1 liberty left,
        and you place a stone on that point.
        """
        if not move.is_play:
            return False
        future_board = copy.deepcopy(self.board)
        future_board.place_stone(player, move.point)
        return future_board.get_go_string(move.point).liberties == 0

    """
    Ko: A situation that arises when a player plays a move where the resulting GameState is identical to another
    GameState played in the past. 	
    """

    @property
    def situation(self) -> tuple[Player, Board]:
        return self.next_player, self.board

    def does_not_violate_ko(self, player: Player, move: Move) -> bool:
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation: tuple[Player, Board] = (player.other, next_board)
        node = self.previous_state
        while node is not None:
            if node.situation == next_situation:
                return True
            node = node.previous_state
        return False

    def is_valid_move(self, move: Move) -> bool:
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return (
                self.board.get_go_string(move.point) is None and
                not self.is_move_self_capture(self.next_player, move) and
                not self.does_not_violate_ko(self.next_player, move)
        )
