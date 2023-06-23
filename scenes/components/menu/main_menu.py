from string import printable
from typing import List, Optional

import pygame
from pygame import Vector2 as V2
from pygame.event import Event
from pygame.surface import Surface

from scenes.components.menu.abstract_menu import AbstractMenu
from scenes.components.menu.button import Button
from scenes.components.menu.text_input import TextInput


class MainMenu(AbstractMenu):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._active_input: Optional[TextInput] = None
        self._commands_buffer: List[str] = []

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
            self._active_input.move_cursor(-1)
        if event.key == pygame.K_LEFT:
            self._active_input.move_cursor(-1)
            return
        if event.key == pygame.K_RIGHT:
            self._active_input.move_cursor(1)
            return
        if event.key == pygame.K_RETURN and self._active_input == self.elements_dict["command_line"]:
            self.enter_command()
            return
        if event.unicode in printable:
            self._active_input.add_text(event.unicode)
            self._active_input.move_cursor(1)

    def next_command(self):
        return None if len(self._commands_buffer) == 0 else self._commands_buffer.pop(0)

    def enter_command(self):
        command_input = self.elements_dict["command_line"]
        command = getattr(command_input, "text", None)
        command_input.text = ""
        command_input.cursor = 0
        if command is not None:
            print("Print from main: " + command)
            self._commands_buffer.append(command)


def create_menu(display: Surface) -> MainMenu:
    menu = MainMenu()
    menu.add_element(Button(V2(0, 0), V2(100, 50), "Exit game", (150, 150, 150), (10, 10, 10), exit))
    menu.add_element(
        TextInput(V2(20, display.get_height() - 70), V2(600, 50), (150, 150, 150), (10, 10, 10)), label="command_line"
    )
    menu.add_element(
        Button(
            V2(630, display.get_height() - 70), V2(100, 50), "Enter", (150, 150, 150), (10, 10, 10), menu.enter_command
        )
    )
    return menu
