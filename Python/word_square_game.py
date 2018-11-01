#!//usr/bin/env python

import string
import sys
import yaml

from board import Board, BoardLayout
from game import Game
from gtree import GTree
from move import Move, PlayedLetter, PlayedWord
from player import Player
from util import Util


def main():
    with open('config.yml', 'r') as config_stream:
        try:
            config = yaml.load(config_stream)
        except yaml.YAMLError as ex:
            print(ex, file=sys.stderr)

    layout = config[config['board_layout']]
    layout_rows = layout.splitlines(False)
    assert(Util.do_rows_form_square(layout_rows))

    for line in layout_rows:
        print(line)


if __name__ == '__main__':
    # TODO: Parse arguments
    main()
