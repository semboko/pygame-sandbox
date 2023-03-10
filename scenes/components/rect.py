from typing import Tuple, Optional

import pygame
import pymunk
from pymunk.vec2d import Vec2d
from pygame.surface import Surface

from scenes.utils import convert


class Rect:
    def __init__(
        self, x: int, y: int, width: int, height: int, space: pymunk.Space, color: Tuple[int, int, int] = (255, 0, 0)
    ) -> None:
        self.color = color
        self.body = pymunk.Body()
        self.body.position = x, y
        verts = (
            (-width // 2, -height // 2),
            (width // 2, -height // 2),
            (width // 2, height // 2),
            (-width // 2, height // 2),
        )
        self.shape = pymunk.Poly(self.body, verts)
        self.shape.density = 1
        space.add(self.body, self.shape)

    def render(self, display: Surface, pymunk_shift: Optional[Vec2d] = Vec2d(0, 0)) -> None:
        h = display.get_height()
        verts = []
        for v in self.shape.get_vertices():
            world_v = self.body.local_to_world(v)
            shifted_v = world_v - pymunk_shift
            verts.append(convert(shifted_v, h))

        pygame.draw.polygon(display, self.color, verts)
