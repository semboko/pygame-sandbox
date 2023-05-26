import pygame
from scenes.components.ball import Ball
from scenes.utils import *

from mods.basemod import *


class Balldeb(BaseMod):
    name = "Ball Debugger"
    author = "Kolya142"
    locked = False

    def start(self, *args, **kwargs):
        if type(self.scene).__name__ != "VoxelWorld":
            self.locked = True

    def handle_events(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.dict["button"] == 3 and not self.locked:
                pos = convert(event.pos, self.scene.size_sc[1])
                print((pos[0] - self.scene.camera_shift.x, pos[1] - self.scene.camera_shift.x))
                self.scene.objects.append(Ball(pos[0] + self.scene.camera_shift.x, pos[1] + self.scene.camera_shift.y, 15, self.scene.space))