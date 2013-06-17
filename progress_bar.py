import numpy
import pygame
pygame.init()


class ProgressBar:

    def __init__(self, origin_x, origin_y, size_width, size_height,
                 initial_progress, screen):
        self.rect = pygame.Rect(origin_x, origin_y, size_width, size_height)
        self.bg_color = (192, 192, 192)
        self.screen = screen
        self.update_progress(initial_progress)

    def update_progress(self, progress):
        self.progress = progress
        self.progress_width = self.rect.w*progress
        if progress < 0.5:
            self.progress_color = (255, 0, 0)
        else:
            self.progress_color = (0, 255, 0)

        self.display(self.screen)


    def display(self, surface):
        pygame.draw.rect(surface, (60, 110, 20), self.rect, 3)
        pygame.draw.rect(surface, self.bg_color, self.rect, 0)
        pygame.draw.rect(surface, self.progress_color,
                         (self.rect.x, self.rect.y,
                          self.progress_width, self.rect.h))

        font = pygame.font.SysFont("Helvetica", 11)
 #       label = font.render("100%", 1, (0, 0, 0))
#        surface.blit(label, (self.rect.x+self.rect.w + 3.0,
#                             self.rect.y+(self.rect.h-label.get_rect().h)*0.5))
        
