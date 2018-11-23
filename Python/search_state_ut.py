#!/usr/bin/env python

import unittest
import yaml
import sys


from bag import Bag
from board import Board
from board_direction import BoardDirection
from gtree import GNode, GTree
from move import Move, PlacedLetter, PlacedWord
from search import SearchState
from util import Cell, Util


class TestSearchState(unittest.TestCase):
    VERBOSE = True

    @staticmethod
    def get_config():
        filename = 'test_search_state.yml'
        with open(filename, 'r') as stream:
            config = yaml.load(stream)
            return config

    def test_is_next_cursor_letter(self, verbose=VERBOSE):
        if verbose:
            print(f'\n\n===Test: {get_function_name()} ===')

        config = TestSearchState.get_config()
        test_board_jay = Board(config, None, Util.get_rows_from_config(config['test_board_jay']))

        dummy_move_acc = []
        dummy_node = None
        dummy_bdir = BoardDirection.NO_DIR
        dummy_rack = ''
        ss = SearchState(dummy_move_acc, dummy_node, Cell(1, 0), dummy_bdir, '')

        ss.bdir = BoardDirection.LEFT
        is_left_char = ss.is_next_cursor_letter(test_board_jay)

        ss.bdir = BoardDirection.RIGHT
        is_right_char = ss.is_next_cursor_letter(test_board_jay)

        ss.bdir = BoardDirection.UP
        is_up_char = ss.is_next_cursor_letter(test_board_jay)

        ss.bdir = BoardDirection.DOWN
        is_down_char = ss.is_next_cursor_letter(test_board_jay)

        lhs = (is_left_char, is_right_char, is_up_char, is_down_char)
        rhs = (True, True, False, False)
        if verbose and lhs != rhs:
            print(f'test_is_next_cursor_letter: Unexpected inequality:\n\t==>{lhs}\n\t   !=\n\t{rhs}')
        assert(lhs == rhs)

    def test_next_cursor(self, verbose=VERBOSE):
        if verbose:
            print(f'\n\n===Test: {get_function_name()} ===')

        config = TestSearchState.get_config()
        test_board_jay = Board(config, None, Util.get_rows_from_config(config['test_board_jay']))

        dummy_move_acc = []
        dummy_node = None
        cursor = Cell(1, 0)
        dummy_bdir = BoardDirection.NO_DIR
        dummy_rack = ''
        ss = SearchState(dummy_move_acc, dummy_node, cursor, dummy_bdir, dummy_rack)

        ss.bdir = BoardDirection.LEFT
        left = ss.next_cursor(test_board_jay)

        ss.bdir = BoardDirection.RIGHT
        right = ss.next_cursor(test_board_jay)

        ss.bdir = BoardDirection.UP
        up = ss.next_cursor(test_board_jay)

        ss.bdir = BoardDirection.DOWN
        down = ss.next_cursor(test_board_jay)

        lhs = [left, right, up, down]
        rhs = [Cell(0, 0), Cell(2, 0), None, Cell(1, 1)]
        assert(lhs == rhs)

    def test_reverse(self, verbose=VERBOSE):
        if verbose:
            print(f'\n\n===Test: {get_function_name()} ===')

        config = TestSearchState.get_config()
        test_board_jay = Board(config, None, Util.get_rows_from_config(config['test_board_jay']))

    def test_update_blank_in_rack(self, verbose=VERBOSE):
        if verbose:
            print(f'\n\n===Test: {get_function_name()} ===')

        config = TestSearchState.get_config()
        test_board_jay = Board(config, None, Util.get_rows_from_config(config['test_board_jay']))

        gtree = GTree()
        gtree.add_word('jay')
        node_j = gtree.root.children['j']
        rev = node_j.children[GNode.CHAR_REV]
        node_a = rev.children['a']
        node_y = node_a.children['y']

        move_placed_letters = [PlacedLetter(Cell(0, 0), 'j')]
        move_primary_word = PlacedWord(Cell(0, 0), Cell(0, 0), 'j')
        move_secondary_words = []
        move_acc = Move(move_placed_letters, move_primary_word, move_secondary_words)

        cursor = Cell(1, 0)
        bdir = BoardDirection.RIGHT
        rack = Bag.CHAR_BLANK
        assert(type(node_a).__name__ == 'GNode')
        ss = SearchState(move_acc, node_a, cursor, bdir, rack)
        ss.update_blank_in_rack(gtree, test_board_jay)

        other = SearchState(
                    Move([PlacedLetter(Cell(0, 0), 'j')
                            , PlacedLetter(Cell(1, 0), 'A')]
                        , PlacedWord(Cell(0, 0), Cell(1, 0), 'jA')
                        , []
                        )
                    , node_a
                    , Cell(2, 0)
                    , BoardDirection.RIGHT
                    , ''
                    )

        if verbose and ss != other:
            print(f'test_update_blank_in_rack: Unexpected inequality:\n\t==>{ss}\n\t   !=\n\t===>{other}')
        assert(ss == other)

    def test_update_char_in_rack(self, verbose=VERBOSE):
        if verbose:
            print(f'\n\n===Test: {get_function_name()} ===')

        config = TestSearchState.get_config()
        test_board_jay = Board(config, None, Util.get_rows_from_config(config['test_board_jay']))

        gtree = GTree()
        gtree.add_word('jay')
        node_j = gtree.root.children['j']
        rev = node_j.children[GNode.CHAR_REV]
        node_a = rev.children['a']
        node_y = node_a.children['y']

        move_placed_letters = [PlacedLetter(Cell(0, 0), 'j')]
        move_primary_word = PlacedWord(Cell(0, 0), Cell(0, 0), 'j')
        move_secondary_words = []
        move_acc = Move(move_placed_letters, move_primary_word, move_secondary_words)

        cursor = Cell(1, 0)
        bdir = BoardDirection.RIGHT
        rack = 'a'
        ss = SearchState(move_acc, node_a, cursor, bdir, rack)
        ss.update_char_in_rack(gtree, test_board_jay)

        other = SearchState(
                    Move([PlacedLetter(Cell(0, 0), 'j')
                            , PlacedLetter(Cell(1, 0), 'a')]
                        , PlacedWord(Cell(0, 0), Cell(1, 0), 'ja')
                        , []
                        )
                    , node_a
                    , Cell(2, 0)
                    , BoardDirection.RIGHT
                    , ''
                    )

        if verbose and ss != other:
            print(f'test_update_char_in_rack: Unexpected inequality:\n\t{ss}\n\t   !=\n\t==>{other}')
        assert(ss == other)

    def test_update_char_on_board(self, verbose=VERBOSE):
        if verbose:
            print(f'\n\n===Test: {get_function_name()} ===')

        config = TestSearchState.get_config()
        test_board_jay = Board(config, None, Util.get_rows_from_config(config['test_board_jay']))

        gtree = GTree()
        gtree.add_word('jay')
        j = gtree.root.children['j']
        rev = j.children[GNode.CHAR_REV]
        a = rev.children['a']
        y = a.children['y']
        eow = y.children[GNode.CHAR_EOW]

        move_placed_letters = [
                PlacedLetter(Cell(0, 0), 'j')
                , PlacedLetter(Cell(1, 0), 'a')
                ]
        move_primary_word = PlacedWord(Cell(0, 0), Cell(1, 0), 'ja')
        move_secondary_words = []
        move_acc = Move(move_placed_letters, move_primary_word, move_secondary_words)

        cursor = Cell(2, 0)
        bdir = BoardDirection.RIGHT
        rack = 'abcd'
        ss = SearchState(move_acc, y, cursor, bdir, rack)
        ss.update_char_on_board(test_board_jay)

        other = SearchState(
                    Move(move_placed_letters
                        , PlacedWord(Cell(0, 0), Cell(2, 0), 'jay')
                        , []
                        )
                    , y
                    , None
                    , BoardDirection.RIGHT
                    , 'abcd'
                    )

        if verbose and ss != other:
            print(f'test_update_char_on_board: Unexpected inequality:\n\t==>{ss}\n\t   !=\n\t==>{other}')
        assert(ss == other)


def get_function_name():
    return sys._getframe(1).f_code.co_name


if __name__ == '__main__':
    # TestSearchState('test_is_next_cursor_letter').test_is_next_cursor_letter()
    # TestSearchState('test_next_cursor').test_next_cursor()
    # TestSearchState('test_reverse').test_reverse()
    # TestSearchState('test_update_blank_in_rack').test_update_blank_in_rack()
    # TestSearchState('test_update_char_in_rack').test_update_char_in_rack()
    # TestSearchState('test_update_char_on_board').test_update_char_on_board()

    runner = unittest.main()

