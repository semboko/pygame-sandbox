import pygame
import pymunk

from scenes.utils import convert
from mods.basemod import *


class Tas(BaseMod):
    name = "Tas"
    author = "Kolya142"
    Poses = []
    names = []
    on = False

    def start(self, *args, **kwargs):
        super(Tas, self).start(*args, **kwargs)

    def update(self):
        self.get_mod("SaveVideo").active = (not self.scene.menu.active)
        if self.on:
            if not pygame.key.get_pressed()[pygame.K_KP4] and not self.scene.menu.active:
                self.names.append(self.get_mod("SaveVideo").nam)
                self.Poses.append(convert(self.scene.player.body.position, self.scene.size_sc[1]))
            if pygame.key.get_pressed()[pygame.K_KP6] :
                self.on = False
                self.names = []
                self.Poses = []
            if pygame.key.get_pressed()[pygame.K_KP5] :
                self.clock.tick(25)
            if pygame.key.get_pressed()[pygame.K_KP4] :
                self.clock.tick(46)
                if self.get_mod("SaveVideo").nam != 0 and len(self.names) != 0:
                    pr = self.names.pop()
                    self.get_mod("SaveVideo").nam = self.names[-1]
                    self.get_mod("SaveVideo").remover(pr)
                if len(self.Poses) != 0:
                    self.scene.player.body.position = convert(self.Poses.pop(), self.scene.size_sc[1])
        if pygame.key.get_pressed()[pygame.K_KP3] :
            self.on = True

    def onrender(self):

        camera_shift = self.scene.camera_shift
        camera_shift = pymunk.Vec2d(-camera_shift.x, camera_shift.y)
        for i in self.Poses:
            pygame.draw.circle(self.disp, (0, 255, 0), (i[0], i[1])+camera_shift, 3)