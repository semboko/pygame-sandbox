import pygame
from pygame import Rect, Surface, Vector2
from pygame.font import SysFont, get_default_font
from scenes.components.menu.abstract_menu import AbstractMenuElement
from typing import Tuple, Callable


RGB = Tuple[int, int, int]


class Button(AbstractMenuElement):
    def __init__(self, pos: Vector2, size: Vector2, text: str, fill: RGB, outline: RGB, func: Callable, detail: int = 20):
        self.rect = Rect(pos, size)
        self.fill = fill
        self.text = text
        self.pos = pos
        self.mouse_temp = False
        self.size = size
        self.func = func
        self.outline = outline
        text_ = SysFont(get_default_font(), detail).render(self.text, True, self.outline)
        text_ = pygame.transform.scale(text_, self.size//2)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.fill)
        self.surface.blit(text_, self.size//4)

    def render(self, display: Surface):
        display.blit(self.surface, self.pos)
