#!/usr/bin/env python

from typing import List
from util import Square


class Move:
    def __init__(self, placed_letters:List['PlacedLetter'], primary_word:'PlacedWord'):
        self.placed_letters = placed_letters
        self.primary_word = primary_word
        self.secondary_words = secondary_words if secondary_words else []

    def updated(self, new_placed_letters, bdir, new_char, new_secondary_words):
        return Move(self.placed_letters.extend(new_placed_letters)
                , Util.update_with_char(self.primary_word, bdir, new_char)
                , self.secondary_words.extend(new_secondary_words)
                )


# Note: For now, use uppercase to represent the character used for blank tiles & lowercase for others.
class PlacedLetter:
    def __init__(self, square:Square, char:str):
        self.char = char
        self.square: Square


class PlacedWord:
    def __init__(self, square_begin, square_end, word):
        self.square_begin = square_begin
        self.square_end = square_end
        self.word = word

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
        next_word = (
                Util.append_char(self.word, child_gnode.char) if BoardDirection.is_forward(bdir)
                else Util.prepend_char(self.word, child_gnode.char)
                )
        return PlacedWord(next_square_begin, next_square_end, next_word)
