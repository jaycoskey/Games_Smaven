#!/usr/bin/env python

from enum import Enum, auto
from move import PlacedWord
from typing import Dict, List
from util import Square, Util


class BoardSquareType(Enum):
    BLANK = auto()
    CENTER = auto()
    DOUBLE_LETTER = auto()
    DOUBLE_WORD = auto()
    INIT_HOOK = auto()
    TRIPLE_LETTER = auto()
    TRIPLE_WORD = auto()


class Board:
    CHAR_EMPTY = '.'

    def __init__(self, config, layout, rows:List[str]=None)->List[List[str]]:
        def board2char(c):
            return Board.CHAR_EMPTY if c == '.' else c

        self.config = config
        if (layout is None) and (rows is None):
            raise ValueError('Error in Board initialization: layout and board parameters cannot both be None')

        if layout is None:
            # For testing: If layout is None, then create a blank layout from rows.
            self.layout = BoardLayout([[Board.CHAR_EMPTY for c in row] for row in rows])
        else:
            # is_layout_rectangle = all([len(layout) == len(layout[0]) for row in rows])
            # assert(is_layout_rectangle)
            self.layout = layout

        if rows is None:
            self.letters = [[Board.CHAR_EMPTY for c in row] for row in self.layout.letters]
        else:
            is_board_rectangle = all([len(row) == len(rows[0]) for row in rows])
            assert(is_board_rectangle)
            self.letters = [[board2char(c) for c in row] for row in rows]

        self.height = len(self.letters)
        self.width = len(self.letters[0])
        assert(self.height == self.layout.height)
        assert(self.width == self.layout.width)

    def __getitem__(self, square):
        return self.letters[square.y][square.x]

    def __setitem__(self, square, char):
        self.letters[square.y][square.x] = char

    def __str__(self, compact=False):
        if compact:
            return '\t' + '\n\t'.join([''.join(row) for row in self.letters])
        else:
            header_footer = '\t' + ' ' * 4 + (''.join([str(k) for k in range(10)]) * 5)[:self.width]
            rows = [''.join(row) for row in self.letters]
            body = '\n'.join([f'\t{k:3d} {row} {k:3d}' for k, row in enumerate(rows)])
            return '{}\n{}\n{}'.format(header_footer, body, header_footer)

    def find_moves(self, gtree, rack):
        return gtree.find_moves(self, rack)

    # TODO: More efficient general solution? Set intersection? More efficient special cases (e.g., sparse board)?
    def hooks(self):
        """Return empty Squares adjacent to ones already filled. (If board is empty, return INIT_HOOKS.)"""
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

    def is_square_empty(self, s):
        return self[s] != Board.CHAR_EMPTY

    def is_square_on_board(self, s):
        return (0 <= s.x < self.width) and (0 <= s.y < self.height)

    def move2points(self, move):
        square2pl = {Square(pl.x, pl.y): pl for pl in move.placed_letters}
        points = self.word2points(square2pl, move.primary_word)
        for secondary_word in move.secondary_words:
            points += self.word2points(square2pl, move.secondary_word)
        if len(move.placed_letters) == int(self.config['rack_size']):
            points += int(self.config['bingo_points'])
        return points

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

    def word2points(self, square2pl, pw:PlacedWord):
        points = 0
        word_multiplier = 1
        for sq in pw.squares():
            # Letter is being placed on board
            if sq in square2pl:
                pl = square2pl[sq]
                if pl.char.islower():
                    bst = self.layout[sq.y][sq.x]
                    letter_multipler = 1
                    if bst == BoardSquareType.DOUBLE_LETTER:
                        letter_multipler = 2
                    elif bst == BoardSquareType.TRIPLE_LETTER:
                        letter_multipler = 3
                    elif bst == BoardSquareType.DOUBLE_WORD:
                        word_multiplier *= 2
                    elif bst == BoardSquareType.TRIPLE_WORD:
                        word_multiplier *= 3
                points += self.game.char2points[pl.char] * letter_multiplier
            elif self[sq].islower():
                # Letter is non-blank, and already on board
                points += self.game.char2points[self[sq]]
        points *= word_multiplier
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
        self.letters = [[BoardLayout.char2bstype[c] for c in row] for row in rows]
        is_rectangle = all([len(row) == len(self.letters[0]) for row in self.letters])
        assert(is_rectangle)
        self.height = len(self.letters)
        self.width = len(self.letters[0])

    def __str__(self, compact=False):
        if compact:
            return ('\t'
                    + '\n\t'.join(
                        [ ''.join([BoardLayout.bstype2char[x] for x in row]) for row in self.letters ]
                        )
                    )
        else:
            header_footer = '\t' + ' ' * 4 + (''.join([str(k) for k in range(10)]) * 5)[:self.width]
            rows = [ ''.join([BoardLayout.bstype2char[x] for x in row]) for row in self.letters ]
            body = '\n'.join([f'\t{k:3d} {row} {k:3d}' for k, row in enumerate(rows)])
            return '{}\n{}\n{}'.format(header_footer, body, header_footer)
