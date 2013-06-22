import pygame
pygame.init()


class Panda(pygame.sprite.Sprite):
    TIME_HUNGRY = 30000
    TIME_DIRTY = 30000
    TIME_PLAYFUL = 75000
    TIME_SLEEPY = 75000
    
    EVENT_HUNGRY = pygame.USEREVENT + 1
    EVENT_DIRTY = pygame.USEREVENT + 2
    EVENT_PLAYFUL = pygame.USEREVENT + 3
    EVENT_SLEEPY = pygame.USEREVENT + 4
    EVENT_ILL = pygame.USEREVENT + 5
    
    UPDATE_FEED_BY = 0.20
    UPDATE_CLEAN_BY = 0.10
    UPDATE_PLAY_BY = 0.25
    UPDATE_SLEEP_BY = 0.25
    UPDATE_CURE_BY = 0.50

    POSITIVE_UPDATE = 1.0
    NEGATIVE_UPDATE = -1.0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self._start = pygame.time.get_ticks()
        self._delay = 500
        self._last_update = 0
        self._frame = 0

        self._feed = 1.0;
        self._play = 1.0;
        self._clean = 1.0;
        self._sleep = 1.0;
        self._cure = 1.0;

        self.calculate_happiness()
        
        self._images = []
        for i in range(0,2):
            image_path = "{0}.png".format(i+1)
            image = pygame.image.load(image_path)
            self._images.append(image)

        self.image = self._images[0]
        self.update(pygame.time.get_ticks())

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

    def get_image(self):
        return self.image

    def update(self, t):
        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self._images): self._frame = 0
            if self._frame < len(self._images):
                self.image = self._images[self._frame]
                self._last_update = t

    def reset(self):
        if self._frame >= len(self._images): self._frame = 0

    def calculate_happiness(self):
        self._happiness = (self._feed + self._clean + self._play
                           + self._sleep + self._cure)/5
 
    def update_hungry(self, is_positive_update):
        print("update hungry")
        update = self.UPDATE_FEED_BY*is_positive_update
        print(update)
        self._feed = self.__update_feeling(update, is_positive_update)
        self.calculate_happiness()

    def update_dirty(self, is_positive_update):
        update = self.UPDATE_CLEAN_BY*is_positive_update
        self._clean = self.__update_feeling(update, is_positive_update)
        self.calculate_happiness()

    def update_playful(self, is_positive_update):
        update = self.UPDATE_CLEAN_BY*is_positive_update
        self._play = self.__update_feeling(update, is_positive_update)
        self.calculate_happiness()

    def update_sleepy(self, is_positive_update):
        update = self.UPDATE_SLEEP_BY*is_positive_update
        self._sleep = self.__update_feeling(update, is_positive_update)
        self.calculate_happiness()

    def update_ill(self, is_positive_update):
        update = self.UPDATE_CURE_BY*is_positive_update
        self._cure = self.__update_feeling(update, is_positive_update)
        self.calculate_happiness()

    def __update_feeling(self, update, is_positive_update):
        feeling = 1.0
        if is_positive_update == 1:
            feeling = min(feeling+update, 1.0)
        else:
            feeling = max(feeling+update, 0.0)
        return feeling
        
