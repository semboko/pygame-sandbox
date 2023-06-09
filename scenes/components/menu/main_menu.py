from scenes.components.menu.abstract_menu import AbstractMenu
from pygame.event import Event
from scenes.components.menu.button import Button
from pygame import Vector2 as V2
from pygame.surface import Surface


class MainMenu(AbstractMenu):
    def handle_mouse(self, event: Event):
        for element in self.elements:
            if element.rect.collidepoint(event.pos):
                if isinstance(element, Button):
                    element.callback()


def create_menu(display: Surface) -> MainMenu:
    menu = MainMenu()
    menu.add_element(Button(V2(0, 0), V2(100, 50), "Exit game", (150, 150, 150), (10, 10, 10), lambda: exit()))
    return menu
