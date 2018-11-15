#!/usr/bin/env python

from enum import Enum, auto
import logging
from random import randint
import os


from bag import Bag
from player import Player
from turn import TurnType
from util import Util


class GameEndType(Enum):
    PLAYERS_PASSED = auto()
    PLAYER_PLAYED_LAST_TILE = auto()
    PLAYER_RESIGNED = auto()


class GameState(Enum):
    NOT_STARTED = auto()
    IN_PLAY = auto()
    SUSPENDED = auto()
    DONE = auto()


class Game:
    def __init__(self, config, gtree, board):
        self.bag = Bag(config[config['counts2chars']])
        self.board = board
        self.config = config
        self.cur_turn_id = 1
        self.game_end_type = None
        self.game_state = GameState.NOT_STARTED
        self.gtree = gtree
        self.history:List[Turn] = []
        self.num_players = int(config['player_count'])
        self.was_prev_turn_pass = False
        self.winner_id = None  # Remove? 

        self.board.set_game(self)

        points2chars = config[config['points2chars']]
        self.char2points = {}
        for p in points2chars:
            for c in points2chars[p]:
                self.char2points[c] = int(p)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        logfile_path = config['logfile_basename'] + '_' + str(os.getpid()) + '.log'
        handler = logging.FileHandler(logfile_path)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:' + logging.BASIC_FORMAT)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self._init_players(self.num_players)


    def _get_players(self, num_players):
        result = []
        for player_id in range(1, num_players + 1):
            p = Player(self, player_id)
            result.append(p)
        return result

    def _init_players(self, num_players):
        players = self._get_players(num_players)
        ordered_pids = [p.player_id for p in players]
        self.ordered_pids = ordered_pids
        self.pid2next = { ordered_pids[k]: ordered_pids[k+1] for k in range(0, num_players - 1) }
        self.pid2next[ordered_pids[num_players - 1]] = ordered_pids[0]
        self.pid2player = {p.player_id: p for p in players}
        self.cur_player_id = ordered_pids[0]

        for p in players:
            p.rack = self.bag.draw(7)

    def exit(self):
        # Clean up resources, notify players, etc.
        pass

    def play(self):
        while True:
            self.play_one_game()
            response = input('Play again (y/n)? ').strip()
            if not response[0].lower() == 'y':
                break
        print('Bye!')

    def play_one_game(self):
        self.game_state = GameState.IN_PLAY
        while self.game_state == GameState.IN_PLAY:
            player = self.pid2player[self.cur_player_id]
            player.show_game_state()
            turn = player.turn_get()
            self.turn_execute(turn)
            if self.game_state == GameState.DONE:
                if turn.turn_type != TurnType.RESIGN:
                    scores = {p.player_id: p.score for p in self.players}
                    self.winner_id = sorted(scores, key=lambda p: p[1])[-1]
                wid = self.winner_id
                print(f'Player #{wid} has won! Congratulations, {self.pid2player[wid].name}!')
                self.cur_player_id = self.winner_id
            else:
                self.cur_player_id = self.pid2next[self.cur_player_id]

    def turn_execute(self, turn):
        print(f'INFO: Entering turn_execute: turn={turn}')
        player = self.pid2player[turn.player_id]
        if turn.turn_type == TurnType.PLACE:
            self.was_prev_turn_pass = False
            placed_chars = ''.join([pl.char for pl in turn.move.placed_letters])
            player.rack = Util.remove_chars(player.rack, placed_chars)
            for pl in turn.move.placed_letters:
                self.board[pl.cell] = pl.char
            player.score += self.board.move2points(turn.move)

            num_letters_to_draw = min(len(placed_chars), len(self.bag))
            if num_letters_to_draw > 0:
                drawn_letters = self.bag.draw(num_letters_to_draw)
                player.rack += drawn_letters
                print(f"After {player.name}'s turn, rack={player.rack}")
            else:
                self.game_state = GameState.DONE

        elif turn.turn_type == TurnType.SWAP:
            self.was_prev_turn_pass = False
            player.rack = Util.remove_chars(player.rack, turn.discarded)
            self.bag.add(turn.discarded)
            drawn_chars = self.bag.draw(len(turn.discarded))
            player.rack += drawn_chars

        elif turn.turn_type == TurnType.PASS:
            if self.was_prev_turn_pass:
                self.game_state = GameState.DONE

        elif turn.turn_type == TurnType.RESIGN:
            self.game_state = GameState.DONE
            self.game_end_type = GameEndType.PLAYER_RESIGNED
            self.winner_id = self.pid2next[turn.player_id]
        else:
            raise ValueError(f'Unknown turn type: {turn.turn_type}')


class GameCommunication:
    @staticmethod
    def turn_get_from_computer():
        pass  # TODO

    @staticmethod
    def turn_get_from_human():
        pass  # TODO

    @staticmethod
    def turn_report_to_computer():
        pass  # TODO: Callback

    @staticmethod
    def turn_report_to_human():
        pass  # TODO 
