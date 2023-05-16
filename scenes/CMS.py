from logging import getLogger
from typing import Tuple

import pygame.draw
import pymunk
from pygame.event import Event

from scenes.abstract import AbstractPymunkScene
from scenes.components import Ball, Segment

from .utils import convert

pygame.init()
pygame.font.init()
map_file = "map.txt"
maps = []
with open(map_file) as f:
    lines = f.read().split("\n")
    for i in lines:
        i: str = i.replace("[", "").replace("]", ",").replace(" ", "").replace(".", "").replace(",00", "0")
        i = i[: len(i) - 1]
        i = i.split(",")
        if i[0] == "":
            break
        xs = 4
        ys = 70
        maps.append(((int(i[0]) / xs, 500 - int(i[1]) / ys), (int(i[2]) / xs, 500 - int(i[3]) / ys)))


class CMS(AbstractPymunkScene):
    def reset_scene(self):
        super().reset_scene()
        for i in maps:
            self.objects.append(Segment(i[0], i[1], 10, self.space, pymunk.Body.STATIC))
        self.menu_state = 0

    def update(self):
        self.space.step(1 / self.fps)
        # self.clean_up()

    def clean_up(self):
        for i in self.objects:
            if not isinstance(i, Segment):
                if i.pos[0] < 0 or i.pos[0] > self.size_sc[0] or i.pos[1] < 0 or i.pos[1] > self.size_sc[1]:
                    del i

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_scene()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.dict["button"] == 1:
                self.objects.append(Ball(*convert(event.pos, self.size_sc[1]), 15, self.space))
