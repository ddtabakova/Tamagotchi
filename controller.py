import pygame
from datetime import timedelta
from collections import OrderedDict
from button import Button
from panda import Panda
from progress_bar import ProgressBar
from progress_bars_controller import ProgressBarController
from parallel_date import ParallelDate

BG_COLOR = (240, 240, 240)
BG_IMAGE = pygame.image.load('Bamboo.png')

class GameController:

    
    def __init__(self, screen):
        self.__screen = screen
        self.__initialize()
        self.__panda = Panda()
        self.__setup_panda(self.__panda)

    def __initialize(self):
        #set up game elements
        self.__screen.fill(BG_COLOR)
        self.__screen.blit(BG_IMAGE, (0, 50))
        self.__buttons = []
        self.__setup_buttons(self.__buttons)
        self.__setup_progress_bars()

    def __setup_buttons(self, buttons):
        #set up control buttons
        for i in range(0,5):
            name = "button-{0}.png".format(i)
            button = Button(23 + i*75, 410, 75, 75, name, self.__button_pressed)
            button.display(self.__screen)
            buttons.append(button)

    def __setup_panda(self, panda):
        #initialize panda event timers
        pygame.time.set_timer(panda.EVENT_HUNGRY, panda.TIME_HUNGRY)
        pygame.time.set_timer(panda.EVENT_DIRTY, panda.TIME_DIRTY)
        pygame.time.set_timer(panda.EVENT_PLAYFUL, panda.TIME_PLAYFUL)
        pygame.time.set_timer(panda.EVENT_SLEEPY, panda.TIME_SLEEPY)

    def __setup_progress_bars(self):
        pbs = OrderedDict([('feed', None), ('play',  None), ('clean', None),
                          ('sleep', None), ('cure', None)])
        i = 0
        for k in pbs.keys():
            pb = ProgressBar(70*i + 15, 7, 60, 20, 0.0, self.__screen)
            pbs[k] = pb;
            i = i + 1
        self.__pb_controller = ProgressBarController(pbs)

    def __update_progress(self):
        self.__pb_controller.feed.update_progress(self.__panda.get_feed())
        self.__pb_controller.play.update_progress(self.__panda.get_play())
        self.__pb_controller.clean.update_progress(self.__panda.get_clean())
        self.__pb_controller.sleep.update_progress(self.__panda.get_sleep())
        self.__pb_controller.cure.update_progress(self.__panda.get_cure())

    def __update_game_info(self):
        
        
    def __button_pressed(self, index):
        #button action
        if index == 0:
            self.__panda.update_hungry(self.__panda.POSITIVE_UPDATE)
        elif index == 1:
            self.__panda.update_playful(self.__panda.POSITIVE_UPDATE)
        elif index == 2:
            self.__panda.update_dirty(self.__panda.POSITIVE_UPDATE)
        elif index == 3:
            self.__panda.update_sleepy(self.__panda.POSITIVE_UPDATE)
        elif index == 4:
            self.__panda.update_ill(self.__panda.POSITIVE_UPDATE)

    def handle_event(self, event):
        pygame.display.update()
        self.__update_progress()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(0,5):
                b = self.__buttons[i]
                if b.pressed(event.pos):
                    b.action(i)
        elif event.type == self.__panda.EVENT_HUNGRY:
            self.__panda.update_hungry(self.__panda.NEGATIVE_UPDATE)
        elif event.type == self.__panda.EVENT_DIRTY:
            self.__panda.update_dirty(self.__panda.NEGATIVE_UPDATE)
        elif event.type == self.__panda.EVENT_PLAYFUL:
            self.__panda.update_playful(self.__panda.NEGATIVE_UPDATE)
        elif event.type == self.__panda.EVENT_SLEEPY:
            self.__panda.update_sleepy(self.__panda.NEGATIVE_UPDATE)
        elif event.type == self.__panda.EVENT_ILL:
            self.__panda.update_ill(self.__panda.NEGATIVE_UPDATE)


    
