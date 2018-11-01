#!/usr/bin/env python

from enum import Enum


class MoveType(Enum):
    NO_MOVE = 0
    PLACE = 1
    SWAP = 2
    PASS = 3
    RESIGN = 4

class Move:
    def __init__(self):
        # TODO: self.move_num: int
        # TODO: self.player_id: int
        # TODO: self.move_type: MoveType
        # TODO: self.played_letters: List[PlayedLetter]
        # TODO: self.played_words: List[PlayedWord]
        # TODO: self.letters_discarded: str
        # TODO: self.letters_drawn: str
        pass


class PlayedLetter:
    # TODO: self.player_id: int
    # TODO: self.char: str
    # TODO: self.square: Square
    pass


class PlayedWord:
    # TODO: self.word: str
    # TODO: self.player_id: int
    # TODO: self.square_begin: str
    # TODO: self.square_end: str
    pass
