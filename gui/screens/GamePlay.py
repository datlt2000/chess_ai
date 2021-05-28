import pygame
import sys
from pygame.locals import *
from confic.confic import Confic
from confic.const import *
from gui.screens.Board import Board

# Class that display board (main game)
class GamePlay:
    # Singleton
    _instance = None

    @staticmethod
    def getInstance():
        if GamePlay._instance == None:
            GamePlay()
        return GamePlay._instance

    def __init__(self):
        if GamePlay._instance != None:
            raise Exception("This is singleton class")

        # Class which display board and piece
        self.board = Board.getInstance()
        self.reset()
        GamePlay._instance = self

    # refresh state of screen
    def refresh(self):
        self.board.updateState()

    def getSurface(self):
        board = self.board.drawBoard()
        container = self.container.copy()
        container.blit(board, (0, 0))
        return container

    def reset(self):
        self.container = pygame.Surface(
            (CONTAINER_WIDTH, CONTAINER_HEIGHT), SRCALPHA)
        self.undoButton = pygame.Rect(BOARD_WIDTH + 50, BOARD_HEIGHT//2 - 100, 160, 50)
        self.resetButton = pygame.Rect(BOARD_WIDTH + 50, BOARD_HEIGHT//2 + 40, 160, 50)

        self.board.reset()

        # draw button
        text1, rect1 = self.createButton("Reset", self.resetButton.center) # reset button
        pygame.draw.rect(self.container, DANGER, self.resetButton)
        self.container.blit(text1, rect1)
        
        text3, rect3 = self.createButton("Undo", self.undoButton.center) # undo button
        pygame.draw.rect(self.container, PRIMARY, self.undoButton)
        self.container.blit(text3, rect3)

    def onClick(self, x_mouse, y_mouse):
        if (x_mouse < BOARD_WIDTH) and (y_mouse < BOARD_HEIGHT):
            if (x_mouse > 0) and (y_mouse > 0):
                self.board.onClick(x_mouse, y_mouse)    # If click on piece
        else:
            if self.undoButton.collidepoint((x_mouse, y_mouse)):
                self.board.undo()
            elif self.resetButton.collidepoint((x_mouse, y_mouse)):
                self.reset()

    def getType(self):
        return "Game 2 Player"

    def createButton(self, title, center):
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render(title, True, WHITE)    # title
        textRect = text.get_rect()
        textRect.center = center
        return text, textRect
        
    # Display screen to window
    # @param WINDOW {surface} app window
    def render(self, WINDOW):
        if(WINDOW == None):
            return False
        fpsClock = pygame.time.Clock()
        self.reset()
        # Background initialization
        background = pygame.image.load(
            'gui\\images\\bg\\' + Confic._backgroundType + '.jpg')
        background = pygame.transform.scale(
            background, (WINDOWN_WIDTH, WINDOWN_HEIGHT))
        
        # Set type of board and piece
        self.board.setBoard(boardType=Confic._boardType, pieceType=Confic._pieceType)

        # Exit button
        font = pygame.font.Font("freesansbold.ttf", 28)
        text = font.render("Back", True, (255, 0, 0))
        textRect = text.get_rect()
        textRect.center = (85, 30)

        # Loop game
        loop = True
        while loop:
            # Handle event
            x_mouse, y_mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (x_mouse > 50) and (y_mouse > 50) and (x_mouse < CONTAINER_WIDTH + 50)\
                            and (y_mouse < CONTAINER_HEIGHT + 50):
                        self.onClick(x_mouse - 50, y_mouse - 50)
                    if textRect.collidepoint((x_mouse, y_mouse)):
                        loop = False    # Exit

            # Fill background
            WINDOW.fill(WHITE)
            WINDOW.blit(background, (0, 0))

            # Render current window
            container = self.getSurface()
            WINDOW.blit(container, (50, 50))
            WINDOW.blit(text, textRect)

            pygame.display.update()
            fpsClock.tick(FPS)

        # Break while = back to menu

    # Run GUI and initialize window
    def run(self):
        # Setting game window
        pygame.init()
        WINDOW = pygame.display.set_mode((WINDOWN_WIDTH, WINDOWN_HEIGHT))
        pygame.display.set_caption('Chinese Chess')
        self.render(WINDOW)
