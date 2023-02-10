from typing import Tuple

import pymunk
from pygame.event import Event
from pygame.surface import Surface

from scenes.abstract import AbstractScene


class GravityScene(AbstractScene):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.circle = pymunk.Body()
        self.circle.position = (self.size_sc[0]//2, self.size_sc[1]//2)
        self.circle_shape = pymunk.Circle(self.circle, 10)
        self.space.add(circle, circle_shape)

    def handle_events(self, events: Tuple[Event]) -> None:
        pass

    def update(self, step):
        super(GravityScene, self).update(step)

    def render(self):
        pass
