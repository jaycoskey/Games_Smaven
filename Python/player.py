#!/usr/bin/env python

from enum import auto, Enum


from bag import Bag
from board_direction import BoardDirection
from move import Move, PlacedLetter, PlacedWord
from search import Search
from turn import Turn, TurnType
from util import Cell, Util


class Command:
    ACROSS = 'across'
    DOWN = 'down'
    PASS = 'pass'
    RESIGN = 'resign'
    SHOW = 'show'
    SWAP = 'swap'


# TODO: Replace both turn_get() and turn_report() with reference to GameCommunication static methods
#       (I.e., add a layer of indirection to support both Human and Computer play)
class Player:
    def __init__(self, game, player_id, name=None):
        self.game = game
        self.player_id = player_id
        self.name = self.get_name_from_user() if name is None else name
        self.rack = ''
        self.player_type = PlayerType.HUMAN

        # self.connection  # IP addr & port, etc. 
        self.color = None  # Set by game in GUI mode
        self.score = 0

    def get_name_from_user(self):
        return input(f'Player #{self.player_id} name: ')

    def show_game_state(self):
        print(f'  Board:\n{self.game.board}')
        if type(self.rack).__name__ == 'str':
            print('  ' + f"{self.name}'s letters: {self.rack}")
        else:
            print('  ' + f"{self.name}'s letters: {''.join(self.rack)}")
        print('  ' + f"Tiles left in bag: {len(self.game.bag)}")
        pid2score = {pid: self.game.pid2player[pid].score for pid in self.game.pid2player}
        pid2name = {pid: self.game.pid2player[pid].name for pid in self.game.pid2player}
        scores_str = ', '.join([f'{pid2name[pid]} (#{pid}): {pid2score[pid]}' for pid in self.game.pid2player])
        print('  ' + f'Scores: {scores_str}')

    # TODO: In a distributed system with a central server, the Turn object should be created at the server, not here.
    # TODO: Use argparse
    def turn_get(self):
        is_cmd_valid = False
        while not is_cmd_valid:
            entry = input(f'Enter command for player #{self.player_id}: ')
            args = entry.strip().lower().split(' ')
            cmd = args[0]
            if cmd == Command.SHOW:
                self.show_game_state()
                continue
            elif cmd in [Command.ACROSS, Command.DOWN]:
                if len(args) != 4:
                    print(f'Invalid move syntax: The place command should be followed by x & y coordinates.')
                    continue
                # Check validity of the move. (For now, all players are human.)
                w = args[1]
                try:
                    beg_x, beg_y = int(args[2]), int(args[3])
                except Exception as ex:
                    print(f'Invalid move syntax: Could not parse x & y values for the place command')
                    break

                forward = BoardDirection.RIGHT if cmd == 'across' else BoardDirection.DOWN
                back = BoardDirection.reversed(forward)

                cell_begin = Cell(beg_x, beg_y)
                cell_end = Cell(beg_x, beg_y)

                placed_chars = ''
                placed_letters = []

                if self.game.board.is_cell_empty(cell_end):
                    placed_chars += w[0]
                    placed_letters.append(PlacedLetter(cell_end, w[0]))

                for k in range(1, len(w)):
                    cell_end = Util.add_cell_bdir(cell_end, forward)
                    if self.game.board.is_cell_empty(cell_end):
                        placed_chars += w[k]
                        placed_letters.append(PlacedLetter(cell_end, w[k]))

                do_reject_move = False

                hooks_played = set(self.game.board.hooks()).intersection([pl.cell for pl in placed_letters])
                if len(hooks_played) == 0:
                    print(f'Invalid move: Word must cross a starting cell or be adjacent to a previously played tile')
                    do_reject_move = True

                normalized_placed_chars = ''.join(map(lambda c: '_' if c.isupper() else c, placed_chars))
                if not Util.is_subset(normalized_placed_chars, self.rack):
                    print(f'Invalid move: Letters placed ({placed_chars}) are not present in the rack')
                    do_reject_move = True

                cell_pre_begin = Util.add_cell_bdir(cell_begin, back)
                if (self.game.board.is_cell_on_board(cell_pre_begin)
                        and not self.game.board.is_cell_empty(cell_pre_begin)
                        ):
                    print(f'Invalid move: Cell before first character is not empty')
                    do_reject_move = True

                cell_post_end = Util.add_cell_bdir(cell_end, forward)
                if (self.game.board.is_cell_on_board(cell_post_end)
                        and not self.game.board.is_cell_empty(cell_post_end)
                        ):
                    print(f'Invalid move: Cell after last character is not empty')
                    do_reject_move = True

                search = Search(self.game.gtree, self.game.board)
                placed_word = PlacedWord(cell_begin, cell_end, w)
                secondary_words = search.get_secondary_words(placed_letters , placed_word, self.rack, False)
                for sw in secondary_words:
                    if not self.game.gtree.has_word(sw):
                        print(f'Invalid move: Secondary word found ({sw} is not in the game dictionary')
                        do_reject_move = True
                if do_reject_move:
                    continue

                cell_begin = Cell(beg_x, beg_y)
                if cmd == 'across':
                    cell_end = Cell(beg_x + len(w) - 1, beg_y)
                else:  # cmd == 'down'
                    cell_end = Cell(beg_x, beg_y + len(w) - 1)
                primary_word = PlacedWord(cell_begin, cell_end, w)
                move = Move(placed_letters, primary_word, secondary_words)
                return Turn(self.player_id
                            , TurnType.PLACE
                            , self.game.board.move2points(move)
                            , move
                            , Bag.DRAWN_UNKNOWN
                            , Bag.DISCARDED_NONE
                            )

            elif cmd == Command.SWAP:
                if len(args) < 2:
                    print(f'Invalid swap syntax: The swap command needs to be followed by letters to be swapped')
                discarded_letters = ''.join(args[1:])
                if not Util.is_subset(discarded_letters, self.rack):
                    print(f'Invalid move: You can only discard letters that are in your rack')
                    continue
                elif len(self.game.bag) < len(discarded_letters):
                    print(f'Invalid move description: Cannot exchange {len(times_dumped)} tiles when only {len(bag)} remain in the bag')
                    continue
                return Turn(self.player_id, TurnType.SWAP, 0, None, Bag.DRAWN_UNKNOWN, discarded_letters)

            elif cmd == Command.PASS:
                if len(args) > 1:
                    print(f'Invalid move syntax: The swap command does not take any additional information')
                # Note: Player can always pass
                return Turn(self.player_id, TurnType.PASS, 0, None, Bag.DRAWN_NONE, Bag.DISCARDED_NONE)

            elif cmd == Command.RESIGN:
                if len(args) > 1:
                    print(f'Invalid move syntax: The resign command does not take any additional information')
                # Note: Player can always resign
                return Turn(self.player_id, TurnType.RESIGN, 0, None, Bag.DRAWN_NONE, Bag.DISCARDED_NONE)

            else:
                print(f'Unrecognized command: {cmd}')

            print(Util.tabify(self.game.config['help_command_syntax']))

    # TODO: GUI version
    def turn_report(player_id, turn):
        if turn.turn_type == TurnType.PLACE:
            pass  # TODO
        elif turn.turn_type == TurnType.SWAP:
            pass  # TODO
        elif turn.turn_type == TurnType.PASS:
            pass  # TODO
        elif turn.turn_type == TurnType.RESIGN:
            pass  # TODO
        else:
            raise ValueError('Unrecognized turn type')


class PlayerType(Enum):
    COMPUTER = auto()
    HUMAN = auto()
