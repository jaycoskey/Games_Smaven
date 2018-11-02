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


def main(config, args):
    if args.command == 'search':
        # TODO: search ==> Initialize Board (BoardLayout, Board) ==> Enter rack & find words
        if args.layoutfile is None or len(args.layoutfile) == 0:
            raise ValueError('search feature requires layoutfile to be set')
        if args.boardfile is None or len(args.boardfile) == 0:
            raise ValueError('search feature requires boardfile to be set')
        if args.rack is None or len(args.rack) == 0:
            raise ValueError('search feature requires rack to be set')

        do_use_layout_config = args.layoutfile[0] == '@'
        layout_rows = ( Util.get_rows_from_config(config[args.layoutfile[1:]])
                        if do_use_layout_config
                        else Util.get_rows_from_filename(args.layoutfile))
        layout = BoardLayout(layout_rows)

        do_use_board_config = args.boardfile[0] == '@'
        board_rows = ( Util.get_rows_from_config(config[args.boardfile[1:]])
                       if do_use_board_config
                       else Util.get_rows_from_filename(args.boardfile))
        board = Board(layout=layout, rows=board_rows)

        rack = args.rack

        if args.verbose:
            print('INFO: Layout:')
            layout.print()
            print('INFO: Board:')
            board.print()
            print(f'INFO: Rack: {rack}')

        print('Search feature not yet implemented')

    elif args.experiment:
        # TODO: experiment ==> Init Board (BoardLayout, Board, Bag); start interactive shell (search/load/replay/etc.)
        raise NotImplementedError('Lab feature not yet implemented')
    elif args.players:
        # TODO: players ==> Init Game (Players, BoardLayout, Board, Bag); play_game(...)
        raise NotImplementedError('Specification of players not yet implemented')
    elif args.zen:  # Train computer strategy using reinforcement learning
        # TODO: zen ==> Init Game (Players w/ strategy, BoardLayout, Board, Bag); play_game(...)
        raise NotImplementedError('Evolve feature not yet implemented')
    else:
        raise ValueError(f'Feature not specified')


if __name__ == '__main__':
    CMD_SEARCH = 'search'
    CMD_EXPERIMENT = 'experiment'
    CMD_PLAYERS = 'players'
    CMD_ZEN = 'zen'

    # Argument summary:
    # a:           b:board   c:config  d:dictionary e:experiment
    # f:           g:gui     h:        i:           j:
    # k:           l:layout  m:        n:           o:output?
    # p:players    q:        r:rack    s:           t:text
    # u:           v:verbose w:        x:           y:
    # z:zen
    #
    prog_description = 'Toolbox for word square games, such as Scrabble and Words With Friends'
    parser = argparse.ArgumentParser(prog=sys.argv[0], description=prog_description)

    parser.add_argument('-c', '--configfile', help='File that contains game configuration', default='config.yml')
    parser.add_argument('-l', '--layoutfile', help='File that contains the layout of the board', default='@layout_scrabble')
    parser.add_argument('-v', '--verbose', action='store_true')

    display_mode_group = parser.add_mutually_exclusive_group(required=False)
    display_mode_group.add_argument('-t', '--text', dest='display_mode', const='text')
    display_mode_group.add_argument('-g', '--gui', dest='display_mode', const='gui')
    parser.set_defaults(display_mode='text')

    subparsers = parser.add_subparsers(title='commands', dest='command')

    # Commands
    parser_search = subparsers.add_parser(CMD_SEARCH, help='Find valid moves for a given board, rack, and dictionary')
    parser_experiment = subparsers.add_parser(CMD_EXPERIMENT, help='Use a shell to experiment')
    parser_players = subparsers.add_parser(CMD_PLAYERS, help='Play a game: Human vs Human, or Computer vs Human')
    parser_zen = subparsers.add_parser(CMD_ZEN, help='Develop a strategy by playing Computer vs Computer')

    # Search args
    parser_search.add_argument('-b', '--boardfile', help='File that contains letters present on board', default='@board_scrabble_test1')
    parser_search.add_argument('-r', '--rack', help='Rack that contains letters to be used in search', default='etaoins')

    # Player args
    players_group = parser_players.add_mutually_exclusive_group(required=False)
    parser_players.add_argument('--hh', dest='players_mode', const='hh', help='Human vs Human')
    parser_players.add_argument('--hc', dest='players_mode', const='hc', help='Human vs Computer')
    parser_players.add_argument('--cc', dest='players_mode', const='cc', help='Computer vs Computer')
    parser_players.set_default(players_mode = 'hh')

    # TODO: Specify how players join and how their identity & connection info is obtained
    # TODO: Specify how input is obtained: keyboard/server:port/etc.

    # Zen args (feature selection not modifiable from command line)
    # TODO: Input file containing weights
    # TODO: Output files containing game stats, and modified weights

    args = parser.parse_args()

    with open('config.yml', 'r') as config_stream:
        try:
            config = yaml.load(config_stream)
        except yaml.YAMLError as ex:
            print(ex, file=sys.stderr)

    main(config, args)
