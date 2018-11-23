#!/usr/bin/env python

from random import randint


class Bag:
    CHAR_BLANK = '_'
    DRAWN_NONE = ''
    DRAWN_UNKNOWN = '?'
    DISCARDED_NONE = ''

    def __init__(self, count2chars):
        char2count = {}
        for count in count2chars:
            for char in count2chars[count]:
                char2count[char] = count
        self.letters = ''.join([c * char2count[c] for c in char2count])

    def __len__(self):
        return len(self.letters)

    def add(self, chars):
        self.letters += chars

    def draw(self, count):
        if count > len(self.letters):
            avail = len(self.letters)
            raise ValueError(f'Not enough letters: {avail} available, but {count} requested')

        chars = []
        for _ in range(count):
            pos = randint(0, len(self.letters) - 1)
            chars.append(self.letters[pos])
            end = len(self.letters)
            self.letters = self.letters[0: pos] + self.letters[pos + 1: end]
        return ''.join(chars)

    def is_empty(self):
        return self.__len__() == 0
