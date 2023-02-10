from abc import ABC
from typing import Tuple

from pygame.event import Event
from pygame.surface import Surface


class AbstractScene(ABC):
    def __init__(self, display: Surface) -> None:
        self.display = display

    def handle_events(self, events: Tuple[Event]) -> None:
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def render(self):
        raise NotImplementedError()
