from pygame.surface import Surface
from typing import List, Tuple, Optional, Dict
from pygame.event import Event
from pygame.rect import Rect
from pygame.font import Font

RGB = Tuple[int, int, int]


class AbstractMenuElement:
    surface: Surface
    rect: Rect
    color: Tuple[int, int, int]
    font: Font

    def __init__(self):
        pass

    def render(self, display: Surface) -> None:
        pass


class AbstractMenu:
    elements: List[AbstractMenuElement]

    def __init__(self):
        self.active = False
        self.elements = []
        self.elements_dict: Dict[str, AbstractMenuElement] = {}

    def handle_mouse(self, event: Event):
        pass

    def handle_keyboard(self, event: Event):
        pass

    def add_element(self, el: AbstractMenuElement, label: Optional[str] = None) -> None:
        self.elements.append(el)
        if label is not None:
            self.elements_dict[label] = el

    def render(self, display: Surface):
        for element in self.elements:
            element.render(display)
