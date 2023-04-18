from mods.basemod import *
from smods.UserData import *
from typing import Tuple
import os
import math

import pygame.draw
import pymunk
from pygame.event import Event

from scenes.abstract import AbstractPymunkScene
from scenes.components import Ball, Segment

lines = None
maps = []
player = (250, 250)
mapsc = []
if len(UserData.get_files("CMSmod")) == 3:
    defs = f'{os.getcwd()}/user_data/{"CMSmod"}/'
    map_file = defs+"map.txt"
    map_file_circles = defs+"map_circles.txt"
    with open(map_file_circles) as f:
        circles = f.read().split("\n")
        for i in circles:
            if i == "":
                break
            i: str
            i = i[:len(i)-1]
            i = i.split()
            print(i)
            xs = 640/1500

            ys = 1
            mapsc.append(((
                             int(float(i[0]))/xs,
                             500-int(float(i[1]))/ys,
                             float(i[2]))
                         ))
    with open(map_file) as f:
        lines = f.read().split("\n")
        for i in lines:
            if i == "":
                break
            i: str = i.replace(".0", "")
            print(i)
            i = i.split()
            if i[0] == '':
                break
            xs = 640/1500
            ys = 320/500
            if len(i) == 2:
                break
            maps.append(((
                             int(i[0])/xs,
                             500-int(i[1])/ys
                         ),(
                             int(i[2])/xs,
                             500-int(i[3])/ys
                         )))
    with open(defs+"map_player.txt") as f:
        i = f.read().replace(".0", "")
        i = i.split("/n")[0].split()
        xs = 640/1500
        ys = 320/500
        print(i)
        if i:
            player = ((
                         int(i[0])/xs,
                         500-int(i[1])/ys
                     ))

class CMSmod(BaseMod):

    name = "CMSmod"
    author = "Kolya142"
    locked = False
    objs = []

    def start(self, *args, **kwargs):
        super(CMSmod, self).start(*args, **kwargs)
        if not maps:
            self.locked = True
        self.scene.player.body.position = player

        if not self.locked:
            for i in maps :
                print(i)
                self.objs.append(Segment(i[0],i[1],10,self.scene.space,pymunk.Body.STATIC))
            for i in mapsc:
                print(i)
                self.objs.append(Ball(i[0], i[1], i[2], self.scene.space))

    def handle_events(self, event: Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.scene.player.body.position = player
                self.objs = []
                if not self.locked :
                    for i in maps :
                        print(i)
                        self.objs.append(Segment(i[0],i[1],10,self.scene.space,pymunk.Body.STATIC))
                    for i in mapsc :
                        print(i)
                        self.objs.append(Ball(i[0], i[1], i[2], self.scene.space))

    def onrender(self):
        for obj in self.objs:
            if isinstance(obj, Segment):
                obj: Segment
                obj.render(self.scene.display, pymunk.Vec2d(+self.scene.camera_shift.x, -self.scene.camera_shift.y))
            else:
                obj: Ball
                print(obj.body.position.y)
                if not math.isnan(obj.body.position.y):
                    obj.render(self.scene.display,pymunk.Vec2d(+self.scene.camera_shift.x, +self.scene.camera_shift.y))