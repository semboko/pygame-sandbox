from typing import Tuple

import pygame
import pymunk
from pygame.surface import Surface

from scenes.utils import convert


class Rect:
    def __init__(
        self, x: int, y: int, width: int, height: int, space: pymunk.Space, color: Tuple[int, int, int] = (255, 0, 0), debug: bool = False
    ) -> None:
        self.color = color
        self.debug = debug
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

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        h = display.get_height()
        verts = [convert(self.body.local_to_world(v) - camera_shift, h) for v in self.shape.get_vertices()]
        pygame.draw.polygon(display, self.color, verts)
        if self.debug:
            pygame.draw.circle(
                display, (0, 0, 0),
                convert(self.body.local_to_world(self.body.center_of_gravity) - camera_shift, h),
                5,
                1
            )
