#!/usr/bin/env python

from typing import List
from util import Square


class Move:
    def __init__(self, placed_letters:List['PlacedLetter'], primary_word:'PlacedWord'):
        self.placed_letters = placed_letters
        self.primary_word = primary_word
        self.secondary_words = secondary_words if secondary_words else []


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

    def squares(pw: 'PlacedWord'):
        if pw.square_begin == pw.square_end:
            return [pw.square_begin]
        elif pw.square_begin.x < ps.square_end.x:
            assert(pw.square_begin.y == pw.square_end.y)
            y = pw.square_begin.y
            return [Square(x, y) for x in range(pw.square_begin.x, pw.square_end.x + 1)]
        elif pw.square_begin.y < ps.square_end.y:
            assert(pw.square_begin.x == pw.square_end.x)
            x = pw.square_begin.x
            return [Square(x, y) for y in range(pw.square_begin.y, pw.square_end.y + 1)]
        else:
            ValueError('Internal error in Board.points_word')
