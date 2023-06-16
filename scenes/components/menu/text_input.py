import pygame

from scenes.components.menu.abstract_menu import AbstractMenuElement, RGB
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.math import Vector2
from pygame.font import SysFont


class TextInput(AbstractMenuElement):
    def __init__(self, pos: Vector2, size: Vector2, fill: RGB, outline: RGB):
        self.outline = outline
        self.size = size
        self.fill = fill

        self.font = SysFont("Arial", 20)
        self.rect = pygame.Rect(pos, size)
        self.surface = Surface(size=size)
        self.surface.fill(fill)

        self.text = ""

        self.active = False

    def render(self, display: Surface) -> None:
        # text_rect = self.text_surface.get_rect(center=self.size / 2)
        # self.surface.blit(self.text_surface, text_rect)
        self.surface.fill(self.fill)
        if self.active:
            pygame.draw.rect(self.surface, self.outline, Rect((0, 0), self.rect.size), 1)

        text_img = self.font.render(self.text, True, (0, 0, 0))
        self.surface.blit(text_img, (0, 0))
        display.blit(self.surface, self.rect)
