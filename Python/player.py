#!/usr/bin/env python


# TODO: Replace both turn_get() and turn_report() with reference to GameCommunication static methods
#       (I.e., add a layer of indirection to support both Human and Computer play)
class Player:
    def __init__(self, game, player_id, name):
        self.game = game
        self.id = player_id
        self.name = name

        # self.connection  # IP addr & port, etc. 
        self.color = None  # Set by game in GUI mode
        self.score = 0

    # TODO: In a distributed system with a central server, the Turn object should be created at the server, not here.
    def turn_get():
        is_cmd_valid = False
        while not is_cmd_valid:
            entry = input('Enter command (? for help): ')
            args = entry.split()
            cmd = args[0]
            if cmd == '?' or cmd == 'help':
                # TODO: Move syntax help message to config file?
                print('Enter one of the following:')
                print('    move <primary_word> <square_begin> <square_end>')
                print('        primary_word: The word formed that contains all the letters placed')
                print('        square_begin: Coordinates of the first letter of the word. Coordinate description TBD')  
                print('        square_end:   Final letter of the word entered, using the system described above')
                print('    swap <letters>')
                print("        letters:      All the letters to be swapped, with '_' representing a blank tile")
                print('    pass')
                print('        (Appropriate when no move appears possible)')
                print('    resign')
                print('    exit              # End game, without passing turn to opponent')
            elif cmd == 'move':
                move = None  # TODO
                points = 0  # TODO
                drawn = ''  # TODO
                return Turn(self.id, TurnType.MOVE, points=0, move=None, drawn=drawn, discarded=None)
            elif cmd == 'swap':
                discarded = ''  # TODO
                drawn = ''  # TODO
                return Turn(self.id, TurnType.SWAP, points=0, move=None, drawn=drawn, discarded=discarded)
            elif cmd == 'pass':
                return Turn(self.id, TurnType.PASS, points=0, move=None, drawn=None, discarded='')
            elif cmd == 'resign':
                return Turn(self.id, TurnType.RESIGN, points=0, move=None, drawn=None, discarded='')
            elif cmd == 'exit':
                self.game.exit()
            else:
                print(f'Unrecognized command: {entry}')

    # TODO: GUI version
    def turn_report(player_id, turn):
        if turn.turn_type == TurnType.MOVE:
            pass  # TODO
        elif turn.turn_type == TurnType.SWAP:
            pass  # TODO
        elif turn.turn_type == TurnType.PASS:
            pass  # TODO
        elif turn.turn_type == TurnType.RESIGN:
            pass  # TODO
        else:
            raise ValueError('Unrecognized turn type')
