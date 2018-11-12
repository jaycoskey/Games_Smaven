#!/usr/bin/env python

import logging


from board import Board
from board_direction import BoardDirection
from move import Move, PlacedLetter, PlacedWord
from typing import Iterable, List, Set
from util import Square


# A node in a GADDAG. (See the Wikipedia page for GADDAG.)
# TODO: Support serialization & deserialization.
class GNode:
    VERBOSE = False
    CHAR_BLANK = ' '

    # CHAR_EOW marks the end of a word, though other words might continue on (e.g. win/winsome).
    CHAR_EOW = '$'

    # CHAR_REV marks the end of the reversed portion of word traveral. (See the GADDAG Wikipedia page.)
    CHAR_REV = '+'

    # CHAR_ROOT is the char of the root of the Trie.
    CHAR_ROOT = '*'

    def __init__(self, char:str):
        self.char = char
        self.children:Dict[str, GNode] = {}

    def __len__(self):
        return 1 + sum([len(c) for c in self.children])

    def __str__(self, indent_level=0):
        indent_str = '  '
        result = (
            f'{indent_str * indent_level}{self.char}\n'
            + '\n'.join([self.children[c].__str__(indent_level + 1) for c in self.children])
            )
        return result

    def add_child(self, char:str)->'GNode':
        child = GNode(char)
        self.children[char] = child
        return child

    def add_string(self, s):
        """Add a string to the subtree based at this GNode. Can contain content characters and CHAR_REV."""
        if s == '':
            # Reached the end of the string. Add the EOW char.
            child = self.add_child(GNode.CHAR_EOW)
        elif s[0] in self.children:
            child = self.children[s[0]]
            child.add_string(s[1:])
        else:
            # Add the next char, and continue recursively.
            child = self.add_child(s[0])
            child.add_string(s[1:])


class GTree:
    VERBOSE = False

    def __init__(self, filename=None):
        print('Creating dictionary ....')
        self.root = GNode(GNode.CHAR_ROOT)
        if filename:
            self.add_wordfile(filename)

    def __len__(self):
        return len(self.root)

    def __str__(self, indent_level=0):
        return self.root.__str__(indent_level=0)

    def add_word(self, word:str):
        """Add the word once for each hook: first hook->beginning, then hook->end"""
        for hook_pos in range(1, len(word)):
            k = hook_pos
            front = ''.join(reversed(word[0:k]))
            back = ''.join(word[k:len(word)])
            string_loop = front + GNode.CHAR_REV + back
            self.root.add_string(string_loop)
        string_end = str(''.join(reversed(word)))
        self.root.add_string(string_end)

    def add_wordfile(self, filename: str):
        def is_line_valid(s):
            return all([ord('a') <= ord(c) <= ord('z') for c in s])

        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if is_line_valid(line):
                    word = line
                    self.add_word(word)

    def add_wordlist(self, words:List[str]):
        for word in words:
            self.add_word(word)

    # How much are we duplicating work across hooks? Any way to reduce effort?
    def find_moves(self, board: Board, rack: str)->Set[Move]:
        result = set()
        hooks = board.hooks()
        for hook in hooks:
            for bdir in [BoardDirection.LEFT, BoardDirection.UP]:
                found_moves = self.root.find_moves(move_acc, board, hook, bdir, rack)
                for move in found_moves:
                    result.add(move)
        return result

    def has_word(self, word)->bool:
        """Check to see if the given word is in the GTree.
        Useful to check whether secondary words created by a Move are valid."""
        if len(word) == 1:
            chars = word + GNode.CHAR_EOW
        else:
            chars = word[0] + GNode.CHAR_REV + word[1:] + GNode.CHAR_EOW
        cursor = self.root
        for c in chars:
            if c not in cursor.children:
                return False
            else:
                cursor = cursor.children[c]
        return True
