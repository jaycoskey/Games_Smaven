#!/usr/bin/env python

from enum import Enum
from typing import List
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
    def __init__(self, layout: 'BoardLayout', rows:List[str]=None):
        self.layout: BoardLayout = layout
        self.letters: List[List[str]] = [[c for c in row] for row in rows]

    def get_hooks():
        # TODO: Move #1: The only hook is the center square
        # TODO: Later moves: Hooks are empty spaces next to played words
        pass

    def print(self):
        for row in self.letters:
            for c in row:
                print(c, end='')
            print()


class BoardLayout:
    char2bstype = { '.': BoardSquareType.BLANK
                    , '*': BoardSquareType.CENTER
                    , 'd': BoardSquareType.DOUBLE_LETTER
                    , 'D': BoardSquareType.DOUBLE_WORD
                    , 't': BoardSquareType.TRIPLE_LETTER
                    , 'T': BoardSquareType.TRIPLE_WORD }
    bstype2char = Util.reversed_dict(char2bstype)
    def __init__(self, rows):
        self.layout_rows = [[BoardLayout.char2bstype[c] for c in row] for row in rows]

    def print(self):
        for row in self.layout_rows:
            print('.'.join([BoardLayout.bstype2char[c] for c in row]))
