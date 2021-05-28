import chess
import _thread
from confic.const import *
from ai.agents.player import Player

class Environment:
    '''
        environment class that is manager
        @param
        first_player: Player
        second_player: Player
        gui: userInterface that display interface
    '''
    _instance=None
    @staticmethod
    def getInstance():
        if Environment._instance == None:
            Environment()
        return Environment._instance

    def __init__(self, first_player = Player('white'), second_player = Player('black'), gui=None):
        if Environment._instance != None:
            raise Exception("This is singleton class")
        self.board = chess.Board()
        self.first_player = first_player
        self.second_player = second_player
        self.gui = gui
        Environment._instance = self

    def setGUI(self, gui):
        self.gui = gui

    def setPlayer1(self, player):
        self.first_player = player

    def setPlayer2(self, player):
        self.second_player = player

    # return current board's state
    # [[wr, wn, wq, wb, wk...], [wp, wp, wp,...],...]
    def getState(self):
        a = self.board.__str__()
        b = a.split("\n")
        state = []
        for i in range(8):
            state.append(b[i].split(" "))
        
        # convert state format
        for i in range(8):
            for j in range(8):
                if state[i][j].isupper():
                    state[i][j] = 'w' + state[i][j].lower()
                elif state[i][j].islower():
                    state[i][j] = 'b' + state[i][j]
        
        return state

    # on and to is tuple that is pocision of moving piece
    def move(self, on, to):
        m = chess.Move.from_uci(SQUARE_NAME[on[0]][on[1]] + SQUARE_NAME[to[0]][to[1]])
        if m in self.board.legal_moves:
            self.board.push(m)
            return True
        elif to[0] == 0 or to[0] == 7:
            m = chess.Move.from_uci(SQUARE_NAME[on[0]][on[1]] + SQUARE_NAME[to[0]][to[1]] + "q")
            if m in self.board.legal_moves:
                self.board.push(m)
                return True 
        return False

    def move_uci(self, uci_str):
        m = chess.Move.from_uci(uci_str)
        if m in self.board.legal_moves:
            self.board.push(m)
            return True
        m = chess.Move.from_uci(uci_str + "q")
        if m in self.board.legal_moves:
            self.board.push(m)
            return True
        return False

    # @param {bool} true if white piece and false if black piece
    def computerMove(self, turn):
        action = None
        if turn:
            action = self.first_player.action(self.board) # first player always white
        else:
            action = self.second_player.action(self.board) # second player alway black
        self.move_uci(action.uci())
        self.gui.refresh()

    # return last move from stack
    def recentMove(self):
        last_square = None
        now_square = None
        if len(self.board.move_stack) > 0:
            m = self.board.peek() # Move class
            last_square = (7 - chess.square_rank(m.from_square), chess.square_file(m.from_square)) # rank is the island of the index
            now_square = (7 - chess.square_rank(m.to_square), chess.square_file(m.to_square))
        return last_square, now_square

    # determine turn of player and player type
    def changeTurn(self):
        if self.board.turn == chess.WHITE:
            type = self.first_player.type() # determine type of player
            if len(type) > 1: # player is ai
                _thread.start_new_thread(self.computerMove, (True,)) # True if white turn
            return type
        else:
            type = self.second_player.type()
            if len(type) > 1: # player is ai
                _thread.start_new_thread(self.computerMove, (False,)) # False if black turn
            return type

    def isPlay(self):
        return not self.board.is_game_over()

    def reset(self):
        self.board.reset()

    def undo(self):
        if len(self.board.move_stack) > 0:
            self.board.pop()
            if len(self.first_player.type()) > 1:
                self.board.pop()
            if len(self.second_player.type()) >1:
                self.board.pop()

    def start(self):
        self.gui.run()
