from typing import Tuple

import pymunk
from pygame.event import Event
from pygame.surface import Surface
import pygame.draw
from scenes.abstract import AbstractScene


class GravityScene(AbstractScene):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.space: pymunk.Space() = pymunk.Space()
        self.circle = pymunk.Body()
        self.circle.position = self.size_sc[0]//2, self.size_sc[1]//2
        self.circle_shape = pymunk.Circle(self.circle, 10)
        self.circle_shape.density = 1
        self.space.add(self.circle, self.circle_shape)

    def handle_events(self, events: Tuple[Event]) -> None:
        pass

    def update(self):
        self.space.step(1/self.fps)

    def render(self):
        self.display.fill((255, 255, 255))
        x, y = self.circle.position
        pygame.draw.circle(self.display, (255, 0, 0), (int(x), int(y)), 10)
