import pygame
from typing import Tuple


class Sprite:
    imgs = {}
    active_sprite = ""

    def add_sprite(self, name, img):
        self.imgs[name] = pygame.image.load(img)
        self.active_sprite = ""

    def render_sprite(self, pos: Tuple[int, int], disp: pygame.Surface):
        if self.active_sprite:
            disp.blit(self.imgs[self.active_sprite],pos)