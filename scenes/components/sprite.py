import pygame
from typing import Tuple


class Sprite:
    imgs = {}
    active_sprite = ""
    sprite_angle = 0

    def add_sprite(self, name, img):
        self.imgs[name] = pygame.image.load(img)
        self.active_sprite = ""

    def rotate_sprite(self, angle):
        if self.active_sprite and abs(angle) > 10:
            self.imgs[self.active_sprite] = pygame.transform.rotate(self.imgs[self.active_sprite], self.sprite_angle - angle)
            self.sprite_angle = angle

    def render_sprite(self, pos: Tuple[int, int], disp: pygame.Surface):
        if self.active_sprite:
            disp.blit(self.imgs[self.active_sprite], pos)