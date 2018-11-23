#!/usr/bin/env python


from bag import Bag
from board import Board
from board_direction import BoardDirection
from move import Move, PlacedLetter, PlacedWord
from gtree import GNode
from typing import Iterable, List
from util import Cell, Util


# Add copying to the appropriate places to avoid aliasing
class Search:
    def __init__(self, gtree, board):
        self.gtree = gtree
        self.board = board

    def find_moves(self, rack)->List[Move]:
        result = []
        for hook in self.board.hooks():
            for bdir in [BoardDirection.LEFT, BoardDirection.UP]:
                found_hook_bdir = self.find_moves_hook_bdir(hook, bdir, rack)
                result.extend(found_hook_bdir)
        return result

    def find_moves_hook_bdir(self, hook, bdir, rack)->Iterable[Move]:
        for node in self.gtree.root.children.values():
            placed_letters = []
            primary_word = PlacedWord(hook, hook, '')
            secondary_words = []
            move_acc = Move(placed_letters, primary_word, secondary_words)
            ss = SearchState(move_acc, node, hook, bdir, rack)
            yield from self.find_moves_ss(ss)

    def find_moves_ss(self, ss)->Iterable[Move]:
        if ss.cursor is None:
            return
        if ss.node.char == GNode.CHAR_EOW:
            if not ss.is_next_cell_letter(self.board):
                yield move_acc.copy()
        elif ss.node.char == GNode.CHAR_REV:
            if not ss.is_next_cell_letter(self.board):
                yield from self.find_moves_ss(ss.reverse_search_direction())
        else:  # node.char is alphabetic
            is_char_on_board = self.board[ss.cursor] == ss.node.char
            if is_char_on_board:
                ss.update_char_on_board(self.board)
                if ss.cursor:
                    yield from self.find_moves_ss(ss)
            else:
                is_char_in_rack = ss.node.char in ss.rack
                if is_char_in_rack:
                    ss.update_char_in_rack(self.gtree, self.board)
                    if ss.cursor:
                        yield from self.find_moves_ss(ss)

                is_blank_in_rack = GNode.CHAR_BLANK in ss.rack
                if is_blank_in_rack:
                    yield from self.find_moves_ss(ss.update_blank_in_rack(self.board))

    def get_secondary_words(self, placed_letters, primary_word, rack, do_update_move_acc=True):
        cell_beg = primary_word.cell_begin
        cell_end = primary_word.cell_end
        primary_bdir = BoardDirection.LEFT if cell_beg.y == cell_end.y else BoardDirection.UP

        result = []
        for pl in placed_letters:
            if pl.char not in self.gtree.root.children:
                continue
            if do_update_move_acc:
                move_acc = Move(placed_letters, primary_word, [])
            else:
                move_acc = None
            node = self.gtree.root.children[pl.char]
            cursor = pl.cell
            ss = SearchState(move_acc, node, cursor, primary_bdir, rack)
            sw = ss.get_secondary_word(self.gtree, self.board)
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
        return (f'SearchState<move_acc={self.move_acc}, cursor={Util.cell2str(self.cursor)}, '
                + f'bdir={self.bdir}, rack="{self.rack}", node={self.node}>'
                )

    def copy(self):
        return SearchState(
                self.move_acc.copy()
                , self.node.copy()
                , Util.cell_copy(self.cursor)
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
            next_begin = Util.add_cell_bdir(begin, back)
            if board.is_cell_on_board(next_begin) and not board.is_cell_empty(next_begin):
                begin = next_begin
                word = board[begin] + word
            else:
                break
        while True:
            next_end = Util.add_cell_bdir(end, forward)
            if board.is_cell_on_board(next_end) and not  board.is_cell_empty(next_end):
                end = next_end
                word = word + board[end]
            else:
                break
        if gtree.has_word(word):
            return PlacedWord(begin, end, word)

    def is_next_cursor_letter(self, board):
        cell = self.next_cursor(board)
        return cell is not None and board[cell] != Board.CHAR_EMPTY

    def next_cursor(self, board):
        """Return self.cursor + self.bdir if result is on board"""
        cell = Cell(self.cursor.x + self.bdir.value[0], self.cursor.y + self.bdir.value[1])
        return cell if board.is_cell_on_board(cell) else None

    def reverse_search_direction(self, board, do_copy=False):
        ss = self.copy() if do_copy else self
        ss.cursor = move_acc.placed_letters[0].cell
        ss.bdir = BoardDirection.reversed(ss.bdir)
        ss.cursor = ss.next_cursor(board)

    def update_blank_in_rack(self, gtree, board, do_copy=False)->'SearchState':
        assert(Bag.CHAR_BLANK in self.rack)
        ss = self.copy() if do_copy else self
        ss.move_acc.placed_letters.append(PlacedLetter(ss.cursor, ss.node.char.upper()))
        ss.move_acc.primary_word = ss.move_acc.primary_word.updated(
                ss.cursor
                , ss.bdir
                , ss.node.char.upper()
                )
        new_secondary_word = ss.get_secondary_word(gtree, board)
        if new_secondary_word:
            ss.move_acc.secondary_words.append(new_secondary_word)
        ss.cursor = ss.next_cursor(board)
        ss.rack = Util.remove_char(ss.rack, Bag.CHAR_BLANK)
        return ss if do_copy else None

    def update_char_in_rack(self, gtree, board, do_copy=False)->'SearchState':
        assert(self.node.char in self.rack)
        ss = self.copy() if do_copy else self
        ss.move_acc.placed_letters.append(PlacedLetter(ss.cursor, ss.node.char))
        ss.move_acc.primary_word = ss.move_acc.primary_word.updated(
                                        ss.cursor
                                        , ss.bdir
                                        , ss.node.char
                                        )
        new_secondary_word = ss.get_secondary_word(gtree, board)
        if new_secondary_word:
            ss.move_acc.secondary_words.append(new_secondary_word)
        ss.cursor = ss.next_cursor(board)
        ss.rack = Util.remove_char(ss.rack, ss.node.char)
        return ss if do_copy else None

    def update_char_on_board(self, board, do_copy=False)->'SearchState':
        assert(board[self.cursor] == self.node.char)
        ss = self.copy() if do_copy else self
        # Do not update placed_letters
        ss.move_acc.primary_word = ss.move_acc.primary_word.updated(ss.cursor, ss.bdir, board[ss.cursor])
        # Do not update secondary_word
        ss.cursor = ss.next_cursor(board)
        # Do not update rack
        return ss if do_copy else None
