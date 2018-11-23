#!/usr/bin/env python

from collections import Counter, namedtuple


from board_direction import BoardDirection


Cell = namedtuple('Cell', ['x', 'y'])


class Util:
    TEST_FEATURES = True

    @staticmethod
    def add_cell_bdir(cell, bdir):
        return Cell(cell.x + bdir.value[0], cell.y + bdir.value[1])

    @staticmethod
    def cell_copy(cell):
        return Cell(cell.x, cell.y)

    @staticmethod
    def do_rows_form_cell(rows):
        row_count = len(rows)
        are_rows_same_length = all(map(lambda row: len(row) == row_count, rows))
        if not are_rows_same_length:
            return False
        is_board_cell = row_count == len(rows[0])
        return is_board_cell

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
    def remove_char(rack, c):
        assert(c in rack)
        indx = rack.index(c)
        end = len(rack)
        return rack[0: indx] + rack[indx + 1: end]

    @staticmethod
    def remove_chars(rack, s):
        for c in s:
            rack = Util.remove_char(rack, c)
        return rack

    @staticmethod
    def reversed_dict(d):
        return { d[k]: k for k in d }

    @staticmethod
    def cell2str(cell):
        return f'({cell[0]},{cell[1]})' if cell else 'None'

    @staticmethod
    def tabify(s):
        return '\n'.join(['\t{}'.format(row) for row in s.splitlines()])

    @staticmethod
    def updated_str_with_char(s, bdir, c):
        if s is None:
            return c
        else:
            return (s + c) if BoardDirection.is_forward(bdir) else (c + s)
