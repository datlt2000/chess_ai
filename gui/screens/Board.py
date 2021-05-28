import pygame
from pygame.locals import *
import sys
import copy
from confic.const import *
from confic.confic import Confic
from ai.environments.manager import Environment

# size is tuple that is (width, length)
# return a dictionary of piece image
def pieceConvert(size, type):
    dictionary = {}
    pieces = PIECES
    for piece in pieces:
        dictionary[piece] = pygame.transform.scale(pygame.image.load(
            'gui\\images\\pieces\\' + type + "\\" + piece + '.png').convert_alpha(), size)
    return dictionary

'''
    singleton class that render board 
'''
class Board:
    # Singleton
    _instance = None
    
    @staticmethod
    def getInstance():
        if Board._instance is None:
            Board(Confic._boardType, Confic._pieceType)
        return Board._instance

    def __init__(self, type, piece):
        if Board._instance is not None:
            raise Exception("This is Singleton Class")
        self.setBoard(type, piece)
        self.inPlay = True
        self.board = Environment.getInstance()
        self.state = self.board.getState()
        self.last_square = None
        self.now_square = None
        self.turn = self.board.changeTurn()
        self.game_over = False
        Board._instance = self

    # Set image for board and piece
    def setBoard(self, boardType, pieceType):
        temp = pygame.image.load("gui\\images\\boards\\" + boardType + ".png")
        self.surface = pygame.transform.scale(temp.convert_alpha(), (BOARD_WIDTH, BOARD_HEIGHT)) #size of window
        self.piece = pieceConvert((SQUARE_SIZE, SQUARE_SIZE), pieceType)

    def endGame(self):
        self.game_over = True

    # update position of piece
    def updateState(self):
        self.state = self.board.getState()
        self.last_square, self.now_square = self.board.recentMove()
        if not self.board.isPlay():
            self.endGame()
        self.turn = self.board.changeTurn()
    
    def reset(self):
        self.board.reset()
        self.updateState()
        self.last_square = None
        self.now_square = None
        self.turn = self.board.changeTurn()
        self.game_over = False
        self.inPlay = True

    def undo(self):
        self.board.undo()
        self.updateState()
        
    # return pygame surface that render board
    def drawBoard(self):
        """ 
        draw component including board, piece, text,...
        """
        surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        surface.blit(self.surface, (0, 0))
        # chosed piece
        if self.last_square is not None:
            pygame.draw.rect(surface, (218, 195, 50), \
                [(self.last_square[1]*SQUARE_SIZE), self.last_square[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE])
        if self.now_square is not None:
            pygame.draw.rect(surface, (247, 236, 91), \
                [(self.now_square[1]*SQUARE_SIZE), self.now_square[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE])

        # draw pieces
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] != " " and self.state[i][j] != ".":
                    surface.blit(self.piece[self.state[i][j]],
                             (j*SQUARE_SIZE, i*SQUARE_SIZE))
            
        if self.game_over:
            font = pygame.font.Font('freesansbold.ttf', 54)
            text = font.render('Game over', True, (0, 255, 0), (0, 0, 128))
            text_rect = text.get_rect()
            text_rect.center = (4*SQUARE_SIZE, 4*SQUARE_SIZE)
            surface.blit(text, text_rect)

        return surface

    def onClick(self, x_mouse, y_mouse):
        col = int(x_mouse)//SQUARE_SIZE
        row = int(y_mouse)//SQUARE_SIZE
        if self.state[row][col][0] == self.turn:
            self.last_square = (row, col)
            self.now_square = None
        else:
            if self.last_square is None:
                return None
            if self.now_square is None:
                if self.board.move(self.last_square, (row, col)):
                    self.now_square = (row, col)
                    self.updateState()

    def eventHandler(self):
        '''
            handling mouse events and reacting to them
        '''
        x_mouse, y_mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.inPlay=False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x_mouse//SQUARE_SIZE < 8 and y_mouse//SQUARE_SIZE < 8:
                    self.onClick(x_mouse, y_mouse)

    # run only board screen
    def run(self):
        pygame.init()
        window = pygame.display.set_mode((SQUARE_SIZE*8, SQUARE_SIZE*8))
        pygame.display.set_caption("chess")
        while self.inPlay:
            self.eventHandler()
            container = self.drawBoard()
            window.blit(container, (0, 0))
            pygame.display.update()
        pygame.quit()
        sys.exit()