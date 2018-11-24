#!/usr/bin/env python

from enum import Enum, auto
from move import PlacedWord
from typing import Dict, List
from util import Cell, Util


class BoardCellType(Enum):
    BLANK = auto()
    START = auto()
    DOUBLE_LETTER = auto()
    DOUBLE_WORD = auto()
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

    # Note: Neither config nor layout are cahnged after Game is initialized.
    def __deepcopy__(self):
        brd = Board(config, layout, self.letters[:][:])
        return brd

    def __getitem__(self, cell):
        return self.letters[cell.y][cell.x]

    def __setitem__(self, cell, char):
        self.letters[cell.y][cell.x] = char

    def __str__(self, compact=False):
        hooks = self.hooks()
        letters = [['+' if Cell(c, r) in self.layout.start_cells and self.is_cell_empty(Cell(c, r))
                        else self.letters[r][c]
                    for c in range(self.width)]
                    for r in range(self.height)]
        if compact:
            return '\t' + '\n\t'.join([''.join(row) for row in letters])
        else:
            header_footer = '\t' + ' ' * 4 + (''.join([str(k) for k in range(10)]) * 5)[:self.width]
            rows = [''.join(row) for row in letters]
            body = '\n'.join([f'\t{k:3d} {row} {k:3d}' for k, row in enumerate(rows)])
            return '{}\n{}\n{}'.format(header_footer, body, header_footer)

    def find_moves(self, gtree, rack):
        return gtree.find_moves(self, rack)

    # TODO: More efficient general solution? Set intersection? More efficient special cases (e.g., sparse board)?
    def hooks(self):
        hooks = []
        for cell in self.layout.start_cells:
            if self[cell] == Board.CHAR_EMPTY:
                hooks.append(cell)

        filled = set([cell for cell in self.cells_filled()])
        for cell in self.cells():
            if self[cell] == Board.CHAR_EMPTY:
                for adj in self.cells_adjacent(cell):
                    if adj in filled:
                        hooks.append(cell)
                        break
        return hooks

    # TODO: Improve efficiency. Unless undo is implemented, is_empty can be cached.
    #       Or hooks() could just be called with an is_board_empty flag.
    def is_empty(self):
        return all([ all([c == BoardCellType.BLANK for c in row])
                        for row in self.letters
                        ])

    def is_cell_empty(self, cell):
        return self[cell] == Board.CHAR_EMPTY

    def is_cell_on_board(self, cell):
        return (0 <= cell.x < self.width) and (0 <= cell.y < self.height)

    def move2points(self, move):
        cell2pl = {Cell(pl.x, pl.y): pl for pl in move.placed_letters}
        points = self.word2points(cell2pl, move.primary_word)
        for secondary_word in move.secondary_words:
            points += self.word2points(cell2pl, move.secondary_word)
        if len(move.placed_letters) == int(self.game.config['rack_size']):
            points += int(self.game.config['bingo_points'])
        return points

    def cells(self):
        for y in range(self.layout.height):
            for x in range(self.layout.width):
                yield Cell(x, y)

    def cells_adjacent(self, cell):
        for x in range(min(0, cell.x - 1), max(self.layout.width - 1, cell.x + 1) + 1):
            for y in range(min(0, cell.y - 1), max(self.layout.height - 1, cell.y + 1) + 1):
                yield Cell(x, y)

    def cells_filled(self):
        for cell in self.cells():
            if self[cell] != Board.CHAR_EMPTY:
                yield cell 

    def set_game(self, game):
        self.game = game

    def word2points(self, cell2pl, pw:PlacedWord):
        points = 0
        word_multiplier = 1
        for cell in pw.cells():
            # Letter is being placed on board
            if cell in cell2pl:
                pl = cell2pl[cell]
                letter_multiplier = 1
                if pl.char.islower():
                    bst = self.layout[cell]
                    if bst == BoardCellType.DOUBLE_LETTER:
                        letter_multiplier = 2
                    elif bst == BoardCellType.TRIPLE_LETTER:
                        letter_multiplier = 3
                    elif bst == BoardCellType.DOUBLE_WORD:
                        word_multiplier *= 2
                    elif bst == BoardCellType.TRIPLE_WORD:
                        word_multiplier *= 3
                points += self.game.char2points[pl.char] * letter_multiplier
            elif self[cell].islower():
                # Letter is non-blank, and already on board
                points += self.game.char2points[self[cell]]
        points *= word_multiplier
        return points


class BoardLayout:
    CHAR_LAYOUT_BLANK = '.'
    CHAR_LAYOUT_START = '*'
    CHAR_LAYOUT_DOUBLE_LETTER = '2'
    CHAR_LAYOUT_DOUBLE_WORD = '@'
    CHAR_LAYOUT_TRIPLE_LETTER = '3'
    CHAR_LAYOUT_TRIPLE_WORD = '#'

    char2bstype = { CHAR_LAYOUT_BLANK: BoardCellType.BLANK
                    , CHAR_LAYOUT_START: BoardCellType.START
                    , CHAR_LAYOUT_DOUBLE_LETTER: BoardCellType.DOUBLE_LETTER
                    , CHAR_LAYOUT_DOUBLE_WORD: BoardCellType.DOUBLE_WORD
                    , CHAR_LAYOUT_TRIPLE_LETTER: BoardCellType.TRIPLE_LETTER
                    , CHAR_LAYOUT_TRIPLE_WORD: BoardCellType.TRIPLE_WORD }
    bstype2char = Util.reversed_dict(char2bstype)

    def __init__(self, rows):
        self.letters = [[BoardLayout.char2bstype[c] for c in row] for row in rows]
        is_rectangle = all([len(row) == len(self.letters[0]) for row in self.letters])
        assert(is_rectangle)
        self.height = len(self.letters)
        self.width = len(self.letters[0])
        self.start_cells = [Cell(x, y) for x in range(self.width) for y in range(self.height)
                            if self[Cell(x, y)] == BoardCellType.START
                            ]

    def __getitem__(self, cell):
        return self.letters[cell.y][cell.x]

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
