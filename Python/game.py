#!/usr/bin/env python

from enum import Enum


class Bag:
    # TODO: self.letters: str
    pass


class GameState(Enum):
    NOT_STARTED = 0
    IN_PLAY = 1
    SUSPENDED = 2
    DONE = 3


class Game:
    # TODO: self.board : Board
    # TODO: self.players: List[Player]  # In order
    #
    # TODO: self.config: Dict
    # TODO: self.cur_move_id: int
    # TODO: self.cur_player_id: int
    # TODO: self.game_state: GameState
    # TODO: self.history: List[Move]
    # TODO: self.history: List[Move]
    # TODO: self.log_file: _io.TextIOWrapper
    # TODO: self.log_filename: str
    # TODO: self.winner: Player

    # TODO: def self.exit():      # Clean up resources (needed?)
    # TODO: def self.get_move():  # Get valid move from player
    # TODO: def self.make_move(): # Execute move
    # TODO: def self.play_game():
    pass
