import numpy
import pygame
from controller import GameController


class Game:
    running = True

    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)

    def main(self):
        pygame.display.set_caption('Tamagotchi')
        controller = GameController(self.screen)

        while self.running:
            controller.update_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                else:
                    controller.handle_event(event)

if __name__ == '__main__':
    Game((420, 480)).main()
