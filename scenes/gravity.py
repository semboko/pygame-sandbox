from typing import Tuple

import pygame.draw
import pymunk
from pygame.event import Event
from pygame.surface import Surface

from scenes.abstract import AbstractScene

from .utils import convert


class Ball:
    def __init__(self, x: int, y: int, r: int, space: pymunk.Space, btype: int = pymunk.Body.DYNAMIC):
        self.body = pymunk.Body(body_type=btype)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, r)
        self.shape.density = 1
        self.r = r
        self.debug = space.debug_draw
        space.add(self.body, self.shape)

    def render(self, display: Surface) -> None:
        h = display.get_height()
        pygame.draw.circle(display, (244, 0, 0), convert(self.body.position, h), self.r)
        if self.debug:
            print(f"circle by id {id(self)}: angle = {self.body.angle}, pos = {tuple(self.body.position)}")


class Segment:
    def __init__(
        self, a: Tuple[int, int], b: Tuple[int, int], r: int, space: pymunk.Space, btype: int = pymunk.Body.DYNAMIC
    ):
        self.body = pymunk.Body(body_type=btype)
        self.shape = pymunk.Segment(self.body, a, b, r)
        self.r = r
        space.add(self.body, self.shape)

    def render(self, display: Surface) -> None:
        h = display.get_height()
        pygame.draw.line(display, (0, 0, 0), convert(self.shape.a, h), convert(self.shape.b, h), self.r)


class GravityScene(AbstractScene):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.space: pymunk.Space() = pymunk.Space()
        self.space.gravity = 0, -1000
        self.space.debug_draw = True
        self.space.damping = 0.5  # Set the friction coefficient of the space object
        self.circle = Ball(250, 400, 10, self.space)
        self.pause = False

        self.segment = Segment((0, 100), (500, 50), 5, self.space, btype=pymunk.Body.KINEMATIC)

    def handle_events(self, events: Tuple[Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause = True
                elif event.key == pygame.K_r:
                    self.reset_scene()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.pause = False

    def reset_scene(self):
        # Reset the objects in the scene to their initial positions
        self.__init__(self.display, self.fps)

    def update(self):
        if not self.pause:
            self.space.step(1 / self.fps)

    def render(self):
        self.display.fill((255, 255, 255))
        self.circle.render(self.display)
        self.segment.render(self.display)
