#!/usr/bin/env python

from board import Board, BoardDirection
from move import Move, PlacedLetter, PlacedWord
from typing import Iterable, List
from util import Square


# A node in a GADDAG. (See the Wikipedia page for GADDAG.)
# TODO: Support serialization & deserialization.
class GNode:
    # CHAR_EOW marks the end of a word, though other words might continue on (e.g. win/winsome).
    CHAR_EOW = '$'

    # CHAR_REV marks the end of the reversed portion of word traveral. (See the GADDAG Wikipedia page.)
    CHAR_REV = '+'

    # CHAR_ROOT is the char of the root of the Trie.
    CHAR_ROOT = '*'

    def __init__(self, char:str):
        self.char = char
        self.children:Dict[str, GNode] = {}

    def add_child(char:str)->'GNode':
        child = GNode(char)
        self.children[char] = child
        return child

    def add_string(self, s):
        """Add a string to the subtree based at this GNode. Can contain content characters and CHAR_REV."""
        if s == '':
            # Reached the end of the string. Add the EOW char.
            child = self.add_child(GNode.CHAR_EOW)
        else:
            # Add the next char, and continue recursively.
            child = self.add_child(s[0])
            child.add_word(s[1:])

    def find_words(self, move_acc:Move, board:Board, bdir:BoardDirection, cursor:Square, rack:str):
        """Recursively call down the Trie while searching for words that meet dictionary, rack, and board constraints.
        Each call involves branching logic made at a single GNode.
        Forming the primary word (see below) usually takes multiple recursive calls, in two phases:
            - Phase 1: The cursor is moving from the original hook backward (LEFT/UP).
            - Phase 2: The cursor is moving from the original hook forward (RIGHT/DOWN).
        Phase 1 can "fork" a Phase 2 when a CHAR_BOW is reached and the search reaches: (a) the board edge, or (b) an empty square
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
        :rtype: Iterable[Move]
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
        """Add the word once for each hook: first hook->beginning, then hook->end"""
        for hook_pos in range(len(word)):
            for k in range(hook_pos, -1, -1):
                front = reversed(word[0:k])
                back = word[k:len(word)]
                self.root.add_string(front + CHAR_REV + back)
        self.root.add_string(reversed(word))

    def add_wordlist(self, filename: str):
        def is_line_valid(s):
            return all([ord('a') < ord(c) < ord('z') for c in s])

        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if is_line_valid(line):
                    word = line
                    self.add_word(word)

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

    def has_word(self, word)->bool:
        """Check to see if the given word is in the GTree.
        Useful to check whether secondary words created by a Move are valid."""
        cursor = self.root
        for c in word:
            if c in cursor.children:
                cursor = cursor[c]
            else:
                return False
        return GNode.CHAR_EOW in cursor.children
