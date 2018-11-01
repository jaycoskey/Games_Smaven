#!/usr/bin/env python

from enum import Enum

from util import Util


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
