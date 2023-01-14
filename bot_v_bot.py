import time
from dlgo import gotypes, goboard, utils
from dlgo.agent import naive, base


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
        utils.print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        game = game.apply_move(bot_move)


if __name__ == '__main__':
    main()
