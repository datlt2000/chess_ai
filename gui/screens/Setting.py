import pygame
import sys
from pygame.locals import *
from confic.const import *
from confic.confic import Confic

# Class that display board setting
class Setting:
    # Singleton
    _instance = None

    @staticmethod
    def getInstance():
        if Setting._instance == None:
            Setting()
        return Setting._instance

    def __init__(self):
        if Setting._instance != None:
            raise Exception("This is singleton class")
        Setting._instance = self
        Confic.loadConfic()
        self.backgrounds = self.getBackgrounds()
        self.pieces = self.getPieces()
        self.boards = self.getBoards()
        self.background = Confic._backgroundType
        self.piece = Confic._pieceType
        self.board = Confic._boardType

    def refresh(self):
        pass
    
    # Get background list and return array of surface
    def getBackgrounds(self):
        arr = Confic.getBackgrounds()
        background = []
        for bg in arr:
            temp = pygame.transform.scale(
                pygame.image.load("gui\\images\\bg\\" + bg + ".jpg").convert_alpha(), (200, 150))
            background.append([bg, temp])
        return background

    # Get piece list and return array of surface
    def getPieces(self):
        arr = Confic.getPieces()
        pieces = []
        for p in arr:
            piece = pygame.transform.scale(
                pygame.image.load("gui\\images\\pieces\\" + p + "\\bk.png").convert_alpha(), (80, 80))
            pieces.append([p, piece])
        return pieces

    # Get board list and return array of surface
    def getBoards(self):
        arr = Confic.getBoards()
        boards = []
        for p in arr:
            board = pygame.transform.scale(
                pygame.image.load("gui\\images\\boards\\" + p + ".png").convert_alpha(), (150, 150))
            boards.append([p, board])
        return boards

    # Return surface that display setting screen
    def getSurface(self):
        container = pygame.Surface(
            (CONTAINER_WIDTH, 900), SRCALPHA)
        i = 0
        for bg in self.backgrounds:
            container.blit(bg[1], (i*210, 0))
            if bg[0] == self.background:
                rect = bg[1].get_rect()
                rect.topleft = (i*210, 0)
                pygame.draw.rect(container, PRIMARY, rect,
                                 width=10, border_radius=5)
            i += 1
        i = 0
        for b in self.boards:
            container.blit(b[1], (170*(i % 5), 170 + 170*(i//5)))
            if b[0] == self.board:
                rect = b[1].get_rect()
                rect.topleft = (170*(i % 5), 170 + 170*(i//5))
                pygame.draw.rect(container, SUCCESS, rect,
                                 width=8, border_radius=5)
            i += 1
        i = 0
        for p in self.pieces:
            container.blit(p[1], (100*i, 680))
            if p[0] == self.piece:
                rect = p[1].get_rect()
                rect.topleft = (100*i, 680)
                pygame.draw.rect(container, DANGER, rect,
                                 width=5, border_radius=10)
            i += 1
        return container

    def getType(self):
        return "Set Board"

    def onClick(self, x_mouse, y_mouse):
        if y_mouse < 50:
            return
        elif y_mouse < 190 and y_mouse > 60:  # fist bg has height from 0 to 150
            if x_mouse % 210 > 10 and x_mouse % 210 < 190:    # x_mouse 200-210, 410-420,... are space
                # width of board is 200 + 10 which is space
                Confic.saveBackground(self.backgrounds[x_mouse//210][0])
                self.background = self.backgrounds[x_mouse//210][0]
        elif y_mouse > 230 and y_mouse < 370:   # first board row has height from 170 to 330
            if x_mouse % 170 > 10 and x_mouse % 170 < 140:
                # width of board is 160 + 10 which is space
                Confic.saveBoard(self.boards[x_mouse//170][0])
                self.board = self.boards[x_mouse//170][0]
        elif y_mouse > 400 and y_mouse < 540:   # second board row has height from 340 to 500
            if x_mouse % 170 > 10 and x_mouse % 170 < 140:
                Confic.saveBoard(self.boards[x_mouse//170 + 5][0])
                self.board = self.boards[x_mouse//170 + 5][0]
        elif y_mouse > 570 and y_mouse < 710:
            if x_mouse % 170 > 10 and x_mouse % 170 < 140:
                if x_mouse // 170 < 3:
                    Confic.saveBoard(self.boards[x_mouse//170 + 10][0])
                    self.board = self.boards[x_mouse//170 + 10][0]
        elif y_mouse > 740 and y_mouse < 800:  # first piece has height from 510 to 590
            if x_mouse % 100 > 10 and x_mouse % 100 < 70:  # x_mouse 80-100, 180-200,... are space
                # width of piece is 80 + 20 is space
                if x_mouse // 100 < 5:
                    Confic.savePiece(self.pieces[x_mouse // 100][0])
                    self.piece = self.pieces[x_mouse // 100][0]

    # Run GUI and initialize pygame
    def run(self):
        pygame.init()
        WINDOW = pygame.display.set_mode((WINDOWN_WIDTH, WINDOWN_HEIGHT))
        pygame.display.set_caption("Chinese Chess")
        self.render(WINDOW)

    # Display board setting to WINDOW
    # @param WINDOW {surface}: game window that display everything
    def render(self, WINDOW):
        if(WINDOW == None):
            return False
        fpsClock = pygame.time.Clock()
        # Initial background
        background = pygame.image.load(
            'gui\\images\\bg\\' + Confic._backgroundType + '.jpg')
        background = pygame.transform.scale(
            background, (WINDOWN_WIDTH, WINDOWN_HEIGHT))

        redirect = None
        loop = True
        # Create submit button
        font = pygame.font.Font("freesansbold.ttf", 28)
        text = font.render("OK", True, WHITE)
        rect = text.get_rect()
        rect.center = (830, 615)
        button = pygame.Rect(780, 590, 100, 50)
        # Loop
        offset = 0
        while loop:
            x_mouse, y_mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        offset = min(offset + 15, 0)
                    elif event.button == 5:
                        offset = max(offset - 15, -200)
                    else:
                        if button.collidepoint((x_mouse, y_mouse)):
                            loop = False
                        if x_mouse < CONTAINER_WIDTH + 50 and x_mouse > 50:
                            self.onClick(x_mouse - 50, y_mouse - offset)

            # Fill background
            WINDOW.fill(WHITE)
            WINDOW.blit(background, (0, 0))

            # Display setting screen
            surface = self.getSurface()
            WINDOW.blit(surface, (50, offset + 50))
            pygame.draw.rect(WINDOW, PRIMARY, button, border_radius=5)
            WINDOW.blit(text, rect)

            pygame.display.update()
            fpsClock.tick(FPS)

        # Break while = back to menu
