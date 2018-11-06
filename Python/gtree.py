#!/usr/bin/env python

from board import Board, BoardDirection
from move import Move, PlacedLetter, PlacedWord
from typing import Iterable, List
from util import Square


# A node in a GADDAG. (See the Wikipedia page for GADDAG.)
# TODO: Support serialization & deserialization.
class GNode:
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

    def __str__(self, indent_level=0, label=''):
        indent_str = '  '
        result = (
            f'{indent_str * indent_level}{label}{self.data}\n'
            + '\n'.join([c.__str__(indent_level + 1, label=c.char) for c in self.children])
            )

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

    # TODO: Eliminate duplication? Words spanning from one hook to another are found twice---once from each direction.
    def find_words(self, move_acc:Move, board:Board, cursor:Square, bdir:BoardDirection, rack:str):
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
        :param Square cursor: The board square (cursor) currently being considered.
        :param BoardDirection bdir: The BoardDirection being used
        :param str rack: The (remaining) letters available for the player to use
        :return: Iterable(move_acc), which has three attributes:
            * played_letters: List[PlacedLetter]  # The letters placed on the board
            * primary_word: PlacedWord            # The word formed by letters played & adjacent collinear letters on the board.
            * secondary_words: List[PlacedWord]   # The secondary words formed, perpendicular to the primary word.
                All words returned meet dictionary, board, & rack constraints.
                Note: This function does not return the Move's score.
        :rtype: Iterable[Move]
        """
        for child_gnode in self.children:  # Dictionary constraint
            next_cursor = Util.add_sq_bdir(move_acc.primary_word.square_end, bdir)
            if self.char == GNode.CHAR_EOW:
                if (not board.is_square_on_board(next_cursor)) or (board[next_cursor] == Board.CHAR_EMPTY):
                    pre_call_hash = hash((move_acc, board, cursor, bdir, rack))
                    yield move_acc  # TODO
                    post_call_hash = hash((move_acc, board, cursor, bdir, rack))
                    assert(pre_call_hash == post_call_hash)
            elif self.char == GNode.CHAR_REV:
                if (not board.is_square_on_board(next_cursor)) or (board[next_cursor] == Board.CHAR_EMPTY):
                    rev_bdir = BoardDirection.reversed(bdir)
                    next_cursor = Util.add_sq_bdir(move_acc.primary_word.square_end, rev_bdir)
                    pre_call_hash = hash((move_acc, board, cursor, bdir, rack))

                    yield from child_gnode.find_words(  # TODO
                            move_acc
                            , board
                            , next_cursor
                            , rev_bdir
                            , Util.removed_char_from_rack(rack, child_gnode.char)
                            )
                    post_call_hash = hash((move_acc, board, cursor, bdir, rack))
                    assert(pre_call_hash == post_call_hash)
            else:  # self.char is alphabetic
                is_char_on_board = board[cursor] == child_gnode.char
                if is_char_on_board:
                    next_primary_word = move_acc.primary_word.updated(cursor, bdir, child_gnode.char)
                    new_secondary_words = board.get_secondary_words(cursor, bdir, child_gnode.char)
                    pre_call_hash = hash((move_acc, board, cursor, bdir, rack))
                    yield from child_gnode.find_words(  # TODO
                            Move(move_acc.placed_letters
                                , next_primary_word
                                , move_acc.secondary_words + new_secondary_words
                                )
                            , board
                            , Util.add_sq_bdir(cursor, bdir)
                            , bdir
                            , rack
                            )
                    post_call_hash = hash((move_acc, board, cursor, bdir, rack))
                    assert(pre_call_hash == post_call_hash)
                else:
                    is_char_in_rack = child_gnode.char in rack
                    if is_char_in_rack:
                        next_primary_word = move_acc.primary_word.updated(cursor, bdir, child_gnode.char)
                        new_secondary_words = board.get_secondary_words(cursor, bdir, child_gnode.char)
                        pre_call_hash = hash((move_acc, board, cursor, bdir, rack))
                        yield from child_gnode.find_words(  # TODO
                                Move(move_acc.placed_letters + [PlacedLetter(cursor, child_gnode.char)]
                                    , next_primary_word
                                    , move_acc.secondary_words + new_secondary_words
                                    )
                                , board
                                , Util.add_sq_bdir(cursor, bdir)
                                , bdir
                                , Util.removed_char(rack, child_gnode.char)
                                )
                        post_call_hash = hash((move_acc, board, cursor, bdir, rack))
                        assert(pre_call_hash == post_call_hash)
                    is_blank_in_rack = GNode.CHAR_BLANK in rack
                    if is_blank_in_rack:
                        next_primary_word = move_acc.primary_word.updated(cursor, bdir, child_gnode.char)
                        new_secondary_words = board.get_secondary_words(cursor, bdir, child_gnode.char)
                        pre_call_hash = hash((move_acc, board, cursor, bdir, rack))
                        yield from child_gnode.find_words(  # TODO
                                Move(move_acc.placed_letters + [PlacedLetter(cursor, child_gnode.char)]
                                    , next_primary_word
                                    , move_acc.secondary_words + new_secondary_words
                                    )
                                , board
                                , Util.add_sq_bdir(cursor, bdir)
                                , bdir
                                , Util.removed_char(rack, child_gnode.char)
                                )
                        post_call_hash = hash((move_acc, board, cursor, bdir, rack))
                        assert(pre_call_hash == post_call_hash)


# GTree is an implementation of a GADDAG: a type of Trie specialized for looking up words from a mid-word "hook".
# For more info, see https://en.wikipedia.org/wiki/GADDAG
class GTree:
    def __init__(self):
        self.root = GNode(GNode.CHAR_ROOT)

    def __str__(self, indent_level=0, label=''):
        return self.root.__str__(indent_level=0, label='')

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
            for bdir in [BoardDirection.LEFT, BoardDirection.UP]:
                # Find words from this hook; move to beginning on word in this board direction
                # TODO: move_acc = ...
                found_words = self.root.find_words(move_acc, board, hook, bdir, rack)
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
