from dlgo import goboard, gotypes, utils
from dlgo.agent import naive


def main() -> None:
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bot = naive.NaiveAgent()

    while not game.is_over():

        print(chr(27) + "[2J")
        utils.print_board(game.board)

        if game.next_player == gotypes.Player.BLACK:
            human_move = input('Enter your move: ')
            # TODO: input checking
            point = utils.point_from_coords(human_move.strip())
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)
        
        utils.print_move(game.next_player, move)
        game = game.apply_move(move)

if __name__ == '__main__':
    main()
