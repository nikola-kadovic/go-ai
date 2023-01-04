from __future__ import annotations
from enum import Enum
from collections import namedtuple
from typing import List


class Player(Enum):
    BLACK = 1
    WHITE = 2

    @property
    def other(self) -> Player:
        return Player.BLACK if self == Player.WHITE else Player.WHITE


class Point(namedtuple('Point', 'row col')):
    def neighbors(self) -> List[Point]:
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]

    def corners(self) -> List[Point]:
        return [
            Point(self.row - 1, self.col - 1),
            Point(self.row - 1, self.col + 1),
            Point(self.row + 1, self.col - 1),
            Point(self.row + 1, self.col + 1)
        ]
