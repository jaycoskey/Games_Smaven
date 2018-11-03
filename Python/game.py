#!/usr/bin/env python

from enum import Enum, auto


class Bag:
    # TODO: self.letters: str
    pass


class GameState(Enum):
    IN_PLAY = auto()
    SUSPENDED = auto()
    DONE = auto()


class Game:
    def __init__(self, board, players, char2points, log_filename):
        self.board = board
        self.player_map = {p.id: p for p in players}

        ordered_ids = [p.id for p in players]
        num_players = len(ordered_ids)
        self.player_order = ordered_ids
        self.pid2next = { ordered_ids[k]: ordered_ids[k+1] for k in range(0, num_players - 1) }
        self.pid2next[ordered_ids[num_players - 1]] = ordered_ids[0]

        self.bag = bag
        self.char2points = char2points
        self.cur_turn_id = 1
        self.cur_player_id = player_order[0]
        self.game_state = GameState.NOT_STARTED
        self.history:List[Turn] = []
        self.log_file = None  # TODO
        self.log_filename = log_filename
        self.winner = None  # Remove? 

    def exit(self):
        """Clean up any resources"""
        pass

    def game_play(self):
        while self.game_state == GameState.IN_PLAY:
            turn = self.turn_get(self.cur_player_id)
            self.turn_execute(turn)
            self.cur_player_id = self.pid2next[self.cur_player_id]

    def turn_execute(self, turn):
        pass

    def turn_get(self, player_id):
        pass


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

