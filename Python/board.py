#!/usr/bin/env python

from enum import Enum, auto
from move import Move, PlacedLetter, PlacedWord
from typing import Dict, List
from util import Square, Util


# We store the board as a list of rows [i.e., (y, x)]. Should these directions be stored as (y, x)?
class BoardDirection(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, 1)
    DOWN = (0, -1)

    @staticmethod
    def is_forward(bdir):
        return bdir in [BoardDirection.RIGHT, BoardDirection.DOWN]

    @staticmethod
    def reversed(bdir):
        if bdir == BoardDirection.LEFT: return BoardDirection.RIGHT
        elif bdir == BoardDirection.UP: return BoardDirection.DOWN

        # The following aren't needed unless words can be played right->left or down->up.
        elif bdir == BoardDirection.RIGHT: return BoardDirection.LEFT
        elif bdir == BoardDirection.DOWN: return BoardDirection.UP


class BoardSquareType(Enum):
    BLANK = auto()
    CENTER = auto()
    DOUBLE_LETTER = auto()
    DOUBLE_WORD = auto()
    TRIPLE_LETTER = auto()
    TRIPLE_WORD = auto()


class Board:
    CHAR_EMPTY = '.'

    def __init__(self, layout:'BoardLayout', rows:List[str]=None):
        def config2obj(c):
            return Board.CHAR_EMPTY if c == '.' else c

        if layout is None:
            # For testing: If layout is None, then create a blank layout from rows.
            self.layout = BoardLayout([['.' for c in row] for row in rows])
        else:
            self.layout: BoardLayout = layout

        self.letters: List[List[str]] = [[config2obj(c) for c in row] for row in rows]

    def __getitem__(self, square):
        return self.letters[square.y][square.x]

    def get_secondary_word(self, gtree, cursor, char, bdir):
        if bdir in [BoardDirection.LEFT, BoardDirection.RIGHT]:
            back = BoardDirection.UP
        else:
            back = BoardDirection.LEFT
        forward = BoardDirection.reverse(back)

        begin = cursor
        end = cursor
        word = char

        while True:
            next_begin = Util.add_sq_bdir(begin, back)
            if self.has_character(next_begin):
                begin = next_begin
        while True:
            next_end = Util.add_sq_bdir(end, forward)
            if self.has_character(next_end):
                end = next_end
        if gtree.has_word(word):
            return PlacedWord(begin, end, word)

    # TODO: More efficient general solution? Set intersection? More efficient special cases (e.g., sparse board)?
    def hooks(self):
        """Return list of empty Squares adjacent to one already filled. (If board is empty, return center Square.)"""
        if self.is_empty():
            return [Square(int(layout.width / 2), int(layout.height / 2))]

        filled = set([s for s in self.squares_filled()])
        if not filled:  # If first player passed, for some reason
            return [Square(int(layout.width / 2), int(layout.height / 2))]

        hooks = []
        for s in self.squares():
            if self[s] is None:
                for adj in self.squares_adjacent(s):
                    if adj in s:
                        hooks.append(adj)
        return hooks

    # TODO: Improve efficiency. Unless undo is implemented, is_empty can be cached.
    #       Or hooks() could just be called with an is_board_empty flag.
    def is_empty(self):
        return all([ all([c == BoardSquareType.BLANK for c in row])
                        for row in self.letters
                        ])

    def is_square_on_board(self, s):
        return (0 <= s.x < self.width) and (0 <= s.y < self.height)

    def move2points(self, move:Move):
        square2pl = {Square(pl.x, pl.y): pl for pl in move.placed_letters}
        points = self.points_word(square2pl, move.primary_word)
        for secondary_word in move.secondary_words:
            points += self.word2points(square2pl, move.secondary_word)
        return points

    def print(self):
        for row in self.letters:
            for c in row:
                print(c, end='')
            print()

    def squares(self):
        for y in range(self.layout.height):
            for x in range(self.layout.width):
                yield Square(x, y)

    def squares_adjacent(self, square):
        for x in range(min(0, square.x - 1), max(self.layout.width - 1, square.x + 1) + 1):
            for y in range(min(0, square.y - 1), max(self.layout.height - 1, square.y + 1) + 1):
                yield Square(x, y)

    def squares_filled(self):
        for s in self.squares():
            if self[s] is not None:
                yield s

    def word2points(self, square2pl:Dict[Square, PlacedLetter], pw:PlacedWord):
        points = 0
        word_multiplier = 1
        for sq in pw.squares():
            if sq in square2pl:
                # Letter is being placed on board
                pl = square2pl[sq]
                if pl.char.islower():
                    bst = self.layout[sq.y][sq.x]
                    letter_multipler = 1
                    if bst == BoardSquareType.DOUBLE_LETTER:
                        letter_multipler = 2
                    elif bst == BoardSquareType.TRIPLE_LETTER:
                        letter_multipler = 3
                    elif bst == BoardSquareType.DOUBLE_WORD:
                        word_multipler *= 2
                    elif bst == BoardSquareType.TRIPLE_WORD:
                        word_multipler *= 3
                points += self.game.char2points[pl.char] * letter_multiplier
            elif pl.char.islower():
                # Letter is already on board
                points += self.game.char2points[self[sq]]
        points *= word_multipler
        return points


class BoardLayout:
    char2bstype = { '.': BoardSquareType.BLANK
                    , '*': BoardSquareType.CENTER
                    , 'd': BoardSquareType.DOUBLE_LETTER
                    , 'D': BoardSquareType.DOUBLE_WORD
                    , 't': BoardSquareType.TRIPLE_LETTER
                    , 'T': BoardSquareType.TRIPLE_WORD }
    bstype2char = Util.reversed_dict(char2bstype)
    def __init__(self, rows):
        self.layout = [[BoardLayout.char2bstype[c] for c in row] for row in rows]
        is_rectangle = all([len(row) == len(self.layout[0]) for row in self.layout])
        assert(is_rectangle)
        self.height = len(self.layout)
        self.width = len(self.layout[0])

    def print(self):
        for row in self.layout:
            print('.'.join([BoardLayout.bstype2char[c] for c in row]))
