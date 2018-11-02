#!/usr/bin/env python

# A node in a GADDAG
# TODO: Support serialization & deserialization.
class GNode:
    # BOW_CHAR = '^'  # Mark the beginning of a word in a Trie (e.g., can happen when the hook is the end of a word)
    #                   The path traversed this far spells out a word in reverse.
    # EOW_CHAR = '$'  # Mark the end of a word in a Trie. Might not be a leaf (e.g., win & winsome).
    #                   The path traversed this far spells out a word, once the first half (before the REV_CHAR) is reversed.
    # REV_CHAR = '+'  # Mark the end of the reversed portion of word traveral. (See the GADDAG Wikipedia page.)
    # TODO: self.value: str
    # TODO: self.children: Map[str, List[GNode]]
    # TODO: def add_child(letter: str): GNode

    # def add_word(self, word):
    #     """TODO: Add addition of word at all hooks"""
    #     if word = '':
    #         child = self.add_child(GNode.EOW_CHAR)
    #     else:
    #         child = self.add_child(word[0])
    #         child.add_word(word[1:])
    #
    # def find_words( self, move_acc: Move, board: Board, bdir: BoardDirection, cursor: Square, rack: str)
    #     """Recursively call down the Trie while searching for words that meet dictionary, rack, and board constraints.
    #     Each call involves branching logic made at a single GNode.
    #     Forming the primary word (see below) usually takes multiple recursive calls, in two phases:
    #       - Phase 1: The cursor is moving from the original hook backward (LEFT/UP).
    #       - Phase 2: The cursor is moving from the original hook forward (RIGHT/DOWN).
    #     Phase 1 can "fork" a Phase 2 when a REV_CHAR is reached and the search reaches: (a) the board edge, or (b) an empty square
    #     Phase 2 can yield results when an EOW_CHAR is reached and the search reaches: (a) the board edge, or (b) an empty square
    #
    #     :param GNode self: This GNode
    #     :param Move move_acc: The Move being formed while searching for all valid moves
    #     :param Board board: The Board being used
    #     :param BoardDirection bdir: The BoardDirection being used
    #     :param Square cursor: The board square (cursor) currently being considered.
    #     :param str rack: The (remaining) letters available for the player to use
    #     :return: move_acc, which has three attributes:
    #                * played_letters: List[PlacedLetter]  # The letters placed on the board
    #                * primary_word: PlacedWord            # The word formed by letters played & adjacent collinear letters on the board.
    #                * secondary_words: List[PlacedWord]   # The secondary words formed, perpendicular to the primary word.
    #              All words returned meet dictionary, board, & rack constraints.
    #              Note: This function does not return the Move's score.
    #     :rtype: Move
    #     """
    #     # TODO: When to re-use args vs when to clone? If only one recursive call is made from this one,
    #     #       or if multiple calls are made in series, then we don't need to make copies of the arguments.
    #     #
    #     for child_gnode in self.children:  # Dictionary constraint
    #         if self.value == GNode.BOW_CHAR and (cursor + bdir is not another letter on the board):
    #             yield move_acc
    #         if self.value == GNode.REV_CHAR and (cursor + bdir is not another letter on the board):
    #             bdir = BoardDirection.reversed(bdir)
    #             ... send off probe in new direction ...
    #         if self.value == GNode.EOW_CHAR and (cursor + bdir is not another letter on the board):
    #             ...
    #         if child_gnode in rack or on board:  # Rack/Board constraint
    #             move_acc.placed_letters_acc = ...
    #             move_acc.primary_word_acc = ...
    #             move_acc.secondary_words_acc = ...
    #             # board does not need to be updated
    #             # bdir is not updated here
    #             next_cursor = hook + bdir
    #             rack = ...
    #
    #             next_bdir = BoardDirection.reverse(bdir) if cur_char == GNode.REV_CHAR else bdir
    #
    #             next_rack = rack with current character removed
    #             # Note: No need to update board
    #             yield from child_gnode.find_words(move_acc, board, bdir, next_cursor, next_rack)
    pass


# GTree is an implementation of a GADDAG: a type of Trie specialized for looking up words from a mid-word "hook".
# For more info, see https://en.wikipedia.org/wiki/GADDAG
class GTree:
    # TODO: self.root: GNode

    # def add_word(self, word: str)
    # def add_wordlist(self, filename: str)
    #     def is_valid(s):
    #         return all([ord('a') < ord(c) < ord('z') for c in s])
    #
    #     with open(filename, 'r') as f:
    #         for line in f.readlines():
    #             line = line.strip()
    #             if is_valid(line):
    #                 word = line
    #                 self.add_word(word)

    # def has_words(self, word): bool
    #     """Check to see if the given word is in the GTree.
    #     This is used to check whether secondary words created by a Move are valid."""
    #     pass
    #
    # # How much are we duplicating work across hooks? Any way to reduce effort?
    # def find_words(self, board: Board, rack: str): List[PlacedWords]
    #     words = set()
    #     hooks = board.get_hooks()
    #     for hook in hooks:
    #         for brddir in [BoardDirection.LEFT, BoardDirection.UP]:
    #             # Find words from this hook; move to beginning on word in this board direction
    #             move_acc = ...
    #             found_words = self.root.find_words(move_acc, board, bdir, hook, rack)
    #             for word in found_words:
    #                 words.add(word)
    #     return words
    pass
