import pygame
import pymunk

from mods.basemod import *
from scenes.gravity import GravityScene
from scenes.components import Ball, Segment
from scenes.components import Ball, Segment, rect
from scenes.gravity import GravityScene
from scenes.utils import *


class GravitySceneGrabFix(BaseMod):
    name = "GavitySceneGrabFix"
    author = "Kolya142"
    locked = False
    sf = None
    move_obj: Ball = None

    def start(self, *args, **kwargs):
        super(GravitySceneGrabFix, self).start(*args, **kwargs)
        self.scene: GravityScene = self.scene
        if type(self.scene).__name__ != "GravityScene" and type(self.scene).__name__ != "WaterScene":
            self.locked = True

    def handle_events(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.locked:
            #print(1)
            if event.dict["button"] == 3:
                #print(2)
                if self.move_obj is None:
                    #print(3)
                    for obj in self.scene.renders_objs:
                        #print(4)
                        if isinstance(obj,Ball) :
                            if obj.body.position.get_distance(convert(event.pos, self.scene.size_sc[1])) <= obj.shape.radius:
                                self.move_obj = obj
                                break
                else:
                    self.move_obj = None

    def update(self):
        # print(self.move_obj)
        if self.move_obj is not None and not self.locked:
            self.move_obj.body.position = convert(pygame.mouse.get_pos(), self.scene.size_sc[1])
