#!/usr/bin/env python

from enum import Enum


# We store the board as a list of rows [i.e., (y, x)]. Should these directions be stored as (y, x)?
class BoardDirection(Enum):
    NO_DIR = (0, 0)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

    @staticmethod
    def is_forward(bdir):
        return bdir in [BoardDirection.RIGHT, BoardDirection.DOWN]

    @staticmethod
    def reversed(bdir):
        if bdir == BoardDirection.LEFT: return BoardDirection.RIGHT
        elif bdir == BoardDirection.UP: return BoardDirection.DOWN

        # The following aren't needed unless words can be played right->left or down->up.
        elif bdir == BoardDirection.RIGHT: return BoardDirection.LEFT
        elif bdir == BoardDirection.DOWN: return BoardDirection.UP
