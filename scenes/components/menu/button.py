import pygame
from pygame.surface import Surface
from pygame.font import Font, SysFont
from scenes.components.menu.abstract_menu import AbstractMenuElement
from typing import Tuple, Callable


RGB = Tuple[int, int, int]


class Button(AbstractMenuElement):
    def __init__(self, pos: pygame.Vector2, size: pygame.Vector2, text: str, fill: RGB, outline: RGB, callback: Callable):
        self.outline = outline
        self.size = size

        self.font = SysFont("Arial", 20)
        self.rect = pygame.Rect(pos, size)
        self.surface = Surface(size=size)
        self.surface.fill(fill)
        self.text_surface = self.font.render(text, True, self.outline)
        self.callback = callback

    def render(self, display: Surface) -> None:
        text_rect = self.text_surface.get_rect(center=self.size/2)
        self.surface.blit(self.text_surface, text_rect)
        display.blit(self.surface, self.rect)
