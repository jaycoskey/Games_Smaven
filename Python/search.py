#!/usr/bin/env python

from board import Board
from board_direction import BoardDirection
from move import PlacedLetter
from game import Bag
from gtree import GNode
from util import Square, Util


# Add copying to the appropriate places to avoid aliasing
class Search:
    def __init__(self, gtree, board):
        self.gtree = gtree
        self.board = board

    def find_moves(self, rack):
        result = []
        for hook in self.board.hooks():
            for bdir in [BoardDirection.LEFT, BoardDirection.UP]:
                found_hook_bdir = self.find_moves_hook_bdir(hook, bdir, rack)
                result.extend(found_hook_bdir)
        return result

    def find_moves_hook_bdir(self, hook, bdir, rack):
        for node in self.gtree.root.children:
            ss = SearchState([], node, hook, bdir, rack)
            yield from find_moves_ss(ss)

    def find_moves_ss(self, ss):
        if ss.node.char == GNode.CHAR_EOW:
            if not ss.is_next_square_letter(self.board):
                yield move_acc.copy()
        elif ss.node.char == GNode.CHAR_REV:
            if not ss.is_next_square_letter(self.board):
                yield from self.find_moves_ss(ss.reverse())
        else:  # node.char is alphabetic
            is_char_on_board = self.board[cursor] == ss.node.char
            if is_char_on_board:
                yield from self.find_moves_ss(ss.update_char_on_board(board))
            else:
                is_char_in_rack = ss.node.char in ss.rack
                if is_char_in_rack:
                    yield from self.find_moves_ss(ss.update_char_in_rack(board))

                is_blank_in_rack = GNode.CHAR_BLANK in ss.rack
                if is_blank_in_rack:
                    yield from self.find_moves_ss(ss.update_blank_in_rack(board))

    def get_secondary_words(self, gtree, board, placed_letters, primary_word):
        # TODO: Get direction of primary_word
        result = []
        ss = SearchState(...)
        for pl in placed_letters:
            sw = ss.get_secondary_word(gtree, board)
            if sw:
                result.append(sw)
        return result

class SearchState:
    def __init__(self, move_acc, node, cursor, bdir, rack):
        self.move_acc = move_acc
        self.node = node
        self.cursor = cursor
        self.bdir = bdir
        self.rack = rack

    def __eq__(self, other):  # For unit tests
        return (self.move_acc == other.move_acc
                and self.node == other.node
                and self.cursor == other.cursor
                and self.bdir == other.bdir
                and self.rack == other.rack
                )

    def __str__(self):
        return (f'SearchState<move_acc={self.move_acc}, cursor={Util.sq2str(self.cursor)}, '
                + f'bdir={self.bdir}, rack="{self.rack}", node={self.node}>'
                )

    def copy(self):
        return SearchState(
                [m.copy() for m in self.move_acc]
                , self.node.copy()
                , self.cursor.copy()
                , self.bdir
                , self.rack
                )

    def get_secondary_word(self, gtree, board):
        if self.bdir in [BoardDirection.LEFT, BoardDirection.RIGHT]:
            back = BoardDirection.UP
        else:
            back = BoardDirection.LEFT
        forward = BoardDirection.reversed(back)

        begin = self.cursor
        end = self.cursor
        word = board[self.cursor]

        while True:
            next_begin = Util.add_sq_bdir(begin, back)
            if board.is_square_on_board(next_begin) and not board.is_square_empty(next_begin):
                begin = next_begin
                word = board[begin] + word
            else:
                break
        while True:
            next_end = Util.add_sq_bdir(end, forward)
            if board.is_square_on_board(next_end) and not  board.is_char_empty(next_end):
                end = next_end
                word = word + board[end]
            else:
                break
        if gtree.has_word(word):
            return PlacedWord(begin, end, word)

    def is_next_cursor_letter(self, board):
        sq = self.next_cursor(board)
        return sq is not None and board[sq] != Board.CHAR_EMPTY

    def next_cursor(self, board):
        """Return self.cursor + self.bdir if result is on board"""
        sq = Square(self.cursor.x + self.bdir.value[0], self.cursor.y + self.bdir.value[1])
        return sq if board.is_square_on_board(sq) else None

    def reverse(self, board):
        self.cursor = move_acc.placed_letters[0].square
        self.bdir = BoardDirection.reversed(self.bdir)
        self.cursor = self.next_cursor(board)

    def update_blank_in_rack(self, gtree, board):
        self.move_acc.placed_letters.append(PlacedLetter(self.cursor, self.node.char.upper()))
        self.move_acc.primary_word = self.move_acc.primary_word.updated(
                self.cursor
                , self.bdir
                , board[self.cursor]
                )
        new_secondary_word = self.get_secondary_word(gtree, board)
        if new_secondary_word:
            self.move_acc.secondary_words.append(new_secondary_word)
        self.cursor = self.next_cursor(board)
        self.rack = Util.remove_char(self.rack, Bag.CHAR_BLANK)

    def update_char_in_rack(self, board):
        self.move_acc.placed_letters.extend(PlacedLetter(cursor, node.char()))
        self.move_acc.primary_word = self.move_acc.primary_word.updated(self.cursor, self.bdir, board[self.cursor])
        new_secondary_word = board.get_secondary_word(self.cursor, self.bdir, self.node.char)
        if new_secondary_word:
            self.move_acc.secondary_words.append(new_secondary_word)
        self.cursor = self.next_cursor(board)
        self.rack = Util.remove_char(self.rack, node.char)

    def update_char_on_board(self, board):
        # Do not update placed_letters
        self.move_acc.primary_word = self.move_acc.primary_word.updated(self.cursor, self.bdir, board[self.cursor])
        # Do not update secondary_word
        self.cursor = self.next_cursor(board)
        # Do not update rack
