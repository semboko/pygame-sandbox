from typing import Optional, List

import pygame.font

from scenes.components.menu.abstract_menu import AbstractMenu
from pygame.event import Event
from scenes.components.menu.button import Button
from scenes.components.menu.label import Label
from scenes.components.menu.text_input import TextInput
from pygame import Vector2, Surface
from log import logger

pygame.font.init()


class MainMenu(AbstractMenu):
    def __init__(self):
        super().__init__()
        self._active_input: Optional[TextInput] = None
        self._commands_buffer: List[str] = []

    def handle_keyboard(self, event: Event):
        if not self._active_input:
            return
        element = self._active_input
        if event.key == pygame.K_BACKSPACE:
            logger.info('main menu: BACK')
            if element.cursor >= 0:
                element.text = element.text[:element.cursor] + element.text[element.cursor+1:]
                element.cursor -= 1
        # elif event.key in (pygame.K_ESCAPE, pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_KP_ENTER, pygame.K_RETURN):
        #     pass
        elif event.key in (pygame.K_RIGHT, pygame.K_LEFT):
            element.move_cursor(-1 if event.key == pygame.K_LEFT else 1)
        else:
            logger.info(f'main menu: UNIC({event.unicode})')
            element.cursor += len(event.unicode)
            element.text = element.text[:element.cursor] + event.unicode + element.text[element.cursor:]
        logger.debug(f'main menu: cursor({element.cursor}), text("{element.text}")')


    def handle_mouse(self, event: Event):
        if not self.active:
            return
        for element in self.elements.values():
            # .......................................................................................
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == pygame.BUTTON_LEFT:
                    if isinstance(element, Button):
                        if element.rect.collidepoint(*event.pos):
                            element.mouse_temp = True

                    # .......................................................................................
                    if isinstance(element, TextInput):
                        element.active = element.rect.collidepoint(*event.pos)
                        if element.active:
                            self._active_input = element
                        if not element.active and self._active_input == element:
                            self._active_input = None

            # .......................................................................................
            if event.type == pygame.MOUSEBUTTONUP:

                if event.button == pygame.BUTTON_LEFT:

                    if isinstance(element, Button):
                        if element.rect.collidepoint(*event.pos) and element.mouse_temp:
                            element.mouse_temp = False
                            element.func()
            # .......................................................................................

    def render(self, display: Surface):
        s = pygame.Surface(display.get_size(), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((100, 100, 100, 108))
        display.blit(s, (0, 0))
        super().render(display)

    def enter_command(self):
        command_input = self.elements["Command line"]
        if command_input.text is not None:
            self._commands_buffer.append(command_input.text)
        command_input.text = ""

    def pop_buffer(self) -> Optional[str]:
        return None if len(self._commands_buffer) == 0 else self._commands_buffer.pop(0)


def create_menu(display: Surface) -> MainMenu:
    menu = MainMenu()
    menu.add_element(Button(Vector2(0, 0), Vector2(90, 45), "Exit", (150, 150, 150), (50, 50, 50), quit, 100), "Exit")
    menu.add_element(TextInput(Vector2(20, display.get_height()-70),
                               Vector2(600, 50), (150, 150, 150), 50), "Command line")
    menu.add_element(Button(Vector2(630, display.get_height()-70), Vector2(90, 45), "Enter", (150, 150, 150), (50, 50, 50), menu.enter_command, 100), "Enter")
    return menu
