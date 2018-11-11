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

    # TODO: Delete. Now that search.py has been created, GNode.find_moves() and GTree.find_moves() are no longer called.
#    def find_moves(self, move_acc:Move, board:Board, cursor:Square, bdir:BoardDirection, rack:str):
#        """Recursively call down the Trie while searching for words that meet dictionary, rack, and board constraints.
#        Each call involves branching logic made at a single GNode.
#        Forming the primary word (see below) usually takes multiple recursive calls, in two phases:
#            - Phase 1: The cursor is moving from the original hook backward (LEFT/UP).
#            - Phase 2: The cursor is moving from the original hook forward (RIGHT/DOWN).
#        Phase 1 can "fork" a Phase 2 when a CHAR_BOW is reached and the search reaches: (a) the board edge, or (b) an empty square
#        Phase 2 can yield results when an CHAR_EOW is reached and the search reaches: (a) the board edge, or (b) an empty square
#
#        :param GNode self: This GNode
#        :param Move move_acc: The Move being formed while searching for all valid moves
#        :param Board board: The Board being used
#        :param Square cursor: The board square (cursor) currently being considered.
#        :param BoardDirection bdir: The BoardDirection being used
#        :param str rack: The (remaining) letters available for the player to use
#        :return: Iterable(move_acc), which has three attributes:
#            * played_letters: List[PlacedLetter]  # The letters placed on the board
#            * primary_word: PlacedWord            # The word formed by letters played & adjacent collinear letters on the board.
#            * secondary_words: List[PlacedWord]   # The secondary words formed, perpendicular to the primary word.
#                All words returned meet dictionary, board, & rack constraints.
#                Note: This function does not return the Move's score.
#        :rtype: Iterable[Move]
#        """
#        for child_gnode in self.children:  # Dictionary constraint
#            next_cursor = Util.add_sq_bdir(move_acc.primary_word.square_end, bdir)
#            if self.char == GNode.CHAR_EOW:
#                if (not board.is_square_on_board(next_cursor)) or (board[next_cursor] == Board.CHAR_EMPTY):
#                    pre_call_hash = hash((move_acc, board, cursor, bdir, rack))
#                    yield move_acc.copy()
#                    post_call_hash = hash((move_acc, board, cursor, bdir, rack))
#                    assert(pre_call_hash == post_call_hash)
#            elif self.char == GNode.CHAR_REV:
#                if (not board.is_square_on_board(next_cursor)) or (board[next_cursor] == Board.CHAR_EMPTY):
#                    rev_bdir = BoardDirection.reversed(bdir)
#                    next_cursor = Util.add_sq_bdir(move_acc.primary_word.square_end, rev_bdir)
#                    pre_call_hash = hash((move_acc, board, cursor, bdir, rack))
#
#                    yield from child_gnode.find_moves(
#                            move_acc.copy()
#                            , board
#                            , next_cursor
#                            , rev_bdir
#                            , Util.remove_char(rack, child_gnode.char)
#                            )
#                    post_call_hash = hash((move_acc, board, cursor, bdir, rack))
#                    assert(pre_call_hash == post_call_hash)
#            else:  # self.char is alphabetic
#                is_char_on_board = board[cursor] == child_gnode.char
#                if is_char_on_board:
#                    new_secondary_word = board.get_secondary_word(cursor, bdir, child_gnode.char)
#                    secondary_words_copy = [pw.copy() for pw in move_acc.secondary_words]
#                    next_secondary_words = (secondary_words_copy + [new_secondary_word] if new_secondary_word
#                                            else secondary_words_copy
#                                            )
#                    pre_call_hash = hash((move_acc, board, cursor, bdir, rack))
#                    yield from child_gnode.find_moves(
#                            Move([pl.copy() for pl in move_acc.placed_letters]
#                                , move_acc.primary_word.updated(cursor, bdir, child_gnode.char)
#                                , next_secondary_words
#                                )
#                            , board
#                            , Util.add_sq_bdir(cursor, bdir)
#                            , bdir
#                            , rack
#                            )
#                    post_call_hash = hash((move_acc, board, cursor, bdir, rack))
#                    assert(pre_call_hash == post_call_hash)
#                else:  # TODO: Unify character/blank cases into one
#                    is_char_in_rack = child_gnode.char in rack
#                    if is_char_in_rack:
#                        new_secondary_word = board.get_secondary_word(cursor, bdir, child_gnode.char)
#                        secondary_words_copy = [pw.copy() for pw in move_acc.secondary_words]
#                        next_secondary_words = (secondary_words_copy + [new_secondary_word] if new_secondary_word
#                                                else secondary_words_copy
#                                                )
#                        pre_call_hash = hash((move_acc, board, cursor, bdir, rack))
#                        yield from child_gnode.find_moves(
#                                Move([pl.copy() for pl in move_acc.placed_letters]
#                                        + [PlacedLetter(cursor, child_gnode.char)]
#                                    , move_acc.primary_word.updated(cursor, bdir, child_gnode.char)
#                                    , next_secondary_words
#                                    )
#                                , board
#                                , Util.add_sq_bdir(cursor, bdir)
#                                , bdir
#                                , Util.remove_char(rack, child_gnode.char)
#                                )
#                        post_call_hash = hash((move_acc, board, cursor, bdir, rack))
#                        assert(pre_call_hash == post_call_hash)
#                    is_blank_in_rack = GNode.CHAR_BLANK in rack
#                    if is_blank_in_rack:
#                        new_secondary_word = board.get_secondary_word(cursor, bdir, child_gnode.char.upper())  # Note: Blank-specific
#                        secondary_words_copy = [pw.copy() for pw in move_acc.secondary_words]
#                        next_secondary_words = (secondary_words_copy + [new_secondary_word] if new_secondary_word
#                                                else secondary_words_copy
#                                                )
#                        pre_call_hash = hash((move_acc, board, cursor, bdir, rack))
#                        yield from child_gnode.find_moves(
#                                Move([pl.copy() for pl in move_acc.placed_letters]
#                                    + [PlacedLetter(cursor, child_gnode.char.upper())]  # Note: Blank-specific
#                                    , move_acc.primary_word.updated(cursor, bdir, child_gnode.char)
#                                    , next_secondary_words
#                                    )
#                                , board
#                                , Util.add_sq_bdir(cursor, bdir)
#                                , bdir
#                                , Util.remove_char(rack, Bag.CHAR_BLANK)  # Note: Blank-specific
#                                )
#                        post_call_hash = hash((move_acc, board, cursor, bdir, rack))
#                        assert(pre_call_hash == post_call_hash)
# GTree is an implementation of a GADDAG: a type of Trie specialized for looking up words from a mid-word "hook".
# For more info, see https://en.wikipedia.org/wiki/GADDAG


class GTree:
    VERBOSE = False

    def __init__(self, filename=None):
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
            return all([ord('a') < ord(c) < ord('z') for c in s])

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
