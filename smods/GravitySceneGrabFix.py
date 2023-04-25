import pygame
import pymunk

from mods.basemod import *
from scenes.gravity import GravityScene
from scenes.components import Ball, Segment
from scenes.components.cmake import Cmake
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
        # if type(self.scene).__name__ != "GravityScene":
        #     self.locked = True

    def handle_events(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.locked:
            print(1)
            if event.dict["button"] == 3:
                print(2)
                if self.move_obj is None:
                    print(3)
                    for obj in self.scene.renders_objs:
                        print(4)
                        if not isinstance(obj, Ball) and not isinstance(obj, Cmake):
                            continue
                        print(type(obj))
                        print(5)
                        if isinstance(obj, Cmake):
                            print(6)
                            if obj.rct.body.position.get_distance(convert(event.pos, self.scene.size_sc[1])) <= 160:
                                self.move_obj = obj
                                break
                        else:
                            if obj.body.position.get_distance(convert(event.pos, self.scene.size_sc[1])) <= obj.shape.radius:
                                self.move_obj = obj
                                break
                else:
                    self.move_obj = None
    def update(self):
        #print(self.move_obj)
        if self.move_obj is not None and not self.locked:
            if isinstance(self.move_obj, Cmake):
                self.move_obj.rct.body.position = convert(pygame.mouse.get_pos(),self.scene.size_sc[1])
            else:
                self.move_obj.body.position = convert(pygame.mouse.get_pos(), self.scene.size_sc[1])