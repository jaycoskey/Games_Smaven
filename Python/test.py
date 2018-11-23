#!/usr/bin/env python

import unittest
import yaml


from gtree_ut import TestGTree
from search_ut import TestSearch
from search_state_ut import TestSearchState
from util_ut import TestUtil


def show_config(filename):
    with open(filename, 'r') as stream:
        config = yaml.load(stream)

    for k in config:
        print(f'Config key: {k}')
        if k == 'letter_counts_scrabble_en':
            print(f'key={k}: val={config[k]}')


def show_test_search_config(filename):
    with open(filename, 'r') as stream:
        config = yaml.load(stream)

    for k in config:
        print(f'Test name: {k}')
        for test_prop in config[k]:
            if test_prop == 'board':
                print(f'\t{test_prop}: ...')
            else:
                print(f'\t{test_prop}: {config[k][test_prop]}')


if __name__ == '__main__':
    # show_config('config.yml')
    # show_test_search_config('test_search.yml')
    runner = unittest.main()

