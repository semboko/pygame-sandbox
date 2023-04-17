from math import cos, sin

import pygame
import pymunk
from pygame.surface import Surface

from scenes.utils import convert


class Ball:
    def __init__(self, x: int, y: int, r: int, space: pymunk.Space, btype: int = pymunk.Body.DYNAMIC):
        self.body = pymunk.Body(body_type=btype)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, r)
        self.shape.density = 0.1
        self.shape.elasticity = 0.9
        self.shape.friction = 0.7
        self.color = (255, 0, 0)
        self.r = r
        space.add(self.body, self.shape)

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        h = display.get_height()
        pygame.draw.circle(display, self.color, convert(self.body.position - camera_shift, h), self.r)
        alpha = self.body.angle
        line_end = cos(alpha) * self.r, sin(alpha) * self.r
        pygame.draw.line(
            display,
            (0, 0, 0),
            convert(self.body.position - camera_shift, h),
            convert(self.body.local_to_world(line_end) - camera_shift, h),
            1,
        )
