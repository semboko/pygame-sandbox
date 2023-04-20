from mods.basemod import *
from smods.UserData import *
from scenes.VoxelWorld import *
from typing import Tuple
import os
import math
import os
from typing import Tuple

import json
import pygame.draw
import pymunk
from pygame.event import Event
from scenes.components.resources import *
import json
from scenes.components.terrain import *

from mods.basemod import *
from scenes.abstract import AbstractPymunkScene
from scenes.components import Ball, Segment
from smods.UserData import *

lines = None
maps = []
player = (250, 250)
codes = ""
mapsc = []
if len(UserData.get_files("CMSmod")) == 1:
    # if i=="" :
    #     break
    # i: str
    # i = i[:len(i) - 1]
    # i = i.split()
    # print(i)
    # xs = 640 / 1500
    #
    # ys = 1
    # mapsc.append(((
    #     int(float(i[0])) / xs,
    #     500 - int(float(i[1])) / ys,
    #     float(i[2]))
    # ))
    xs = 1
    ys = 1
    defs = f'{os.getcwd()}/user_data/{"CMSmod"}/map.json'
    with open(defs) as f:
        datas = json.load(f)
        for i in datas["lines"].split("\n"):
            j: str = i[:len(i) - 1].split(" ")
            if j == [""]:
                continue
            maps.append(((float(j[0]) / xs, 500 - float(j[1]) / ys ), ( float(j[2]) / xs, 500 - float(j[3]) / ys)))
        for i in datas["circles"].split("\n") :
            j: str = i[:len(i) - 1].split(" ")
            if j == [""]:
                continue
            mapsc.append((float(j[0]) / xs,500 - float(j[1]) / ys,float(j[2])))
        i = datas["player"]
        player = (float(i[:len(i) - 1].split(" ")[0]), 500 - float(i[:len(i) - 1].split(" ")[1]))
        codes = datas["code"]

class CMSmod(BaseMod):

    name = "CMSmod"
    author = "Kolya142"
    locked = False
    objs = []
    updates = []

    def start(self, *args, **kwargs):
        super(CMSmod, self).start(*args, **kwargs)
        if not maps or type(self.scene).__name__ != "VoxelWorld":
            self.locked = True

        if not self.locked:
            self.scene.player.body.position = player
            self.scene: VoxelWorld
            for i in maps :
                print(i)
                self.objs.append(Segment(i[0],i[1],10,self.scene.space,pymunk.Body.STATIC))
            for i in mapsc:
                print(i)
                self.objs.append(Ball(i[0], i[1], i[2], self.scene.space))
            exec(codes)

    def update(self):
        for i in self.updates:
            i(self)

    def handle_events(self, event: Event):
        if event.type == pygame.KEYDOWN and not self.locked:
            if event.key == pygame.K_p:
                pygame.quit()
                print("Choice option:\n\t(0: exit,1: code to map)")
                options = input(":")
                if options=="1" :
                    file = input("file: ")
                    with open(file) as f:
                        with open(f'{os.getcwd()}/user_data/{"CMSmod"}/map.json') as mf:
                            dt = json.load(mf)
                        dt["code"] = f.read()
                        with open(f'{os.getcwd()}/user_data/{"CMSmod"}/map.json', 'w') as mf:
                            json.dump(dt, mf)
                exit()

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
                    exec(codes)

    def onrender(self):
        if not self.locked:
            for obj in self.objs:
                if isinstance(obj, Segment):
                    obj: Segment
                    obj.render(self.scene.display, pymunk.Vec2d(+self.scene.camera_shift.x, -self.scene.camera_shift.y))
                else:
                    obj: Ball
                    #print(obj.body.position.y)
                    if not math.isnan(obj.body.position.y):
                        obj.render(self.scene.display,pymunk.Vec2d(+self.scene.camera_shift.x, +self.scene.camera_shift.y))
