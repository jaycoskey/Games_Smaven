#!/usr/bin/env python

import unittest
import yaml


from board import Board
from gtree import GTree
from search import Search


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


if __name__ == '__main__':
    # TestSearch.show_test_search_config()

    # TestSearch('test_board_edge').test_board_edge()
    # TestSearch('test_empty_board').test_empty_board()
    # TestSearch('test_fill_gap').test_fill_gap()
    # TestSearch('test_fill_gap_with_blank').test_fill_gap_with_blank()
    # TestSearch('test_fill_noncontiguous_gaps').test_fill_noncontiguous_gaps()
    # TestSearch('test_parallel_word').test_parallel_word()
    # TestSearch('test_secondary_words').test_secondary_words()

    runner = unittest.main()

