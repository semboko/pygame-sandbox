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
        display.blit(self.surface, self.rect)
        for i in range(len(self.history)):
            print(self.history[i])
