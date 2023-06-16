import pygame
from pygame import Rect, Surface, Vector2
from pygame.font import SysFont, get_default_font
from scenes.components.menu.abstract_menu import AbstractMenuElement
from typing import Tuple, Callable

RGB = Tuple[int, int, int]


class TextInput(AbstractMenuElement):
    def __init__(self, pos: Vector2, size: Vector2, fill: RGB, detail: int = 5):
        self.rect = Rect(pos, size)
        self.fill = fill
        self.text = ""
        self.detail = detail
        self.pos = pos
        self.size = size
        self.active = False
        self._frames = 0
        self.cursor = -1
        self.font = SysFont("Arial", self.detail)

        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.fill)
        self.surface_copy = self.surface.copy()

    def blit_text(self):
        if self.active:
            self.surface.fill((50, 50, 200))
            self.surface.blit(pygame.transform.scale(self.surface_copy, (self.rect.width-6, self.rect.height-6)), (3, 3))
        else:
            self.surface = self.surface_copy.copy()
        text_ = self.font.render(self.text, True, (50, 50, 50))
        self.surface.blit(text_, (0, -self.rect.height/4))

    def move_cursor(self, dx: int):
        if dx not in (-1, 1):
            raise Exception("x muse be -1 or 1")
        if self.cursor + dx < 0 or self.cursor + dx > len(self.text):
            return
        self.cursor += dx

    def render(self, display: Surface):
        self.blit_text()
        if self.active and self._frames < 50:
            text_ = self.font.render(self.text[:self.cursor+1], True, (50, 50, 50))
            line_x = text_.get_width()
            pygame.draw.line(self.surface, (10, 10, 10), (line_x, 0), (line_x, self.rect.height))
        self._frames = (self._frames + 1) % 100

        display.blit(self.surface, self.pos)