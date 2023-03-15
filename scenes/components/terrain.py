from random import randint
from typing import Tuple

import pymunk

from scenes.components.segment import Segment
from pymunk import Space, Body
from pygame.surface import Surface


class Terrain:
    def __init__(self, x_min: int, x_max: int, y_min: int, y_max: int, steps: int, space: Space):
        self.space = space
        self.segments = []
        self.x_max, self.x_min, self.y_max, self.y_min = x_max, x_min, y_max, y_min

        self.seg_width = (x_max - x_min)//steps
        for x in range(x_min, x_max, self.seg_width):
            p1 = self.segments[-1].shape.b if self.segments else (x, randint(y_min, y_max))
            p2 = (p1[0] + self.seg_width, randint(y_min, y_max))
            self.segments.append(self.create_segment(p1, p2))

    def create_segment(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> Segment:
        s = Segment(p1, p2, 1, self.space, btype=Body.STATIC)
        s.shape.friction = 0.95
        return s

    def update(self, x_shift: float) -> None:
        left_x = self.segments[0].shape.a[0]
        right_x = self.segments[-1].shape.b[0]
        shift_x = x_shift
        if shift_x + 50 < left_x:
            b = self.segments[0].shape.a
            a = pymunk.Vec2d(b.x - self.seg_width, randint(self.y_min, self.y_max))
            self.segments.insert(0, self.create_segment(a, b))
            self.space.remove(self.segments[-1].body, self.segments[-1].shape)
            del (self.segments[-1])
        if shift_x > right_x - 1000:
            a = self.segments[-1].shape.b
            b = pymunk.Vec2d(a.x + self.seg_width, randint(self.y_min, self.y_max))
            self.segments.append(self.create_segment(a, b))
            self.space.remove(self.segments[0].body, self.segments[0].shape)
            del (self.segments[0])

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        for s in self.segments:
            s.render(display, camera_shift)
