#!/usr/bin/env python

import unittest
import yaml
import sys


from board import Board
from board_direction import BoardDirection
from gtree import GNode, GTree
from move import Move, PlacedLetter, PlacedWord
from search import Search, SearchState
from util import Cell, Util


class TestSearch(unittest.TestCase):
    VERBOSE = True

    @staticmethod
    def run_config_test(test_name, verbose=VERBOSE):
        if verbose:
            print(f'\n\n===Test: {test_name}===')

        with open('test_search.yml', 'r') as stream:
            config = yaml.load(stream)

        config_test = config[test_name]
        if verbose:
            print(f"*** Config keys: {', '.join(config_test)}")

        config_board = config_test['board']

        # Dictionary
        config_dictionary = config_test['dictionary']
        if verbose:
            print(f'*** Dictionary words')
            for dword in config_dictionary:
                print(f'\t- {dword}')

        # Rack
        config_rack = config_test['rack']
        if verbose:
            print(f'*** Rack letters: {config_rack}')

        # Words expected to be found
        config_words_found = config_test['words_found']
        if verbose:
            print(f'*** Expected words')
            if type(config_words_found).__name__ == 'str':
                config_words_found = [config_words_found]
            if config_words_found:
                for word in config_words_found:
                    print(f'\t- {word}')
            else:
                print(f'\t<None>')

        board = Board(config_test, layout=None, rows=config_board)
        gtree = GTree()
        gtree.add_wordlist(config_dictionary)
        search = Search(gtree, board)
        moves_found = search.find_moves(config_rack)

        # Words actually found
        words_found = []
        for move in moves_found:
            words_found.append(move.primary_word)
            words_found.extend(move.secondary_words)

        if verbose:
            print(f'*** Number of moves found={len(moves_found)}')
            for move in moves_found:
                print(f'==> {move}')

        if config_words_found:
            assert(all([ word in words_found
                    for word in config_words_found
                    ]))

        # Words not expected to be found
        if 'words_not_found' in config_test:
            config_words_not_found = config_test['words_not_found']
            assert(all([word not in config_words_not_found
                        for word in words_found]))

    @staticmethod
    def show_test_search_config():
        filename = 'test_search.yml'
        with open(filename, 'r') as stream:
            config = yaml.load(stream)

        for k in config:
            print(f'Test name: {k}')
            for test_prop in config[k]:
                if test_prop == 'board':
                    print(f'\t{test_prop}: ...')
                else:
                    print(f'\t{test_prop}: {config[k][test_prop]}')

    def test_board_edge(self):
        TestSearch.run_config_test('test_board_edge')

    def test_empty_board(self):
        TestSearch.run_config_test('test_empty_board')

    def test_fill_gap(self):
        TestSearch.run_config_test('test_fill_gap')

    def test_fill_gap_with_blank(self):
        TestSearch.run_config_test('test_fill_gap_with_blank')

    def test_fill_noncontiguous_gaps(self):
        TestSearch.run_config_test('test_fill_noncontiguous_gaps')

    def test_parallel_word(self):
        TestSearch.run_config_test('test_parallel_word')

    def test_secondary_words(self):
        TestSearch.run_config_test('test_secondary_words')


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

        lhs = left, right, up, down
        rhs = [Cell(0, 0), Cell(0, 2), None, Cell(1, 1)]
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
        j = gtree.root.children['j']
        rev = j.children[GNode.CHAR_REV]
        a = rev.children['a']
        y = a.children['y']

        move_placed_letters = [PlacedLetter(Cell(0, 0), 'j')]
        move_primary_word = PlacedWord(Cell(0, 0), Cell(0, 0), 'j')
        move_secondary_words = []
        move_acc = Move(move_placed_letters, move_primary_word, move_secondary_words)

        cursor = Cell(1, 0)
        bdir = BoardDirection.RIGHT
        rack = '_'
        ss = SearchState(move_acc, a, cursor, bdir, rack)
        ss.update_blank_in_rack(gtree, test_board_jay)

        other = SearchState(
                    Move(move_placed_letters +  [PlacedLetter(Cell(1, 0), 'A')]
                        , PlacedWord(Cell(0, 0), Cell(1, 0), 'ja')
                        , []
                        )
                    , y
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
        j = gtree.root.children['j']
        rev = j.children[GNode.CHAR_REV]
        a = rev.children['a']
        y = a.children['y']

        move_placed_letters = [PlacedLetter(Cell(0, 0), 'j')]
        move_primary_word = PlacedWord(Cell(0, 0), Cell(0, 0), 'j')
        move_secondary_words = []
        move_acc = Move(move_placed_letters, move_primary_word, move_secondary_words)

        cursor = Cell(1, 0)
        bdir = BoardDirection.RIGHT
        rack = 'a'
        ss = SearchState(move_acc, a, cursor, bdir, rack)
        ss.update_blank_in_rack(gtree, test_board_jay)

        other = SearchState(
                    Move(move_placed_letters +  [PlacedLetter(Cell(1, 0), 'a')]
                        , PlacedWord(Cell(0, 0), Cell(1, 0), 'ja')
                        , []
                        )
                    , y
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
                    Move(move_placed_letters +  [PlacedLetter(Cell(2, 0), 'y')]
                        , PlacedWord(Cell(0, 0), Cell(2, 0), 'jay')
                        , []
                        )
                    , eow
                    , Cell(3, 0)
                    , BoardDirection.RIGHT
                    , 'abcd'
                    )

        if verbose and ss != other:
            print(f'test_update_char_on_board: Unexpected inequality:\n\t==>{ss}\n\t   !=\n\t==>{other}')
        assert(ss == other)


def get_function_name():
    return sys._getframe(1).f_code.co_name


if __name__ == '__main__':
    # TestSearch.show_test_search_config():
    runner = unittest.main()
