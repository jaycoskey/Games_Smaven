#!/usr/bin/env python

import unittest


from board_direction import BoardDirection
from util import Square, Util


class TestUtil(unittest.TestCase):
    def test_add_sq_bdir(self):
        before_sq = Square(2, 2)
        bdir = BoardDirection.RIGHT
        after_sq = Util.add_sq_bdir(before_sq, bdir)
        expected_sq = Square(3, 2)
        assert(after_sq == expected_sq)

    def test_do_rows_form_square(self):
        rows_square = ['1234', '1234', '1234', '1234']
        rows_non_square1 = ['1234', '1234']
        rows_non_square2 = ['1234', '123', '12', '1']
        assert(Util.do_rows_form_square(rows_square))
        assert(not Util.do_rows_form_square(rows_non_square1))
        assert(not Util.do_rows_form_square(rows_non_square2))

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

    # TODO: def test_sq2str(self):  # square

    def test_updated_str_with_char(self):  # s, bdir, c
        assert(Util.updated_str_with_char('use', BoardDirection.LEFT, 'f') == 'fuse')
        assert(Util.updated_str_with_char('use', BoardDirection.UP, 'f') == 'fuse')
        assert(Util.updated_str_with_char('use', BoardDirection.RIGHT, 'd') == 'used')
        assert(Util.updated_str_with_char('use', BoardDirection.DOWN, 'd') == 'used')


if __name__ == '__main__':
    runner = unittest.main()
