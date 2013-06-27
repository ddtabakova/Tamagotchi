import pygame
import random
from threading import Timer
from panda_view import PandaView
pygame.init()


class Panda():
    STATE_EATING = 1
    STATE_PLAYING = 2
    STATE_BATHING = 3
    STATE_SLEEPING = 4
    STATE_HEALING = 5
    STATE_NORMAL = 0
    
    TIME_HUNGRY = 10000
    TIME_DIRTY = 10000
    TIME_PLAYFUL = 25000
    TIME_SLEEPY = 25000
    
    EVENT_HUNGRY = pygame.USEREVENT + 1
    EVENT_DIRTY = pygame.USEREVENT + 2
    EVENT_PLAYFUL = pygame.USEREVENT + 3
    EVENT_SLEEPY = pygame.USEREVENT + 4
    EVENT_ILL = pygame.USEREVENT + 5
    
    UPDATE_FEED_BY = 0.20
    UPDATE_CLEAN_BY = 0.25
    UPDATE_PLAY_BY = 0.25
    UPDATE_SLEEP_BY = 0.25
    UPDATE_CURE_BY = 0.50

    POSITIVE_UPDATE = 1.0
    NEGATIVE_UPDATE = -1.0

    NORMAL_PANDA = pygame.image.load('panda_sprite_normal.png')
    EATING_PANDA = pygame.image.load('panda_sprite_eating.png')
    ANGRY_PANDA = pygame.image.load('panda_sprite_angry.png')
    BATH_PANDA = pygame.image.load('panda_sprite_bath.png')
    SLEEPY_PANDA = pygame.image.load('panda_sprite_sleep.png')
    HEALING_PANDA = pygame.image.load('panda_sprite_cure.png')
    PLAYING_PANDA = pygame.image.load('panda_sprite_play.png')

    def __init__(self):
        self._panda_view = PandaView(self.NORMAL_PANDA, 250, 300)
        self._feed = 1.0;
        self._play = 1.0;
        self._clean = 1.0;
        self._sleep = 1.0;
        self._cure = 1.0;
        self._state = self.STATE_NORMAL

        self.calculate_happiness()

    def get_happiness(self):
        return self._happiness
    
    def get_feed(self):
        return self._feed;

    def get_play(self):
        return self._play;

    def get_clean(self):
        return self._clean;

    def get_sleep(self):
        return self._sleep;

    def get_cure(self):
        return self._cure;

    def get_panda_view(self, time):
        return self._panda_view.get_image(time)

    def calculate_happiness(self):
        self._happiness = (self._feed + self._clean + self._play
                           + self._sleep + self._cure)/5
        self.__check_cure()

    def __check_cure(self):
        if self._happiness < 0.5 or self._feed == 0.0 or self._sleep == 0.0 or self._clean == 0.0:
            if self.__should_make_ill():
                self.update_ill(self.NEGATIVE_UPDATE)

    def __should_make_ill(self):
        if self._cure > 0.0:
            r = random.randint(1, 10)
            if r < 4:
                return True
        return False

    def sleep(self):
        if self._state == self.STATE_NORMAL:
            if self._sleep == 1.0:
                self._go_angry()
                return
            self._state = self.STATE_SLEEPING
            self._panda_view.change_state(self.SLEEPY_PANDA)
        elif self._state == self.STATE_SLEEPING:
            self.update_sleepy(self.POSITIVE_UPDATE)
            if self._sleep == 1.0:
                if self._sleep_timer:
                    self._sleep_timer.cancel()
                self._go_to_normal()
                return
        self._sleep_timer = Timer(10.0, self.sleep).start()

    def play(self):
        if self._state == self.STATE_NORMAL:
            if self._play == 1.0:
                self._go_angry()
                return

        self._state = self.STATE_PLAYING
        self._panda_view.change_state(self.PLAYING_PANDA)
        self._play_timer = Timer(4.0, self._finish_activity, [self.update_playful]).start()
            
    def eat(self):
        if self._state == self.STATE_NORMAL:
            if self._feed == 1.0:
                self._go_angry()
                return

            self._state = self.STATE_EATING
            self._panda_view.change_state(self.EATING_PANDA)
            self._eat_timer = Timer(5.0, self._finish_activity, [self.update_hungry]).start()

    def bath(self):
        if self._state == self.STATE_NORMAL:
            if self._clean == 1.0:
                self._go_angry()
                return

            self._state = self.STATE_BATHING
            self._panda_view.change_state(self.BATH_PANDA)
            self._bath_timer = Timer(3.0, self._finish_activity, [self.update_dirty]).start()

    def heal(self):
        if self._state == self.STATE_NORMAL:
            if self._cure == 1.0:
                self._go_angry()
                return

        self._state = self.STATE_HEALING
        self._panda_view.change_state(self.HEALING_PANDA)
        self._heal_timer = Timer(3.0, self._finish_activity, [self.update_ill]).start()
                
    def _go_angry(self):
        self._panda_view.change_state(self.ANGRY_PANDA)
        self._angry_timer = Timer(3.0, self._go_to_normal).start()

    def _go_to_normal(self):
        self._state = self.STATE_NORMAL
        self._panda_view.change_state(self.NORMAL_PANDA)

    def _finish_activity(self, callback):
        self._go_to_normal()
        callback(self.POSITIVE_UPDATE)
        
    def update_hungry(self, is_positive_update):
        if self._state == self.STATE_NORMAL:
            update = self.UPDATE_FEED_BY*is_positive_update
            self._feed = self.__update_feeling(self._feed, update, is_positive_update)
            self.calculate_happiness()

    def update_dirty(self, is_positive_update):
        update = self.UPDATE_CLEAN_BY*is_positive_update
        self._clean = self.__update_feeling(self._clean, update, is_positive_update)
        self.calculate_happiness()

    def update_playful(self, is_positive_update):
        update = self.UPDATE_CLEAN_BY*is_positive_update
        self._play = self.__update_feeling(self._play, update, is_positive_update)
        self.calculate_happiness()

    def update_sleepy(self, is_positive_update):
        if self._state == self.STATE_SLEEPING and is_positive_update == self.NEGATIVE_UPDATE:
            return
        update = self.UPDATE_SLEEP_BY*is_positive_update
        self._sleep = self.__update_feeling(self._sleep, update, is_positive_update)
        self.calculate_happiness()

    def update_ill(self, is_positive_update):
        update = self.UPDATE_CURE_BY*is_positive_update
        self._cure = self.__update_feeling(self._cure, update, is_positive_update)
        self.calculate_happiness()

    def __update_feeling(self, feeling, update, is_positive_update):
        if is_positive_update == self.POSITIVE_UPDATE:
            feeling = min(feeling+update, 1.0)
        else:
            feeling = max(feeling+update, 0.0)
        return feeling
        
