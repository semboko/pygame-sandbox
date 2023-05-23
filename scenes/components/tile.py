from math import ceil

import pygame


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
        display.blit(self.img, (self.i, self.y))


class Background:
    def __init__(self, display_width: int) -> None:
        self.images = [pygame.image.load(f"./assets/bgs/bg-{i}.png") for i in range(3)]
        self.image_width = self.images[0].get_width()
        n = ceil(display_width / self.image_width) + 1
        self.n = n

        for image_idx, image in enumerate(self.images):
            n = self.n + image_idx + 1
            imga = pygame.surface.Surface((image.get_width() * n, image.get_height()), pygame.SRCALPHA)
            for i in range(n):
                imga.blit(image, (i * image.get_width(), 0))
            self.images[image_idx] = imga

    def render(self, display: pygame.Surface, shift: pygame.Vector2) -> None:
        width = self.image_width/self.n
        for image_idx, image in enumerate(self.images):
            layer_shift = (shift.x * (image_idx + 1) * 0.3) % self.image_width
            print(f"draw image by index {image_idx+1}, file tile.py")
            display.blit(image, (width - layer_shift - width, 0))
