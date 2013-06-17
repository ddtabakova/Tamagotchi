import numpy
import pygame
import random
from datetime import timedelta
from collections import OrderedDict
from button import Button
from panda import Panda
from progress_bar import ProgressBar


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
            b = Button(20 + i*80, 420, 50, 50, 'sample_button.png', self.action)
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
        panda = Panda()

        pygame.time.set_timer(panda.EVENT_HUNGRY, 60000 )
        pygame.time.set_timer(panda.EVENT_DIRTY, 60000)
        pygame.time.set_timer(panda.EVENT_PLAYFUL, 150000)
        pygame.time.set_timer(panda.EVENT_SLEEPY, 150000)
        
        playtime = 0.0
        clock = pygame.time.Clock()

        font = pygame.font.SysFont("Helvetica", 14)

        while self.running:
            time = pygame.time.get_ticks()
            panda.update(time)
#            self.screen.blit(bg, (0, 0))
 #           self.screen.blit(panda.getimage(), (0,0))

            self.progress_bars['feed'].update_progress(panda.get_feed())
            self.progress_bars['play'].update_progress(panda.get_play())
            self.progress_bars['clean'].update_progress(panda.get_clean())
            self.progress_bars['sleep'].update_progress(panda.get_sleep())
            self.progress_bars['cure'].update_progress(panda.get_cure())

            seconds = clock.tick()/1000
            playtime += seconds
            rt = playtime*144
            rt_m, rt = divmod(rt, 60)
            rt_h, rt_m = divmod(rt_m, 60)
            rt_d, rt_h = divmod(rt_h, 24)

            time_display = str(int(rt_d)) + " d " + str(int(rt_h)) + " h " + str(int(rt_m)) + " m"
            time_label = font.render(time_display, 0, (0, 0, 0), (240, 240, 240))
            self.screen.blit(time_label, (200, 33))
            
            happiness_display = str(int(panda.get_happiness()*100))
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
                elif event.type == panda.EVENT_HUNGRY:
                    print("feed update")
                    panda.make_hungry()
                elif event.type == panda.EVENT_DIRTY:
                    print("dirty update")
                    panda.make_dirty()
                elif event.type == panda.EVENT_PLAYFUL:
                    print("playful update")
                    panda.make_playful()
                elif event.type == panda.EVENT_SLEEPY:
                    print("sleepy update")
                    panda.make_sleepy()
                elif event.type == panda.EVENT_ILL:
                    print("ill event")
                    panda.make_ill()

    def action(self, index):
        if index == 0:
            pass
            

if __name__ == '__main__':
    Game((420, 480)).main()
