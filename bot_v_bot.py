import time

import dlgo.agent.base
from dlgo import gotypes
from dlgo import goboard
from dlgo.agent import naive, base

# As per Go standards
COLS = 'ABCDEFGHIJKLMNOPQRST'

STONE_TO_CHAR: dict[gotypes.Player, str] = {
    None: ' . ',
    gotypes.Player.BLACK: ' x ',
    gotypes.Player.WHITE: ' o ',
}


def print_move(player: gotypes.Player, move: goboard.Move):
    if move.is_pass:
        move_str = f"player {str(player)} passes"
    elif move.is_resign:
        move_str = f"player {str(player)} resigns"
    else:
        move_str = f"{str(player)} {COLS[move.point.cols - 1]} {move.point.row}"
    print(move_str)


def print_board(board: goboard.Board):
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line = []
        for col in range(1, board.num_rows + 1):
            stone = board.get_player(gotypes.Point(row, col))
            line.append(STONE_TO_CHAR[stone])
        print(f"{bump}{row} {''.join(line)}")
    print(f"    {'  '.join(COLS[:board.num_cols])}")


def main():
    board_size = 9

    game = goboard.GameState.new_game(board_size)
    bots: dict[gotypes.Player, base.Agent] = {
        gotypes.Player.BLACK: naive.NaiveAgent(),
        gotypes.Player.WHITE: naive.NaiveAgent()
    }

    while not game.is_over():
        time.sleep(0.3)

        print(chr(27) + "[2J")
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        game = game.apply_move(bot_move)


if __name__ == '__main__':
    main()
