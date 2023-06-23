from typing import Tuple, Dict

from pygame import Rect
from pygame.event import Event
from pygame.surface import Surface


class AbstractMenuElement:
    surface: Surface
    rect: Rect
    color: Tuple[int, int, int]

    def __init__(self):
        pass

    def render(self, display: Surface) -> None:
        pass


class AbstractMenu:
    active: bool = False
    elements: Dict[str, AbstractMenuElement] = {}

    def __init__(self):
        self.active = False

        # Buttons, inputs...

    def handle_mouse(self, event: Event):
        pass

    def add_element(self, el: AbstractMenuElement, name: str):
        self.elements[name] = el

    def render(self, display: Surface):
        for element in self.elements.values():
            element.render(display)
