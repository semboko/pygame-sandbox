import pygame

from string import printable
from scenes.components.menu.abstract_menu import AbstractMenu
from pygame.event import Event
from scenes.components.menu.button import Button
from scenes.components.menu.text_input import TextInput
from pygame import Vector2 as V2
from typing import Optional, List
from pygame.surface import Surface


class MainMenu(AbstractMenu):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._active_input: Optional[TextInput] = None

    def handle_mouse(self, event: Event):
        self._active_input = None
        for element in self.elements:
            if isinstance(element, Button) and element.rect.collidepoint(event.pos):
                element.callback()
            if isinstance(element, TextInput):
                if element.rect.collidepoint(event.pos):
                    element.active = True
                    self._active_input = element
                else:
                    element.active = False

    def handle_keyboard(self, event: Event):
        if not self._active_input:
            return
        if event.key == pygame.K_BACKSPACE:
            self._active_input.text = self._active_input.text[:-1]
            return
        if event.unicode in printable:
            self._active_input.text += event.unicode


def create_menu(display: Surface) -> MainMenu:
    menu = MainMenu()
    menu.add_element(Button(V2(0, 0), V2(100, 50), "Exit game", (150, 150, 150), (10, 10, 10), exit))
    menu.add_element(TextInput(V2(0, 60), V2(200, 50), (150, 150, 150), (10, 10, 10)))
    menu.add_element(TextInput(V2(0, 110), V2(200, 50), (150, 150, 150), (10, 10, 10)))
    return menu
