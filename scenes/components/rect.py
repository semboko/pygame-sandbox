from pygame.surface import Surface
import pymunk
import pygame
from scenes.utils import convert


class Rect:
    def __init__(self, x: int, y: int, width: int, height: int, space: pymunk.Space) -> None:
        self.body = pymunk.Body()
        self.body.position = x, y
        verts = (
            (-width//2, -height//2),
            (width//2, -height//2),
            (width//2, height//2),
            (-width//2, height//2)
        )
        self.shape = pymunk.Poly(self.body, verts)
        self.shape.density = 1
        space.add(self.body, self.shape)

    def render(self, display: Surface) -> None:
        h = display.get_height()
        verts = [
            convert(self.body.local_to_world(v), h)
            for v in self.shape.get_vertices()
        ]
        pygame.draw.polygon(display, (255, 0, 0), verts)