import pygame
import pymunk
from math import ceil


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


class Background:
    def __init__(self, display_width: int) -> None:
        self.images = [
            pygame.image.load(f"./assets/bgs/bg-{i}.png")
            for i in range(3)
        ]
        self.image_width = self.images[0].get_width()
        self.n = ceil(display_width/self.image_width) + 1

    def render(self, display: pygame.Surface, shift: pygame.Vector2) -> None:
        for image_idx, image in enumerate(self.images):
            layer_shift = (shift.x * (image_idx + 1) * 0.3) % self.image_width
            for i in range(self.n + image_idx):
                display.blit(image, (i * self.image_width - layer_shift, 0))
