import math
import random
from random import randint
from typing import Sequence

import pygame
import pymunk
from noise.perlin import SimplexNoise

from mods.basemod import *
from scenes.abstract import AbstractPymunkScene
from scenes.components import Ball, Segment, rect
from scenes.utils import *


def HUEtoRGB(n: float):
    n = max(n, 0)
    n = min(n, 255)
    if n < 85:
        return int(255 - n), int(n), 0
    if n < 170:
        return int(0), int(255 - n), int(n)
    if n < 255:
        return int(n), 0, int(255 - n)


class rgbline(BaseMod):
    name = "rgbline"
    author = "Kolya142"
    locked = True
    sf = None
    noise: SimplexNoise
    objs: Sequence[Ball] = []

    def start(self, *args, **kwargs):
        super(rgbline, self).start(*args, **kwargs)
        self.scene: AbstractPymunkScene = self.scene
        self.noise = SimplexNoise()
        # self.space.add(PivotJoint(ball1.body, self.space.static_body, (250, 250)))

    def handle_events(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.locked:
            if event.dict["button"] == 2:
                for i in range(0, 200, 40):
                    p1 = Ball(event.pos[0] + i, self.scene.size_sc[1] - event.pos[1], 15, self.scene.space)
                    p2 = Ball(event.pos[0] + i + 20, self.scene.size_sc[1] - event.pos[1], 15, self.scene.space)
                    if i != 0:
                        self.scene.space.add(pymunk.constraints.PinJoint(self.objs[-1].body, p1.body, (0, 0), (0, 0)))
                    self.scene.space.add(pymunk.constraints.PinJoint(p1.body, p2.body, (+10, 0), (-10, 0)))
                    self.objs.extend((p1, p2))
                    self.scene.objects.extend((p1, p2))

    def update(self):
        # print(self.move_obj)
        if self.objs and not self.locked:
            for obj in self.objs:
                t = self.noise.noise2(self.objs.index(obj), 0) * 255
                print(HUEtoRGB(t), t)
                obj.color = HUEtoRGB(t)
