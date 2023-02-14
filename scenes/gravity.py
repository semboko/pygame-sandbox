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
        self.circle.position = (self.size_sc[0]//2, self.size_sc[1]//2)
        self.circle_shape = pymunk.Circle(self.circle, 10)
        self.space.add(self.circle, self.circle_shape)
    def handle_events(self, events: Tuple[Event]) -> None:
        pass

    def update(self, step):
        self.space.step(step)
    def render(self):
        self.display.fill((255, 255, 255))
        for i in range(len(self.space.bodies)):
            shape_type = self.space.shapes[i].__class__.__name__
            print(self.space.shapes[i].__sizeof__())
