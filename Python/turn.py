#!/usr/bin/env python

from enum import Enum, auto

from move import Move


class TurnType(Enum):
    PLACE = auto()
    SWAP = auto()
    PASS = auto()
    RESIGN = auto()


class Turn:
    next_turn_num = 1

    def __init__(self, player_id:int, turn_type:TurnType, points:int, move:Move=None, drawn:str=None, discarded:str=None):
        # print(f'INFO: Turn(): player_id={player_id}, turn_type={turn_type}, points={points}, move={move}, drawn={drawn}, discarded={discarded}')
        if turn_type == TurnType.PLACE:
            assert(move and len(drawn) > 0 and not discarded)
        elif turn_type == TurnType.SWAP:
            assert(not move and len(drawn) > 0 and len(discarded) > 0 and len(drawn) == len(discarded))
        elif turn_type == TurnType.PASS:
            assert(points == 0 and not move and not drawn and not discarded)
        elif turn_type == TurnType.RESIGN:
            assert(points == 0 and not move and not drawn and not discarded)

        self.turn_num = Turn.next_turn_num
        Turn.next_turn_num += 1

        self.player_id = player_id
        self.turn_type = turn_type
        self.points = points
        self.move = move
        self.letters_drawn = drawn
        self.letters_discarded = discarded
