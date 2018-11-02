#!/usr/bin/env python

from enum import Enum


class TurnType(Enum):
    NO_TURN = 0
    MOVE = 1
    SWAP = 2
    PASS = 3
    RESIGN = 4


class Turn:
    def __init__(self):
        # TODO: self.turn_num: int
        # TODO: self.turn_type: TurnType
        # TODO: self.player_id: int
        # TODO: self.move: Move
        # TODO: self.letters_discarded: str
        # TODO: self.letters_drawn: str
        # TODO: self.points: str
        pass
