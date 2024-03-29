from typing import Dict, Type

import pygame
from pygame.surface import Surface

from scenes.components.resources import BaseResource


class Invertory:
    icons: Dict[Type[BaseResource], int] = {}
    previewsize: int = 64

    def __init__(self):
        pass

    def pickup(self, obj: BaseResource) -> None:
        if type(obj) not in self.icons:
            self.icons[type(obj)] = 0
        self.icons[type(obj)] += 1

    def drop(self, obj: BaseResource) -> None:
        pass

    def render(self, display: Surface):
        h = display.get_height()
        w = display.get_width()
        y = h - self.previewsize * 0.5
        x = w // 2 - (len(self.icons) * self.previewsize / 2) - self.previewsize / 2
        for it, count in self.icons.items():
            display.blit(it.icon, pygame.Vector2(x, y))

            df = pygame.font.get_default_font()
            font = pygame.font.SysFont(df, 15, False)
            text = font.render(f"{count}", True, (0, 0, 0))
            display.blit(text, (x, y - 10))

            x += self.previewsize
