import pygame
from animated_sprite import AnimatedSprite


class PandaView:

    def __init__(self, image, width, height):
        self.__width = width
        self.__height = height
        self.__image = image
        self.__panda_sprite = AnimatedSprite(self.__slice_sprite(), 4)

    def get_image(self, time):
        self.__panda_sprite.update(time)
        return self.__panda_sprite.image

    def change_state(self, image):
        self.__image = image
        self.__panda_sprite.change_images(self.__slice_sprite())

    def __slice_sprite(self):
        images = []

        master_width, master_height = self.__image.get_size()
        for i in range(int(master_width/self.__width)):
            image = self.__image.subsurface((i*self.__width, 0,
                                             self.__width, self.__height))
            images.append(image)
        return images
