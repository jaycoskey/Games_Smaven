#!/usr/bin/env python

from board_direction import BoardDirection
from typing import List
from util import Square, Util


class Move:
    def __init__(self, placed_letters:List['PlacedLetter']
            , primary_word:'PlacedWord', secondary_words=None):
        self.placed_letters = placed_letters
        self.primary_word = primary_word
        self.secondary_words = secondary_words if secondary_words else []

    def __str__(self):
        pls_val = ','.join([str(pl) for pl in self.placed_letters])
        pls = f'placed_letters={pls_val}'
        pw_val = str(self.primary_word)
        pw = f'primary_word={pw_val}'
        sec_val = ','.join([str(w) for w in self.secondary_words])
        sec = f'secondary_words=[{sec_val}]'
        return f'Move<{pls},{pw},{sec}'

    def copy(self):
        return Move([pl.copy() for pl in self.placed_letters]
                    , self.primary_word.copy()
                    , [pw.copy() for pw in self.secondary_words]
                    )

    def updated(self, new_placed_letters, bdir, new_char, new_secondary_words):
        return Move(self.placed_letters.extend(new_placed_letters)
                , Util.update_with_char(self.primary_word, bdir, new_char)
                , self.secondary_words.extend(new_secondary_words)
                )


# Note: The use here of lowercase and uppercase does not work for most languages.
class PlacedLetter:
    def __init__(self, square:Square, char:str, is_blank:bool=False):
        self.char = upper(char) if is_blank else char.lower()
        self.square = square

    def __str__(self):
        return f"'{self.char}'@{Util.sq2str(self.square)}"

    def copy(self):
        return PlacedLetter(self.square, self.char)

    def is_blank(self):
        return isupper(self.char)


class PlacedWord:
    def __init__(self, square_begin, square_end, word):
        self.square_begin = square_begin
        self.square_end = square_end
        self.word = word

    def __str__(self):
        return f'"{self.word}"@[{Util.sq2str(self.square_begin)}..{Util.sq2str(self.square_end)}]'

    def copy(self):
        return PlacedWord(self.square_begin, self.square_end, self.word)

    def squares(self):
        if self.square_begin == self.square_end:
            return [self.square_begin]
        elif self.square_begin.x < self.square_end.x:
            assert(self.square_begin.y == self.square_end.y)
            y = self.square_begin.y
            return [Square(x, y) for x in range(self.square_begin.x, self.square_end.x + 1)]
        elif self.square_begin.y < self.square_end.y:
            assert(self.square_begin.x == self.square_end.x)
            x = self.square_begin.x
            return [Square(x, y) for y in range(self.square_begin.y, self.square_end.y + 1)]
        else:
            ValueError('Internal error in Board.points_word')

    def updated(self, cursor, bdir, char):
        next_square_begin = (
                self.square_begin if BoardDirection.is_forward(bdir)
                else Util.add_sq_bdir(self.square_begin, bdir)
                )
        next_square_end = (
                self.square_end if not BoardDirection.is_forward(bdir)
                else Util.add_sq_bdir(self.square_end, bdir)
                )
        next_word = Util.updated_str_with_char(self.word, bdir, char)

        return PlacedWord(next_square_begin, next_square_end, next_word)
