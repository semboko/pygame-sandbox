from abc import ABC
from typing import Tuple

import pymunk
from pygame.event import Event
from pygame.surface import Surface


class AbstractScene(ABC):
    def __init__(self, display: Surface) -> None:
        self.display: Surface = display
        self.size_sc: tuple = display.get_size()
        self.space: pymunk.Space() = pymunk.Space()
    def handle_events(self, events: Tuple[Event]) -> None:
        raise NotImplementedError()

    def update(self, step: int):
        self.space.step(step)

    def render(self):
        raise NotImplementedError()
