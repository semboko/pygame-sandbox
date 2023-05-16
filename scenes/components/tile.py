import pygame
import pymunk

class Tile:
    def __init__(self, img: pygame.Surface, speed: int, y: int):
        self.img = img
        self.i = 0
        self.y = y
        self.speed = speed
    def render(self, display: pygame.Surface):
        if self.img.get_width() != display.get_width():
            self.img = pygame.transform.scale(self.img, display.get_size())
            self.i = display.get_width()
        self.i -= self.speed
        if self.i + self.img.get_width() >= display.get_width() * 2:
            self.i = 0
        if self.i <= 0:
            self.i = display.get_width()
        i = self.i - self.img.get_width()
        display.blit(self.img, (i, self.y))
        display.blit(self.img,(self.i,self.y))