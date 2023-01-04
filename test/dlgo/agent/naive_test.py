import pytest
from dlgo import gotypes

# NOTE: we are using goboard slow for these tests. If correctly implemented and tested
# both GoBoards and GameStates should operate identically from an external point of view.
from dlgo import goboard_slow as goboard
from dlgo.agent import naive


class TestNaiveAgent:
    @pytest.fixture(scope="class")
    def game_state_no_moves(self) -> goboard.GameState:
        game_state = goboard.GameState.new_game(board_size=1)

        game_state = game_state.apply_move(
            move=goboard.Move(
                point=gotypes.Point(1, 1)
            ))

        return game_state  # Player.WHITE's turn

    @pytest.fixture(scope="class")
    def game_state_one_move(self) -> goboard.GameState:
        game_state = goboard.GameState.new_game(board_size=2)

        game_state = game_state.apply_move(goboard.Move(gotypes.Point(1, 1)))
        game_state = game_state.apply_move(goboard.Move(gotypes.Point(1, 2)))
        game_state = game_state.apply_move(goboard.Move(gotypes.Point(2, 1)))

        return game_state  # Player.WHITE's turn, only Point(2, 2) remaining

    @pytest.fixture(scope="class")
    def game_state_multiple_moves(self) -> goboard.GameState:
        game_state = goboard.GameState.new_game(board_size=2)

        game_state = game_state.apply_move(goboard.Move(gotypes.Point(1, 1)))
        game_state = game_state.apply_move(goboard.Move(gotypes.Point(1, 2)))

        return game_state  # Player.BLACK's turn, Point(2, 1), Point(2, 2) remaining

    @pytest.fixture(scope="function")
    def agent(self) -> naive.NaiveAgent:
        return naive.NaiveAgent()

    def test_agent_handles_no_available_moves(self, agent: naive.NaiveAgent, game_state_no_moves: goboard.GameState):
        move = agent.select_move(game_state_no_moves)

        assert move.is_pass
        assert move.is_play is False
        assert move.is_resign is False

    def test_agent_handles_one_available_move(self, agent: naive.NaiveAgent, game_state_one_move: goboard.GameState):
        move = agent.select_move(game_state_one_move)

        assert move.is_play
        assert move.point == gotypes.Point(2, 2)

    def test_agent_handles_multiple_available_moves(self, agent: naive.NaiveAgent,
                                                    game_state_multiple_moves: goboard.GameState):
        move = agent.select_move(game_state_multiple_moves)

        assert move.is_play
        # TODO: should probably mock out the random function to adhere to principles
        assert move.point in [gotypes.Point(2, 1), gotypes.Point(2, 2)]
