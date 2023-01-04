from dlgo.gotypes import Point
from dlgo.goboard_slow import Board, Point, Player

"""
In the context of Go, an eye can be defined as a single unoccupied space in a GoString where it is impossible
for an opponent to place a stone. 

A property of GoStrings with at least one eye is that it is impossible to capture the string - it will always have
at least one liberty, and it is impossible to place a stone to remove that liberty.
"""


def is_point_an_eye(board: Board, point: Point, color: Player) -> bool:
    # if occupied, trivially not an eye.
    if board.get_go_string(point) is not None:
        return False

    # all immediate neighbors of the point must contain friendly stones
    for neighbor in point.neighbors():
        if board.is_on_grid(neighbor) and board.get_player(neighbor) != color:
            return False

    friendly_corners = 0
    off_board_corners = 0

    for corner in point.corners():
        if board.is_on_grid(corner):
            if board.get_player(corner) == color:
                friendly_corners += 1
        else:
            off_board_corners += 1

        if off_board_corners > 0:
            return off_board_corners + friendly_corners == 4
        return friendly_corners >= 3
