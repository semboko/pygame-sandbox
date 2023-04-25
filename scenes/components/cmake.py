from typing import Tuple

import pygame
import pymunk
from pygame.surface import Surface
from scenes.components.rect import Rect
from scenes.utils import convert


class Cmake:
    def __init__(self,x: int,y: int,space: pymunk.Space) -> None:
        self.img = pygame.image.load("cmake.png")
        self.rct = Rect(x, y, 160, 160, space)

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        img = pygame.transform.rotate(self.img, self.rct.body.angle)
        #self.rct.render(display, camera_shift)
        h = display.get_height()
        x, y = self.rct.body.position + (-100, 100)
        display.blit(img, (x, h-y))
