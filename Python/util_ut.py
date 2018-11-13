#!/usr/bin/env python

import unittest


from board_direction import BoardDirection
from util import Cell, Util


class TestUtil(unittest.TestCase):
    def test_add_cell_bdir(self):
        before_cell = Cell(2, 2)
        bdir = BoardDirection.RIGHT
        after_cell = Util.add_cell_bdir(before_cell, bdir)
        expected_cell = Cell(3, 2)
        assert(after_cell == expected_cell)

    def test_do_rows_form_cell(self):
        rows_cell = ['1234', '1234', '1234', '1234']
        rows_non_cell1 = ['1234', '1234']
        rows_non_cell2 = ['1234', '123', '12', '1']
        assert(Util.do_rows_form_cell(rows_cell))
        assert(not Util.do_rows_form_cell(rows_non_cell1))
        assert(not Util.do_rows_form_cell(rows_non_cell2))

    # TODO: def test_get_rows_from_config(self):  # cfg

    # TODO: def test_get_rows_from_filename(self):  # filename

    def test_is_subset(self):
        # No repetitions
        assert(Util.is_subset('b', 'abc'))
        assert(not Util.is_subset('abc', 'b'))

        # Tests involving multiplicity
        assert(Util.is_subset('abc', 'abbc'))
        assert(not Util.is_subset('abbc', 'abc'))

    def test_remove_char(self):
        assert(Util.remove_char('abc', 'a') == 'bc')
        assert(Util.remove_char('abc', 'b') == 'ac')
        assert(Util.remove_char('abc', 'c') == 'ab')

    def test_remove_chars(self):
        new_str = Util.remove_chars('TheQuickBrownFox', 'eFnoQruw')
        expected_str = 'ThickBox'
        if new_str != expected_str: print(f'{new_str} != {expected_str}')
        assert(new_str == expected_str)

    def test_reversed_dict(self):
        assert(Util.reversed_dict({'a':1, 'b':2, 'c':3}) == {1:'a', 2:'b', 3:'c'})

    # TODO: def test_cell2str(self):  # cell

    def test_updated_str_with_char(self):  # s, bdir, c
        assert(Util.updated_str_with_char('use', BoardDirection.LEFT, 'f') == 'fuse')
        assert(Util.updated_str_with_char('use', BoardDirection.UP, 'f') == 'fuse')
        assert(Util.updated_str_with_char('use', BoardDirection.RIGHT, 'd') == 'used')
        assert(Util.updated_str_with_char('use', BoardDirection.DOWN, 'd') == 'used')


if __name__ == '__main__':
    runner = unittest.main()
