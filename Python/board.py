#!/usr/bin/env python

from enum import Enum

from util import Util


# We store the board as a list of rows [i.e., (y, x)]. Should these directions be stored as (y, x)?
class BoardDirection(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, 1)
    DOWN = (0, -1)

    @staticmethod
    def reversed(brddir):
        if brddir == BoardDirection.LEFT: return BoardDirection.RIGHT
        elif brddir == BoardDirection.UP: return BoardDirection.DOWN

        # The following aren't needed unless words can be played right->left or down->up.
        elif brddir == BoardDirection.RIGHT: return BoardDirection.LEFT
        elif brddir == BoardDirection.DOWN: return BoardDirection.UP

class BoardSquareType(Enum):
    BLANK = 0
    CENTER = 1
    DOUBLE_LETTER = 2
    DOUBLE_WORD = 3
    TRIPLE_LETTER = 4
    TRIPLE_WORD = 5


class Board:
    # TODO: board_layout: BoardLayout
    # TODO: letters: List[List[str]]

    # TODO: def get_hooks()
    #           Move #1: The only hook is the center square
    #           Later moves: Hooks are empty spaces next to played words
    pass


class BoardLayout:
    def __init__(self, rows):
        char2bstype = { '.': BoardSquareType.BLANK
                      , '*': BoardSquareType.CENTER
                      , 'd': BoardSquareType.DOUBLE_LETTER
                      , 'D': BoardSquareType.DOUBLE_WORD
                      , 't': BoardSquareType.TRIPLE_LETTER
                      , 'T': BoardSquareType.TRIPLE_WORD }
        bstype2char = Util.reversed_dict(char2bstype)
        self.layout_rows = [[char2bstype[c] for c in row] for row in rows]

    def print(self):
        for row in self.layout_rows:
            print(map(lambda x: bstype2char[x], row))
