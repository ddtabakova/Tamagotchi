import numpy
import pygame
import random
from datetime import timedelta
from collections import OrderedDict
from button import Button
from panda import Panda
from progress_bar import ProgressBar
from parallel_date import ParallelDate


class Game:
    running = True

    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)

    def main(self):
        self.screen.fill((240, 240, 240))
        pygame.display.set_caption('Tamagotchi')
        bg = pygame.image.load('Bamboo.png')
        self.screen.blit(bg, (0, 50))

        self.buttons = []
        for i in range(0,5):
            button_name = "button-{0}.png".format(i)
            b = Button(23 + i*75, 410, 75, 75, button_name, self.action)
            b.display(self.screen)
            self.buttons.append(b)

        self.progress_bars = OrderedDict([('feed', None), ('play',  None), ('clean', None),
                              ('sleep', None), ('cure', None)])
        i = 0
        for k in self.progress_bars.keys():
            p = ProgressBar(70*i + 15, 7, 60, 20, 0.0, self.screen)
            self.progress_bars[k] = p;
            i = i + 1

        pygame.display.update()
        self.panda = Panda()

        pygame.time.set_timer(self.panda.EVENT_HUNGRY, 30000 )
        pygame.time.set_timer(self.panda.EVENT_DIRTY, 30000)
        pygame.time.set_timer(self.panda.EVENT_PLAYFUL, 75000)
        pygame.time.set_timer(self.panda.EVENT_SLEEPY, 75000)
        
        playtime = 0.0
        clock = pygame.time.Clock()

        font = pygame.font.SysFont("Helvetica", 14)
        t_date = ParallelDate(144.0)
        while self.running:
            time = pygame.time.get_ticks()
            self.panda.update(time)
#            self.screen.blit(bg, (0, 0))
 #           self.screen.blit(panda.getimage(), (0,0))

            self.progress_bars['feed'].update_progress(self.panda.get_feed())
            self.progress_bars['play'].update_progress(self.panda.get_play())
            self.progress_bars['clean'].update_progress(self.panda.get_clean())
            self.progress_bars['sleep'].update_progress(self.panda.get_sleep())
            self.progress_bars['cure'].update_progress(self.panda.get_cure())

            playtime += (clock.tick()/1000)
            t_date.update_date(playtime)
            time_display = t_date.get_days() + " d " + t_date.get_hours() + " h "+  t_date.get_minutes() + " m"
            time_label = font.render(time_display, 0, (0, 0, 0), (240, 240, 240))
            self.screen.blit(time_label, (200, 33))
            
            happiness_display = str(int(self.panda.get_happiness()*100))
            happiness_label = font.render("Happiness: " + happiness_display + "%", 0, (0, 0, 0), (240, 240, 240))
            self.screen.blit(happiness_label, (15, 33))

            pygame.display.update()
            for event in pygame.event.get():
                #print(event.type)
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(0,5):
                        b = self.buttons[i]
                        if b.pressed(event.pos):
                            b.action(i)
                            print("{0} button pressed!".format(i));
                elif event.type == self.panda.EVENT_HUNGRY:
                    print("feed update")
                    self.panda.update_hungry(-1)
                elif event.type == self.panda.EVENT_DIRTY:
                    print("dirty update")
                    self.panda.update_dirty(-1)
                elif event.type == self.panda.EVENT_PLAYFUL:
                    print("playful update")
                    self.panda.update_playful(-1)
                elif event.type == self.panda.EVENT_SLEEPY:
                    print("sleepy update")
                    self.panda.update_sleepy(-1)
                elif event.type == self.panda.EVENT_ILL:
                    print("ill event")
                    self.panda.update_ill(-1)

    def action(self, index):
        if index == 0:
            self.panda.update_hungry(1)
            
            

if __name__ == '__main__':
    Game((420, 480)).main()
