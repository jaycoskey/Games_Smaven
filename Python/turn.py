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
        if turn_type == TurnType.PLACE:
            assert(move and len(drawn) > 0 and not discarded)
        elif turn_type == TurnType.SWAP:
            assert(not move and len(discarded) > 0)
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
        self.drawn = drawn
        self.discarded = discarded

    def __str__(self):
        return ('\n\t'.join([f'Turn<player_id={self.player_id}'
                            , f'turn_type={self.turn_type}'
                            , f'points={self.points}'
                            , f'move={self.move}'
                            , f'drawn={self.drawn}'
                            , f"discarded={'NONE' if self.discarded == '' else self.discarded}>"]))

