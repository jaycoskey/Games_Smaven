#!/usr/bin/env python

from copy import deepcopy


from board_direction import BoardDirection
from typing import List
from util import Cell, Util


class Move:
    def __init__(self, placed_letters:List['PlacedLetter']
                    , primary_word:'PlacedWord', secondary_words=None):
        self.placed_letters = placed_letters
        self.primary_word = primary_word
        self.secondary_words = secondary_words if secondary_words else []

    def __deepcopy__(self, memo=None):
       move = Move([deepcopy(pl) for pl in self.placed_letters]
                    , deepcopy(self.primary_word)
                    , [deepcopy(sw) for sw in deepcopy(secondary_words)]
                    )
       return move

    def __eq__(self, other):
        return (self.placed_letters == other.placed_letters
                and self.primary_word == other.primary_word
                and self.secondary_words == other.secondary_words
                )

    def __str__(self):
        pls_val = ','.join([str(pl) for pl in self.placed_letters])
        pls = f"placed_letters={'NONE' if pls_val == '' else pls_val}"
        pw_val = str(self.primary_word)
        pw = f'primary_word={pw_val}'
        sec_val = ','.join([str(w) for w in self.secondary_words])
        sec = f"secondary_words=[{sec_val}]"
        return f'Move<{pls},{pw},{sec}>'

    def updated(self, new_placed_letters, bdir, new_char, new_secondary_words):
        return Move(self.placed_letters.extend(new_placed_letters)
                , Util.update_with_char(self.primary_word, bdir, new_char)
                , self.secondary_words.extend(new_secondary_words)
                )


# Note: The use here of lowercase and uppercase does not work for most languages.
class PlacedLetter:
    def __init__(self, cell:Cell, char:str, is_blank:bool=False):
        self.char = upper(char) if is_blank else char.lower()
        self.cell = cell

    def __deepcopy__(self, memo=None):
        return PlacedLetter(self.char, self.cell)

    def __eq__(self, other):
        return self.char == other.char and self.cell == other.cell

    def __str__(self):
        return f"'{self.char}'@{Util.cell2str(self.cell)}"

    def is_blank(self):
        return isupper(self.char)

    @property
    def x(self):
        return self.cell.x

    @property
    def y(self):
        return self.cell.y


class PlacedWord:
    def __init__(self, cell_begin, cell_end, word):
        self.cell_begin = cell_begin
        self.cell_end = cell_end
        self.word = word

    def __deepcopy__(self, memo=None):
        return PlacedWord(self.cell_begin, self.cell_end, self.word)

    def __eq__(self, other):
        return (self.cell_begin == other.cell_begin
                and self.cell_end == other.cell_end
                and self.word == other.word
                )

    def __str__(self):
        return f'"{self.word}"@[{Util.cell2str(self.cell_begin)}..{Util.cell2str(self.cell_end)}]'

    def cells(self):
        if self.cell_begin == self.cell_end:
            return [self.cell_begin]
        elif self.cell_begin.x < self.cell_end.x:
            assert(self.cell_begin.y == self.cell_end.y)
            y = self.cell_begin.y
            return [Cell(x, y) for x in range(self.cell_begin.x, self.cell_end.x + 1)]
        elif self.cell_begin.y < self.cell_end.y:
            assert(self.cell_begin.x == self.cell_end.x)
            x = self.cell_begin.x
            return [Cell(x, y) for y in range(self.cell_begin.y, self.cell_end.y + 1)]
        else:
            ValueError('Internal error in Board.points_word')

    def updated(self, cursor, bdir, char):
        next_cell_begin = (
                self.cell_begin if BoardDirection.is_forward(bdir)
                else Util.add_cell_bdir(self.cell_begin, bdir)
                )
        next_cell_end = (
                self.cell_end if not BoardDirection.is_forward(bdir)
                else Util.add_cell_bdir(self.cell_end, bdir)
                )
        next_word = Util.updated_str_with_char(self.word, bdir, char)

        return PlacedWord(next_cell_begin, next_cell_end, next_word)
