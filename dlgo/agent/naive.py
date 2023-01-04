from dlgo.agent.base import Agent
from dlgo.goboard import GameState, Move, Point
from dlgo.agent.helpers import is_point_an_eye
from random import choice

"""
The absolute worst GoAI imaginable. It selects random valid moves from the GoBoard that don't
fill in an eye, and plays these moves. If there are no available moves, it passes.
"""


class NaiveAgent(Agent):
    def __init__(self) -> None:
        super().__init__()

    def select_move(self, game_state: GameState) -> Move:
        potential_moves: list[Point] = []
        for row in range(1, game_state.board.num_rows + 1):
            for col in range(1, game_state.board.num_cols + 1):
                move = Move.play(Point(row, col))
                if not game_state.is_valid_move(move):
                    continue
                if not is_point_an_eye(game_state.board, Point(row, col), game_state.next_player):
                    potential_moves.append(move.point)

        if len(potential_moves) > 0:
            return Move.play(choice(potential_moves))
        else:
            return Move.pass_turn()
