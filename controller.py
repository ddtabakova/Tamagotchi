import pygame
from datetime import timedelta
from collections import OrderedDict
from button import Button
from panda import Panda
from progress_bar import ProgressBar
from progress_bars_controller import ProgressBarController
from parallel_date import ParallelDate

BG_COLOR = (240, 240, 240)
BG_IMAGE = pygame.image.load('images/Bamboo.png')
BG_IMAGE_BOTTOM = pygame.image.load('images/bottom-bg.png')
BG_IMAGE_TOP = pygame.image.load('images/top-bg.png')
LABELS_FONT = pygame.font.SysFont("Ariel", 20)


class GameController:

    def __init__(self, screen):
        self.__screen = screen
        self.__playtime = 0.0
        self.__clock = pygame.time.Clock()
        self.__date = ParallelDate(144.0)
        self.__panda = Panda()
        self.__setup_panda(self.__panda)
        self.__initialize()

    def __initialize(self):
        """set up game screen elements"""
        self.__screen.blit(BG_IMAGE, (0, 50))
        self.__screen.blit(BG_IMAGE_BOTTOM, (0, 405))
        self.__screen.blit(BG_IMAGE_TOP, (0, 0))
        ticks = pygame.time.get_ticks()
        for image in self.__panda.get_panda_view(ticks):
            self.__screen.blit(image, (90, 90))

        self.__buttons = []
        self.__setup_buttons(self.__buttons)
        self.__setup_progress_bars()

    def __setup_buttons(self, buttons):
        """set up control buttons"""
        for i in range(0, 5):
            name = "images/button-{0}.png".format(i)
            button = Button(23 + i*75, 410, 75, 75, name,
                            self.__button_pressed)
            button.display(self.__screen)
            buttons.append(button)

    def __setup_panda(self, panda):
        """initialize panda event timers"""
        pygame.time.set_timer(panda.EVENT_HUNGRY, panda.TIME_HUNGRY)
        pygame.time.set_timer(panda.EVENT_DIRTY, panda.TIME_DIRTY)
        pygame.time.set_timer(panda.EVENT_PLAYFUL, panda.TIME_PLAYFUL)
        pygame.time.set_timer(panda.EVENT_SLEEPY, panda.TIME_SLEEPY)

    def __setup_progress_bars(self):
        """creates all progress bars and a progress controller for them"""
        pbs = OrderedDict([('feed', None), ('play',  None), ('clean', None),
                          ('sleep', None), ('cure', None)])
        i = 0
        for k in pbs.keys():
            pb = ProgressBar(72*i + 37, 23, 60, 20, 0.0, self.__screen)
            pbs[k] = pb
            i = i + 1
        self.__pb_controller = ProgressBarController(pbs)

    def __update_progress(self):
        self.__pb_controller.feed.update_progress(self.__panda.get_feed())
        self.__pb_controller.play.update_progress(self.__panda.get_play())
        self.__pb_controller.clean.update_progress(self.__panda.get_clean())
        self.__pb_controller.sleep.update_progress(self.__panda.get_sleep())
        self.__pb_controller.cure.update_progress(self.__panda.get_cure())

    def __update_game_info(self):
        """renders happiness and time labels"""
        happy_value = str(int(self.__panda.get_happiness()*100))
        happy_text = "Happiness: {0}%".format(happy_value)
        happy_label = LABELS_FONT.render(happy_text, 0, (1, 1, 1), None)
        self.__screen.blit(happy_label, (12, 52))

        self.__date.update_date(self.__playtime)
        d = self.__date.get_days()
        h = self.__date.get_hours()
        m = self.__date.get_minutes()
        time_display = "{0} d {1} h {2} m".format(d, h, m)
        time_label = LABELS_FONT.render(time_display, 0, (1, 1, 1), None)
        self.__screen.blit(time_label, (200, 52))

    def __button_pressed(self, index):
        """button pressed callback actions"""
        if not self.__panda:
            return
        if index == 0:
            self.__panda.eat()
        elif index == 1:
            self.__panda.play()
        elif index == 2:
            self.__panda.bath()
        elif index == 3:
            self.__panda.sleep()
        elif index == 4:
            self.__panda.heal()

    def update_game(self):
        self.__initialize()
        if self.__panda.get_alive():
            self.__playtime += (self.__clock.tick()/1000)
        self.__update_progress()
        self.__update_game_info()
        pygame.display.update()

    def handle_event(self, event):
        if not self.__panda.get_alive():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.__panda = Panda()
                self.__playtime = 0.0
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(0, 5):
                b = self.__buttons[i]
                if b.pressed(event.pos):
                    b.action(i)
        if event.type == self.__panda.EVENT_HUNGRY:
            self.__panda.update_hungry(self.__panda.NEGATIVE_UPDATE)
        elif event.type == self.__panda.EVENT_DIRTY:
            self.__panda.update_dirty(self.__panda.NEGATIVE_UPDATE)
        elif event.type == self.__panda.EVENT_PLAYFUL:
            self.__panda.update_playful(self.__panda.NEGATIVE_UPDATE)
        elif event.type == self.__panda.EVENT_SLEEPY:
            self.__panda.update_sleepy(self.__panda.NEGATIVE_UPDATE)
        elif event.type == self.__panda.EVENT_ILL:
            self.__panda.update_ill(self.__panda.NEGATIVE_UPDATE)
