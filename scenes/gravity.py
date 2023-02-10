from typing import Tuple

import pymunk
from pygame.event import Event
from pygame.surface import Surface

from scenes.abstract import AbstractScene


class GravityScene(AbstractScene):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.space = pymunk.Space()
        
        self.circle = pymunk.Body()
        self.circle_shape = pymunk.Circle(self.circle, 10)

    def handle_events(self, events: Tuple[Event]) -> None:
        pass

    def update(self):
        self.space.step()

    def render(self):
        pass
