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
    STATE_DEAD = -1

    TIME_HUNGRY = 20000
    TIME_DIRTY = 50000
    TIME_PLAYFUL = 25000
    TIME_SLEEPY = 30000

    EVENT_HUNGRY = pygame.USEREVENT + 1
    EVENT_DIRTY = pygame.USEREVENT + 2
    EVENT_PLAYFUL = pygame.USEREVENT + 3
    EVENT_SLEEPY = pygame.USEREVENT + 4
    EVENT_ILL = pygame.USEREVENT + 5

    UPDATE_FEED_BY = 0.25
    UPDATE_CLEAN_BY = 0.50
    UPDATE_PLAY_BY = 0.25
    UPDATE_SLEEP_BY = 0.25
    UPDATE_CURE_BY = 0.50

    POSITIVE_UPDATE = 1.0
    NEGATIVE_UPDATE = -1.0

    NORMAL_PANDA = pygame.image.load('images/panda_sprite_normal.png')
    EATING_PANDA = pygame.image.load('images/panda_sprite_eating.png')
    ANGRY_PANDA = pygame.image.load('images/panda_sprite_angry.png')
    BATH_PANDA = pygame.image.load('images/panda_sprite_bath.png')
    SLEEPY_PANDA = pygame.image.load('images/panda_sprite_sleep.png')
    HEALING_PANDA = pygame.image.load('images/panda_sprite_cure.png')
    PLAYING_PANDA = pygame.image.load('images/panda_sprite_play.png')
    HAPPY1_PANDA = pygame.image.load('images/panda_sprite_happy1.png')
    HAPPY2_PANDA = pygame.image.load('images/panda_sprite_happy2.png')
    HAPPY3_PANDA = pygame.image.load('images/panda_sprite_happy3.png')
    DIRTY1_PANDA = pygame.image.load('images/panda_dirty1.png')
    DIRTY2_PANDA = pygame.image.load('images/panda_poop.png')
    SICK1_PANDA = pygame.image.load('images/panda_sick1.png')
    SICK2_PANDA = pygame.image.load('images/panda_sick2.png')
    DEAD_PANDA = pygame.image.load('images/panda_sprite_dead.png')

    def __init__(self):
        self._panda_view = PandaView(self.NORMAL_PANDA, 250, 300)
        self._is_alive = True
        self._feed = 1.0
        self._play = 1.0
        self._clean = 1.0
        self._sleep = 1.0
        self._cure = 1.0
        self._state = self.STATE_NORMAL
        self._happy_images = [
            self.HAPPY1_PANDA,
            self.HAPPY2_PANDA,
            self.HAPPY3_PANDA]
        self.calculate_happiness()

 #-------->getters
    def get_happiness(self):
        return self._happiness

    def get_feed(self):
        return self._feed

    def get_play(self):
        return self._play

    def get_clean(self):
        return self._clean

    def get_sleep(self):
        return self._sleep

    def get_cure(self):
        return self._cure

    def get_alive(self):
        return self._is_alive

    def get_panda_view(self, time):
        images = [self._panda_view.get_image(time)]
        if (self._state == self.STATE_SLEEPING or
                self._state == self.STATE_BATHING):
            return images
        if self._clean < 1.0:
                images.append(self.DIRTY1_PANDA)
                if self._clean < 0.5:
                        images.append(self.DIRTY2_PANDA)
        if self._cure < 1.0 and self._state != self.STATE_HEALING:
            images.append(self.SICK1_PANDA)
            if self._cure < 0.5:
                images.append(self.SICK2_PANDA)

        return images

    def calculate_happiness(self):
        self._happiness = (self._feed + self._clean + self._play
                           + self._sleep + self._cure)/5
        self.__check_cure()
        self.__check_sleep()
        self.__check_kill()

    def kill(self):
        self._feed = 0.0
        self._play = 0.0
        self._clean = 0.0
        self._sleep = 0.0
        self._cure = 0.0
        self._is_alive = False
        self._state = self.STATE_DEAD
        self._panda_view.change_state(self.DEAD_PANDA)

 #-------->auto activities
    def __check_kill(self):
        if self._happiness < 0.1:
            self.kill()

    def __check_cure(self):
        if (self._happiness < 0.5 or self._feed == 0.0 or
                self._sleep == 0.0 or self._clean == 0.0):
            if self.__should_make_ill():
                self.update_ill(self.NEGATIVE_UPDATE)

    def __should_make_ill(self):
        if self._cure > 0.0:
            r = random.randint(1, 10)
            if r < 4:
                return True
        return False

    def __check_sleep(self):
        if self._sleep == 0.0:
            self.sleep()

 #-------->activity methods
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
        self._sleep_timer = Timer(6.0, self.sleep)
        self._sleep_timer.start()

    def play(self):
        change_state = self._go_do_this(
            self._play,
            self.PLAYING_PANDA,
            4.0,
            self.update_playful)

        if change_state:
            self._state = self.STATE_PLAYING

    def eat(self):
        change_state = self._go_do_this(
            self._feed,
            self.EATING_PANDA,
            5.0,
            self.update_hungry)

        if change_state:
            self._state = self.STATE_EATING

    def bath(self):
            change_state = self._go_do_this(
                self._clean,
                self.BATH_PANDA,
                3.0,
                self.update_dirty)

            if change_state:
                self._state = self.STATE_BATHING

    def heal(self):
        change_state = self._go_do_this(
            self._cure,
            self.HEALING_PANDA,
            4.0,
            self.update_ill)

        if change_state:
            self._state = self.STATE_HEALING

    def _go_do_this(self, feeling, state_image, time, callback):
        if ((self._state == self.STATE_NORMAL and feeling == 1.0) or
                self._state == self.STATE_SLEEPING):
            if self._state == self.STATE_SLEEPING:
                print(self._sleep_timer)
                if self._sleep_timer:
                    self._sleep_timer.cancel()
                self._state = self.STATE_NORMAL
            self._go_angry()
            return False
        if self._state != self.STATE_NORMAL:
            return False
        self._panda_view.change_state(state_image)
        self._activity_timer = Timer(
            time,
            self._finish_activity,
            [callback]).start()
        return True

    def _go_angry(self):
        self._panda_view.change_state(self.ANGRY_PANDA)
        self._angry_timer = Timer(3.0, self._go_to_normal).start()

    def _go_to_normal(self):
        self._state = self.STATE_NORMAL
        self._panda_view.change_state(self.NORMAL_PANDA)

    def _finish_activity(self, callback):
        callback(self.POSITIVE_UPDATE)
        self._panda_view.change_state(self._get_happy_face())
        self._happy_timer = Timer(2.0, self._go_to_normal).start()

    def _get_happy_face(self):
        r = random.randint(0, 2)
        return self._happy_images[r]

 #-------->methods which are used for updating the condition of the panda
    def update_hungry(self, is_positive_update):
        u = self.UPDATE_FEED_BY*is_positive_update
        self._feed = self.__update_feeling(self._feed, u, is_positive_update)
        self.calculate_happiness()

    def update_dirty(self, is_positive_update):
        u = self.UPDATE_CLEAN_BY*is_positive_update
        self._clean = self.__update_feeling(self._clean, u, is_positive_update)
        self.calculate_happiness()

    def update_playful(self, is_positive_update):
        u = self.UPDATE_PLAY_BY*is_positive_update
        self._play = self.__update_feeling(self._play, u, is_positive_update)
        self.calculate_happiness()

    def update_sleepy(self, is_positive_update):
        if (self._state == self.STATE_SLEEPING and
                is_positive_update == self.NEGATIVE_UPDATE):
            return
        u = self.UPDATE_SLEEP_BY*is_positive_update
        self._sleep = self.__update_feeling(self._sleep, u, is_positive_update)
        self.calculate_happiness()

    def update_ill(self, is_positive_update):
        u = self.UPDATE_CURE_BY*is_positive_update
        self._cure = self.__update_feeling(self._cure, u, is_positive_update)
        self.calculate_happiness()

    def __update_feeling(self, feeling, update, is_positive_update):
        if is_positive_update == self.POSITIVE_UPDATE:
            feeling = min(feeling+update, 1.0)
        else:
            feeling = max(feeling+update, 0.0)
        return feeling
