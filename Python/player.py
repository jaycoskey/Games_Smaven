#!/usr/bin/env python

from enum import auto, Enum


from bag import Bag
from board_direction import BoardDirection
import game
from move import Move, PlacedWord
from search import Search
from turn import Turn, TurnType
from util import Square, Util


# TODO: Replace both turn_get() and turn_report() with reference to GameCommunication static methods
#       (I.e., add a layer of indirection to support both Human and Computer play)
class Player:
    def __init__(self, game, player_id):
        self.game = game
        self.player_id = player_id
        self.name = self.get_name_from_user()
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

    # TODO: In a distributed system with a central server, the Turn object should be created at the server, not here.
    def turn_get(self):
        is_cmd_valid = False
        ###
        ###
        ### DEBUG HACK
        self.rack = 'swatxyz'
        ###
        ###
        ###
        while not is_cmd_valid:
            entry = input(f'Enter command for player #{self.player_id}: ')
            args = entry.strip().lower().split(' ')
            cmd = args[0]
            if cmd == 'show':
                self.show_game_state()
                continue
            elif cmd in ['across', 'down']:
                if len(args) != 4:
                    print(f'Invalid move syntax: The place command should be followed by x & y coordinates.')
                    break
                # Check validity of the move. (For now, all players are human.)
                w = args[1]
                try:
                    beg_x, beg_y = int(args[2]), int(args[3])
                except ex as Exception:
                    print(f'Invalid move syntax: Could not parse x & y values for the place command')
                    break

                bdir =  BoardDirection.RIGHT if cmd == 'across' else BoardDirection.DOWN
                square_begin = Square(beg_x, beg_y)
                square_end = Square(beg_x, beg_y)

                placed_chars = ''
                placed_letters = []

                if self.game.board.is_square_empty(square_end):
                    placed_letters.append(PlacedLetter(square_end, w[0]))

                for k in range(1, len(w)):
                    square_end = Util.add_sq_bdir(square_end, bdir)
                    if self.game.board.is_square_empty(square_end):
                        placed_chars += w[k]
                        placed_letters.append(PlacedLetter(square_end, w[k]))

                do_reject_move = False
                if not Util.is_subset(placed_chars, self.rack):
                    print(f'Invalid move: Letters placed are not present in the rack')
                    do_reject_move = True
                if not self.game.gtree.has_word(w):
                    s = self.game.gtree.root.children['s']
                    plus = s.children['+']
                    w = plus.children['w']
                    print(f"Children of sw: {''.join(w.children)}")
                    a = w.children['a']
                    t = a.children['t']
                    char_end = t.children['$']
                    print(f'Invalid move: Word entered is not in the game dictionary')
                    do_reject_move = True
                search = Search(self.game.gtree, self.game.board)
                placed_word = PlacedWord(square_begin, square_end, w)
                secondary_words = search.get_secondary_words( placed_letters , placed_word, self.rack, False)
                for sw in secondary_words:
                    if not self.game.gtree.has_word(sw):
                        print(f'Invalid move: Secondary word found ({sw} is not in the game dictionary')
                        do_reject_move = True
                if do_reject_move:
                    raise ValueError('Internal error: Did not exit turn input loop on input error')

                square_begin = Square(beg_x, beg_y)
                if cmd == 'across':
                    square_end = Square(beg_x + len(w) - 1, beg_y)
                else:  # cmd == 'down'
                    square_end = Square(beg_x, beg_y + len(w) - 1)
                primary_word = PlacedWord(square_begin, square_end, w)
                move = Move(placed_letters, primary_word, secondary_words)
                return Turn(self.player_id
                            , TurnType.PLACE
                            , self.game.board.move2points(move)
                            , move
                            , Bag.DRAWN_UNKNOWN
                            , Bag.DISCARDED_NONE
                            )
            elif cmd == 'swap':
                discarded_letters = ''.join(args[1:])
                if not Util.is_subset(discarded_letters, rack):
                    print(f'Invalid move: You can only discard letters that are in your rack')
                    continue
                elif len(bag) < len(discarded_letters):
                    print(f'Invalid move description: Cannot exchange {len(times_dumped)} tiles when only {len(bag)} remain in the bag')
                    continue
                return Turn(player_id, TurnType.SWAP, 0, move, Bag.DRAWN_UNKNOWN,  discarded_letters)
            elif cmd == 'pass':
                if len(args) > 1:
                    print(f'Invalid move syntax: The swap command does not take any additional information')
                # Note: Player can always pass
                return Turn(TurnType.PASS, None, Bag.DRAWN_NONE, game.Game.DISCARDED_NONE)
            elif cmd == 'resign':
                if len(args) > 1:
                    print(f'Invalid move syntax: The resign command does not take any additional information')
                # Note: Player can always resign
                return Turn(TurnType.RESIGN, None, Bag.DRAWN_NONE, game.Game.DISCARDED_NONE)

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
