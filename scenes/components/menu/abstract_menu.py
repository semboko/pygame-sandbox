from typing import List, Tuple

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
    elements: List[AbstractMenuElement] = []

    def __init__(self):
        self.active = False

        # Buttons, inputs...

    def handle_mouse(self, event: Event):
        pass

    def add_element(self, el: AbstractMenuElement):
        self.elements.append(el)

    def render(self, display: Surface):
        for element in self.elements:
          element.render(display)
