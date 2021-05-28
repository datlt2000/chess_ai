import time

# player interface
class Player:
    def __init__(self, color):
        if color in ['white', 'black']:
            self.color = color[0]
        else:
            raise Exception("cannot create player")

    def type(self):
        return self.color

    def close(self):
        pass

    def action(self):
        return None

import chess
import ai.agents.minimax as minimax

# ai for chess
class Ai(Player):
    def __init__(self, color):
        super().__init__(color)
    
    def type(self):
        color = super().type()
        return "ai" + color
    

    def can_checkmate(self, move, current_board):
        fen = current_board.fen()
        future_board = chess.Board(fen)
        future_board.push(move)
        return future_board.is_checkmate()

    def action(self, current_board, ai_white = False):
        for move in current_board.legal_moves:
            if(self.can_checkmate(move, current_board)):
                return move
    
        number_of_moves = len(list(current_board.legal_moves))

        if(number_of_moves > 30):
            move = minimax.find_move(current_board, 1, ai_white)
            return move
        elif(number_of_moves > 10):
            move = minimax.find_move(current_board, 3, ai_white)
            return move
        else:
            move = minimax.find_move(current_board, 5, ai_white)
            return move