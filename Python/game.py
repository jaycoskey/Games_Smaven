#!/usr/bin/env python

from enum import Enum, auto
import logging
from random import randint


class Bag:
    CHAR_BLANK = ' '
    DRAWN_NONE = ''
    DRAWN_UNKNOWN = '?'
    DISCARDED_NONE = ''

    def __init__(self, count2chars):
        char2count = {}
        for count in count2chars:
            for char in count2chars[count]:
                char2count[char] = count
        self.letters = ''.join([c * char2count[c] for c in char2count])

    def __len__(self):
        return len(self.letters)

    def add(self, chars):
        self.letters += chars

    def draw(self, count):
        def draw_single():
            pos = randint(0, len(self.letters) - 1)
            return self.letters.pop(pos)

        if count > len(self.letters):
            raise ValueError(f'Not enough letters: {len(self.letters)} available, but {count} requested')

        return [draw_single for _ in range(count)]


class GameState(Enum):
    IN_PLAY = auto()
    SUSPENDED = auto()
    DONE = auto()


class Game:
    def __init__(self, config, board, num_players, points2chars, log_filename):
        self.bag = bag
        self.board = board
        self.cur_turn_id = 1
        self.game_state = GameState.NOT_STARTED
        self.history:List[Turn] = []
        self.num_players = num_players
        self.winner = None  # Remove? 

        self.char2points = {c:points2chars[p] for c in points2chars[p] for p in points2chars}


        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_filename)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:' + logging.BASIC_FORMAT)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def __enter__(self):
        self.get_players()

    def __exit__(self):
        # Clean up resources, notify players, etc.
        pass

    def _init_players(self):
        players = self.get_players()
        self.player_map = {p.id: p for p in players}
        ordered_ids = [p.id for p in players]
        self.player_order = ordered_ids
        self.pid2next = { ordered_ids[k]: ordered_ids[k+1] for k in range(0, num_players - 1) }
        self.pid2next[ordered_ids[num_players - 1]] = ordered_ids[0]
        self.cur_player_id = player_order[0]

    def get_players(self, num_players):
        result = []
        for player_id in range(1, num_players + 1):
            p = Player(self, player_id)
            p.get_name()
            results.append(p)
        return result

    def play(self):
        while True:
            self.game_play_one_game()
            response = input('Play again (y/n)? ').strip()
            if not response[0].lower() == 'y':
                break
        print('Bye!')

    def play_one_game(self):
        self.game_state = GameState.IN_PLAY
        while self.game_state == GameState.IN_PLAY:
            turn = self.turn_get(self.cur_player_id)
            if turn.turn_type == TurnType.RESIGN:
                self.game_state == GameState.DONE
            self.turn_execute(turn)
            self.cur_player_id = self.pid2next[self.cur_player_id]

    def turn_execute(self, turn):
        player = self.get_player(turn.player_id)
        if turn.turn_type == TurnType.PLACE:
            placed_chars = ''.join([pl.char for pl in turn.move.placed_letters])
            TODO: remove letters from rack
            TODO: place letters on board
            TODO: increment player score
            drawn_letters = bag.draw(len(placed_letters))

            placed_letter_count = len(turn.move.placed_letters)
            drawn_letters_count = min(placed_letter_count, len(bag))
            drawn_letters = bag_draw

        elif turn.turn_type == TurnType.SWAP:
            TODO: remove letters from rack
            TODO: draw from bag

        elif turn.turn_type == TurnType.PASS:
            TODO: if previous player passed, game is a tie

        elif turn.turn_type == TurnType.RESIGN:
        else:
            raise ValueError(f'Unknown turn type: {turn.turn_type}')


class GameCommunication:
    @staticmethod
    def get_turn_from_computer():
        pass  # TODO

    @staticmethod
    def get_turn_from_human():
        pass  # TODO

    @staticmethod
    def report_turn_from_computer():
        pass  # TODO: Callback

    @staticmethod
    def report_turn_from_human():
        pass  # TODO 
