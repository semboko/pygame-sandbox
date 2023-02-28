from pygame.surface import Surface
import pymunk
import pygame
from scenes.utils import convert
from scenes.components.pj import PJ
from scenes.components.rect import Rect
from scenes.components.ball import Ball


class Car:
    def __init__(self, x: int, y: int, width: int, height: int, space: pymunk.Space) -> None:
        self.car_body = Rect(x, y, width, height, space)
        self.add_rear_suspension(x, y, width, height, space)

    def add_rear_suspension(self, x, y, width, height, space: pymunk.Space):
        self.rear_sleeve = Ball(x - 5 * width / 6, y - height, 5, space)
        self.rear_joint = pymunk.PinJoint(self.car_body.body, self.rear_sleeve.body, (-width//2, -height//2), (0, 0))

    def render(self, display: Surface) -> None:
        self.car_body.render(display)
        PJ(self.rear_joint).render(display)
