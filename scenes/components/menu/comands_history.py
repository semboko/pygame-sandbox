from scenes.components.menu.abstract_menu import AbstractMenuElement
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.math import Vector2
from scenes.components.menu.text_input import TextInput
import pygame
from typing import List


class CommandsHistory(AbstractMenuElement):
    def __init__(self, command_input: TextInput, height: int, history: List[str]):
        super().__init__()
        self.rect = Rect(command_input.rect.topleft - Vector2(0, height), Vector2(command_input.rect.width, height))
        self.surface = Surface(self.rect.size, pygame.SRCALPHA)
        self.surface.fill((100, 100, 100, 108))
        self.history = history

        self.font = pygame.font.SysFont("Arial", 16)

    def render(self, display: Surface) -> None:
        y = self.surface.get_height()
        for entry in reversed(self.history):
            command_img = self.font.render(entry, True, (0, 0, 0))
            self.surface.blit(command_img, (20, y - command_img.get_height()))
            y -= command_img.get_height()

        display.blit(self.surface, self.rect)
