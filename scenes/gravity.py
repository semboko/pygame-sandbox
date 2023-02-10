from typing import Tuple

from pygame.event import Event
from pygame.surface import Surface

from scenes.abstract import AbstractScene


class GravityScene(AbstractScene):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def handle_events(self, events: Tuple[Event]) -> None:
        pass

    def update(self):
        pass

    def render(self):
        pass
