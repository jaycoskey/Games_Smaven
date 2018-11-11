#!/usr/bin/env python

from collections import Counter, namedtuple


from board_direction import BoardDirection


Square = namedtuple('Square', ['x', 'y'])


class Util:
    @staticmethod
    def add_sq_bdir(sq, bdir):
        return Square(sq.x + bdir.value[0], sq.y + bdir.value[1])

    @staticmethod
    def do_rows_form_square(rows):
        row_count = len(rows)
        are_rows_same_length = all(map(lambda row: len(row) == row_count, rows))
        if not are_rows_same_length:
            return False
        is_board_square = row_count == len(rows[0])
        return is_board_square

    @staticmethod
    def get_rows_from_config(cfg):
        return [line for line in cfg.split('\n') if len(line) > 0]

    @staticmethod
    def get_rows_from_filename(filename):
        with open(filename, 'r') as f:
            result = [line.strip() for line in f.readlines()]
            print(f'# of rows in result={len(result)}')
            return [line.strip() for line in f.readlines()]

    @staticmethod
    def is_subset(s1, s2):
        cntr1 = Counter(s1)
        cntr2 = Counter(s2)
        for k in cntr1.keys():
            if k not in cntr2 or cntr2[k] < cntr1[k]:
                return False
        return True

    @staticmethod
    def removed_char(rack, c):
        index = rack.find(c)
        return rack[0: index] + rack[index: len(rack)]

    @staticmethod
    def removed_chars(rack, s):
        for c in s:
            rack = removed_char(rack, c)
        return rack

    @staticmethod
    def reversed_dict(d):
        return { d[k]: k for k in d }

    @staticmethod
    def sq2str(square):
        return f'({square[0]},{square[1]})' if square else 'None'

    @staticmethod
    def updated_str_with_char(s, bdir, c):
        return (s + c) if BoardDirection.is_forward(bdir) else (c + s)
