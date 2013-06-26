import numpy
import pygame
pygame.init()

BG_COLOR_POSITIVE = (160, 203, 60)
BG_COLOR_NEGATIVE = (255, 0, 0)
BG_COLOR = (250, 250, 180)

class ProgressBar:

    def __init__(self, origin_x, origin_y, size_width, size_height,
                 initial_progress, screen):
        self.rect = pygame.Rect(origin_x, origin_y, size_width, size_height)
        self.bg_color = BG_COLOR
        self.screen = screen
        self.update_progress(initial_progress)

    def update_progress(self, progress):
        self.progress = progress
        self.progress_width = self.rect.w*progress
        if progress < 0.5:
            self.progress_color = BG_COLOR_NEGATIVE
        else:
            self.progress_color = BG_COLOR_POSITIVE

        self.__display(self.screen)


    def __display(self, surface):
        pygame.draw.rect(surface, (60, 110, 20), self.rect, 3)
        pygame.draw.rect(surface, self.bg_color, self.rect, 0)
        pygame.draw.rect(surface, self.progress_color,
                         (self.rect.x, self.rect.y,
                          self.progress_width, self.rect.h))        
