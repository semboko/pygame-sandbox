import pygame
from pygame import Rect, Surface, Vector2
from pygame.font import SysFont, get_default_font
from scenes.components.menu.abstract_menu import AbstractMenuElement
from typing import Tuple


RGB = Tuple[int, int, int]


class Label(AbstractMenuElement):
    def __init__(self, pos: Vector2, size: Vector2, text: str, fill: RGB, detail: int = 20):
        self.rect = Rect(pos, size)
        self.fill = fill
        self.text = text
        self.size = size
        self.pos = pos
        text_ = SysFont(get_default_font(), detail).render(self.text, True, self.fill)
        text_ = pygame.transform.scale(text_, self.size//2)
        self.surface = text_

    def render(self, display: Surface):
        display.blit(self.surface, self.pos)
