from dlgo import goboard, gotypes

__all__ = ['print_move', 'print_board']

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