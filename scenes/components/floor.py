import pygame.draw
from pymunk import Vec2d, Space, Body
from pygame.surface import Surface
from typing import List
from scenes.components.segment import Segment
from random import randint
from scenes.utils import convert


class RandomFloor:

    segments: List[Segment]

    def __init__(self, start_x: int, end_x: int, min_y: int, max_y: int, pieces: int, space: Space):
        self.space = space
        self.min_y, self.max_y = min_y, max_y
        self.segments = []

        self.segment_x_projection = (end_x - start_x) / pieces

        for p in range(pieces - 1):
            p_start_x = self.segment_x_projection * p
            p_start_y = randint(min_y, max_y) if not self.segments else self.segments[-1].shape.b[1]
            p_end_x = self.segment_x_projection * (p + 1)
            p_end_y = randint(min_y, max_y)
            seg = self.create_segment(Vec2d(p_start_x, p_start_y), Vec2d(p_end_x, p_end_y))
            self.segments.append(seg)

    def create_segment(self, a: Vec2d, b: Vec2d) -> Segment:
        seg = Segment(a, b, 5, self.space, btype=Body.STATIC)
        seg.shape.friction = 1
        return seg

    def update_segments(self, pymunk_shift: Vec2d):
        left_x = self.segments[0].shape.a[0]
        right_x = self.segments[-1].shape.b[0]
        shift_x = pymunk_shift[0]
        if shift_x + 50 < left_x:
            b = self.segments[0].shape.a
            a = Vec2d(b.x - self.segment_x_projection, randint(self.min_y, self.max_y))
            self.segments.insert(0, self.create_segment(a, b))
            self.space.remove(self.segments[-1].body, self.segments[-1].shape)
            del(self.segments[-1])
        if shift_x > right_x - 1000:
            a = self.segments[-1].shape.b
            b = Vec2d(a.x + self.segment_x_projection, randint(self.min_y, self.max_y))
            self.segments.append(self.create_segment(a, b))
            self.space.remove(self.segments[0].body, self.segments[0].shape)
            del(self.segments[0])

    def render(self, display: Surface, pymunk_shift: Vec2d = Vec2d(0, 0)):
        h = display.get_height()
        for seg in self.segments:
            a = seg.shape.a - pymunk_shift
            b = seg.shape.b - pymunk_shift
            pygame.draw.line(display, (0, 0, 0), convert(a, h), convert(b, h))
