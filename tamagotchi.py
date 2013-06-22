import numpy
import pygame
import random
from datetime import timedelta
from button import Button
from panda import Panda
from progress_bar import ProgressBar
from parallel_date import ParallelDate
from controller import GameController

class Game:
    running = True

    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)

    def main(self):
        pygame.display.set_caption('Tamagotchi')
        controller = GameController(self.screen)
        pygame.display.update()

        
        playtime = 0.0
        clock = pygame.time.Clock()

        font = pygame.font.SysFont("Helvetica", 14)
        t_date = ParallelDate(144.0)
        while self.running:
            time = pygame.time.get_ticks()

            playtime += (clock.tick()/1000)
            t_date.update_date(playtime)
            time_display = t_date.get_days() + " d " + t_date.get_hours() + " h "+  t_date.get_minutes() + " m"
            time_label = font.render(time_display, 0, (0, 0, 0), (240, 240, 240))
            self.screen.blit(time_label, (200, 33))
            
            #happiness_display = str(int(self.panda.get_happiness()*100))
            #happiness_label = font.render("Happiness: " + happiness_display + "%", 0, (0, 0, 0), (240, 240, 240))
            #self.screen.blit(happiness_label, (15, 33))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                else:
                    controller.handle_event(event)

            
            

if __name__ == '__main__':
    Game((420, 480)).main()
