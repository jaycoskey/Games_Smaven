#!//usr/bin/env python

import argparse
import string
import sys
import yaml

from board import Board, BoardLayout
from game import Game
from gtree import GTree
from move import Move, PlacedLetter, PlacedWord
from player import Player
from util import Util


def main():
    for line in layout_rows:
        print(line)


if __name__ == '__main__':
    prog_description = 'Toolbox for word square games. Details TBD'
    parser = argparse.ArgumentParser(prog_description)
    args = parser.parse_args()

    with open('config.yml', 'r') as config_stream:
        try:
            config = yaml.load(config_stream)
        except yaml.YAMLError as ex:
            print(ex, file=sys.stderr)

    layout = config[config['board_layout']]
    layout_rows = layout.splitlines(False)
    assert(Util.do_rows_form_square(layout_rows))

    main()
