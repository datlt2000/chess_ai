import pygame
import sys
from pygame.locals import *

from gui.screens.Setting import Setting
from gui.screens.GamePlay import GamePlay

from confic.const import *
from confic.confic import Confic

from ai.agents.player import Player, Ai

# Class that display menu
class Menu:
    # Singleton
    _instance = None

    @staticmethod
    def getInstance():
        if Menu._instance == None:
            Menu()
        return Menu._instance

    def __init__(self):
        if Menu._instance != None:
            raise Exception("This is singleton class")
        self.loop = True
        Menu._instance = self

    # Set environment
    def setManager(self, manager):
        self.manager = manager
    
    # Update new state {background, chess}
    def refresh(self):
        Confic.loadConfic()
        self.loop = False

    # Display screen to window
    # @param WINDOW {surface} app window
    def render(self, WINDOW):
        if(WINDOW == None):
            return False
        fpsClock = pygame.time.Clock()

        font = pygame.font.Font("freesansbold.ttf", 32)
        # Create button 1
        button1 = pygame.Rect(360, 150, 200, 60) # Create button (X axis, Y axis, width, height)
        text1 = font.render("2 Player", True, WHITE)    # title of button
        textRect1 = text1.get_rect()
        textRect1.center = (460, 180)   # Create frame of title and set position for frame

        # Create button 2
        button2 = pygame.Rect(360, 250, 200, 60)
        text2 = font.render("1 Player", True, WHITE)
        textRect2 = text2.get_rect()
        textRect2.center = (460, 280)

        # Create button 3
        button3 = pygame.Rect(360, 350, 200, 60)
        text3 = font.render("Setting", True, WHITE)
        textRect3 = text3.get_rect()
        textRect3.center = (460, 380)

        # Create button 4
        button4 = pygame.Rect(360, 450, 200, 60)
        text4 = font.render("Exit", True, WHITE)
        textRect4 = text4.get_rect()
        textRect4.center = (460, 480)

        while True:
            # Game loop of pygame
            self.loop = True
            redirect = None

            # Background initialization
            Confic.loadConfic()
            background = pygame.image.load('gui\\images\\bg\\' + Confic._backgroundType +'.jpg')
            background = pygame.transform.scale(
            background, (WINDOWN_WIDTH, WINDOWN_HEIGHT))
            while self.loop:
                # Handle event
                x_mouse, y_mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if(x_mouse > 50 and y_mouse > 50 and x_mouse < (CONTAINER_WIDTH + 50)
                           and y_mouse < (CONTAINER_HEIGHT + 50)):
                            if event.button == 1:
                                if button1.collidepoint((x_mouse, y_mouse)):
                                    redirect = "2Player"
                                    self.loop = False
                                elif button2.collidepoint((x_mouse, y_mouse)):
                                    redirect = "1Player"
                                    self.loop = False
                                elif button3.collidepoint((x_mouse, y_mouse)):
                                    redirect = "Setting"
                                    self.loop = False
                                elif button4.collidepoint((x_mouse, y_mouse)):
                                    redirect = "Exit"
                                    self.loop = False

                # Fill background
                WINDOW.fill(WHITE)
                WINDOW.blit(background, (0, 0))
                pygame.draw.rect(WINDOW, PRIMARY, button1)
                WINDOW.blit(text1, textRect1)
                pygame.draw.rect(WINDOW, SUCCESS, button2)
                WINDOW.blit(text2, textRect2)
                pygame.draw.rect(WINDOW, DANGER, button3)
                WINDOW.blit(text3, textRect3)
                pygame.draw.rect(WINDOW, INFOR, button4)
                WINDOW.blit(text4, textRect4)

                pygame.display.update()
                fpsClock.tick(FPS)

            # redirect
            if redirect == "2Player":
                game = GamePlay.getInstance()
                f = Player("white")
                s = Player("black")
                self.manager.setPlayer1(f)
                self.manager.setPlayer2(s)
                self.manager.setGUI(game)
                game.render(WINDOW)
                self.manager.setGUI(self)
            elif redirect == "Setting":
                setting = Setting.getInstance()
                self.manager.setGUI(setting)
                setting.render(WINDOW)
                self.manager.setGUI(self)
            elif redirect == "Exit":
                pygame.quit()
                sys.exit()
            elif redirect == "1Player":
                game = GamePlay.getInstance()
                f = Player("white")
                s = Ai("black")
                self.manager.setPlayer1(f)
                self.manager.setPlayer2(s)
                self.manager.setGUI(game)
                game.render(WINDOW)
                self.manager.setGUI(self)

    # run GUI and initialize window
    def run(self):
        # Setting game window
        pygame.init()
        WINDOW = pygame.display.set_mode((WINDOWN_WIDTH, WINDOWN_HEIGHT))
        pygame.display.set_caption('Chess')
        self.render(WINDOW)
