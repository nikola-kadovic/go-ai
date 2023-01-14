import random

from dlgo.gotypes import Player, Point
"""
This file generates a list of all zobrist hashes for our board into a table. We place this in our hash table zobrist.py
"""


# 2 ^ 63 - 1, the maximum number we can have for the purposes of our hashes. Since we are
# only creating 722 hashes, we can just assume each number will be unique
MAX63 = 0x7fffffffffffffff


def to_str(player_state: Player) -> str:
    if player_state is None:
        return 'None'
    else:
        return str(player_state)


table = {}
empty_board = 0

for row in range(1, 20):
    for col in range(1, 20):
        for state in (Player.BLACK, Player.WHITE):
            code = random.randint(0, MAX63)
            table[Point(row, col), state] = code

print('from dlgo.gotypes import Player, Point', end='\n\n')
print("__all__ = ['HASH_CODE', 'EMPTY_BOARD']", end='\n\n')
print('HASH_CODE = {')

for (pt, state), hash_code in table.items():
    print(' (%r, %s): %r,' % (pt, to_str(state), hash_code))

print('}\n')
print('EMPTY_BOARD = %d' % (empty_board,))
