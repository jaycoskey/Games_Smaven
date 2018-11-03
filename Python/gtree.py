#!/usr/bin/env python

from board import Board, BoardDirection
from move import Move, PlacedLetter, PlacedWord
from typing import List
from util import Square


# A node in a GADDAG. (See the Wikipedia page for GADDAG.)
# TODO: Support serialization & deserialization.
class GNode:
    # CHAR_BOW marks the beginning of a word in a Trie (e.g., can happen when the hook is the end of a word)
    # Note: The path traversed from the root to a GNode with CHAR_BOW spells out the beginning of the word in reverse.
    CHAR_BOW = '^'

    # CHAR_EOW marks the end of a word. Note that other words might continue down the trie (e.g., win & winsome).
    CHAR_EOW = '$'

    # CHAR_REV marks the end of the reversed portion of word traveral. (See the GADDAG Wikipedia page.)
    CHAR_REV = '+'

    # CHAR_ROOT is the char of the root of the Trie.
    CHAR_ROOT = '*'

    def __init__(self, char:str):
        self.char = char
        self.children = {}

    def add_child(char:str)->'GNode':
        child = GNode(char)
        self.children[char] = child
        return child

    def add_word(self, word):
        """TODO: Add addition of word at all hooks"""
        if word == '':
            child = self.add_child(GNode.CHAR_EOW)
        else:
            child = self.add_child(word[0])
            child.add_word(word[1:])

    def find_words(self, move_acc:Move, board:Board, bdir:BoardDirection, cursor:Square, rack:str):
        """Recursively call down the Trie while searching for words that meet dictionary, rack, and board constraints.
        Each call involves branching logic made at a single GNode.
        Forming the primary word (see below) usually takes multiple recursive calls, in two phases:
            - Phase 1: The cursor is moving from the original hook backward (LEFT/UP).
            - Phase 2: The cursor is moving from the original hook forward (RIGHT/DOWN).
        Phase 1 can "fork" a Phase 2 when a CHAR_REV is reached and the search reaches: (a) the board edge, or (b) an empty square
        Phase 2 can yield results when an CHAR_EOW is reached and the search reaches: (a) the board edge, or (b) an empty square

        :param GNode self: This GNode
        :param Move move_acc: The Move being formed while searching for all valid moves
        :param Board board: The Board being used
        :param BoardDirection bdir: The BoardDirection being used
        :param Square cursor: The board square (cursor) currently being considered.
        :param str rack: The (remaining) letters available for the player to use
        :return: move_acc, which has three attributes:
            * played_letters: List[PlacedLetter]  # The letters placed on the board
            * primary_word: PlacedWord            # The word formed by letters played & adjacent collinear letters on the board.
            * secondary_words: List[PlacedWord]   # The secondary words formed, perpendicular to the primary word.
                All words returned meet dictionary, board, & rack constraints.
                Note: This function does not return the Move's score.
        :rtype: Move
        """
        # TODO: When to re-use args vs when to clone? If only one recursive call is made from this one,
        #       or if multiple calls are made in series, then we don't need to make copies of the arguments.
        #
        for child_gnode in self.children:  # Dictionary constraint
            if self.char == GNode.CHAR_BOW:  #  TODO: ... and (Util.add_sq_bdir(cursor, bdir) is not another letter on the board):
                yield move_acc
            if self.char == GNode.CHAR_REV:  # TODO: ... and (Util.add_sq_bdir(cursor, bdir) is not another letter on the board):
                bdir = BoardDirection.reversed(bdir)
                # TODO: ... send off probe in new direction ...
            if self.char == GNode.CHAR_EOW:  # TODO: ... and (Util.add_sq_bdir(cursor, bdir) is not another letter on the board):
                pass # TODO ...
            if child_gnode.char in rack:  # TODO: ... or on board:  # Rack/Board constraint
                move_acc.placed_letters_acc = None  # TODO ...
                move_acc.primary_word_acc = None  # TODO ...
                move_acc.secondary_words_acc = None  # TODO ...
                # board does not need to be updated
                # bdir is not updated here
                next_cursor = Util.add_sq_bdir(hook, bdir)
                rack = None  # TODO...

                next_bdir = BoardDirection.reverse(bdir) if cur_char == GNode.CHAR_REV else bdir

                next_rack = rack  # TODO ... with current character removed
                # Note: No need to update board
                yield from child_gnode.find_words(move_acc, board, bdir, next_cursor, next_rack)


# GTree is an implementation of a GADDAG: a type of Trie specialized for looking up words from a mid-word "hook".
# For more info, see https://en.wikipedia.org/wiki/GADDAG
class GTree:
    def __init__(self):
        self.root = GNode(GNode.CHAR_ROOT)

    def add_word(self, word:str):
        self.root.add_word(word)

    def add_wordlist(self, filename: str):
        def is_line_valid(s):
            return all([ord('a') < ord(c) < ord('z') for c in s])

            with open(filename, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    if is_line_valid(line):
                        word = line
                        self.add_word(word)

    def has_word(self, word)->bool:
        """Check to see if the given word is in the GTree.
        This is used to check whether secondary words created by a Move are valid."""
        pass

    # How much are we duplicating work across hooks? Any way to reduce effort?
    def find_words(self, board: Board, rack: str)->List[PlacedWord]:
        words = set()
        hooks = board.get_hooks()
        for hook in hooks:
            for brddir in [BoardDirection.LEFT, BoardDirection.UP]:
                # Find words from this hook; move to beginning on word in this board direction
                # TODO: move_acc = ...
                found_words = self.root.find_words(move_acc, board, bdir, hook, rack)
                for word in found_words:
                    words.add(word)
        return words
