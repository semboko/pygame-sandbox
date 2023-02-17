from abc import ABC
from typing import Tuple

from pygame.event import Event
from pygame.surface import Surface


class AbstractScene(ABC):
    def __init__(self, display: Surface, fps: int) -> None:
        self.display: Surface = display
        self.size_sc: tuple = display.get_size()
        self.fps: int = fps

    def handle_events(self, events: Tuple[Event]) -> None:
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def render(self):
        raise NotImplementedError()
