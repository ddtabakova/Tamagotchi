import pygame


class Button:

    def __init__(self, origin_x, origin_y, size_width, size_height,
                 image_path, action):
        self.rect = pygame.Rect(origin_x, origin_y, size_width, size_height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(self.image,
                                                  (size_width, size_height))
        self.action = action

    def display(self, surface):
        surface.blit(self.image, self.rect)

    def pressed(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
