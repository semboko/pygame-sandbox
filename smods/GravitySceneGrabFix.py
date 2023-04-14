import pygame
import pymunk

from mods.basemod import *
from scenes.gravity import GravityScene
from scenes.components import Ball, Segment, rect
from scenes.utils import *

class GravitySceneGrabFix(BaseMod):

    name = "GavitySceneRepair"
    author = "Kolya142"
    locked = False
    sf = None
    move_obj: Ball = None

    def start(self, *args, **kwargs):
        super(GravitySceneGrabFix, self).start(*args, **kwargs)
        self.scene: GravityScene = self.scene

    def handle_events(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.dict["button"] == 3:
                if self.move_obj is None:
                    for obj in self.scene.renders_objs:
                        if not isinstance(obj, Ball):
                            continue
                        if obj.body.position.get_distance(convert(event.pos, self.scene.size_sc[1])) <= obj.shape.radius:
                            print(2)
                            self.move_obj = obj
                            break
                else:
                    self.move_obj = None
    def update(self):
        #print(self.move_obj)
        if self.move_obj is not None:
            self.move_obj.body.position = convert(pygame.mouse.get_pos(), self.scene.size_sc[1])
