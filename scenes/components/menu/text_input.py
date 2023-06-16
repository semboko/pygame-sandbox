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

        self.font = SysFont("Mono", 20)
        self.rect = pygame.Rect(pos, size)
        self.surface = Surface(size=size)
        self.surface.fill(fill)
        self.frames = 0

        self.text = ""
        self.cursor = 0
        self.active = False

    def move_cursor(self, dx: int) -> None:
        if dx not in (-1, 1):
            raise Exception("dx must be -1 or 1")
        if self.cursor <= 0 and dx == -1:
            return
        if self.cursor >= len(self.text) and dx == 1:
            return
        self.cursor += dx

    def add_text(self, txt: str):
        self.text = self.text[:self.cursor] + txt + self.text[self.cursor:]

    def render(self, display: Surface) -> None:
        # text_rect = self.text_surface.get_rect(center=self.size / 2)
        # self.surface.blit(self.text_surface, text_rect)
        self.surface.fill(self.fill)
        if self.active:
            pygame.draw.rect(self.surface, self.outline, Rect((0, 0), self.rect.size), 1)

        text_img = self.font.render(self.text, True, (0, 0, 0))
        self.surface.blit(text_img, (0, self.rect.height/2 - text_img.get_height()/2))

        self.frames += 1
        self.frames %= 30
        if self.active and self.frames < 10:
            letter_width = 12
            cursor_start = pygame.Vector2(letter_width * self.cursor, 10)
            cursor_end = pygame.Vector2(cursor_start.x, self.rect.height - 10)
            pygame.draw.line(self.surface, (0, 0, 0), cursor_start, cursor_end, 3)
            print(self.cursor)
        display.blit(self.surface, self.rect)
