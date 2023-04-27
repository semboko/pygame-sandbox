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

class CMSmod(BaseMod):

    name = "CMSmod"
    author = "Kolya142"
    locked = False
    objs = []
    buttons = []
    updates = []
    mapr = ""

    def start(self, *args, **kwargs):
        super(CMSmod, self).start(*args, **kwargs)
        if type(self.scene).__name__ != "VoxelWorld":
            self.locked = True
        self.gm = self.get_maps()
        y = 250 - len(self.gm) / 2
        self.buttons = [pygame.rect.Rect((20, y + i * 30, 80, 20)) for i in range(len(self.gm))]
        # self.buttons[0].on_click(self.buttons[0].text)
        # self.get_map(self.mapr)
        # self.inits()

    def get_maps(self):
        return os.listdir(f'{os.getcwd()}/user_data/CMSmod/')

    def get_map(self, name: str):
        global player, codes, maps, mapsc, lines
        if len(UserData.get_files("CMSmod")) >= 1 :
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
            defs = f'{os.getcwd()}/user_data/CMSmod/{name}'
            with open(defs) as f :
                datas = json.load(f)
                for i in datas["lines"].split("\n") :
                    j: str = i[:len(i) - 1].split(" ")
                    if j==[""] :
                        continue
                    maps.append(((float(j[0]) / xs,500 - float(j[1]) / ys),(float(j[2]) / xs,500 - float(j[3]) / ys)))
                for i in datas["circles"].split("\n") :
                    j: str = i[:len(i) - 1].split(" ")
                    if j==[""] :
                        continue
                    mapsc.append((float(j[0]) / xs,500 - float(j[1]) / ys,float(j[2])))
                i = datas["player"]
                player = (float(i[:len(i) - 1].split(" ")[0]),500 - float(i[:len(i) - 1].split(" ")[1]))
                codes = datas["code"]

    def inits(self):
        if not self.locked:
            self.scene.player.body.position = player
            self.scene: VoxelWorld
            for i in maps :
                print(i)
                self.objs.append(Segment(i[0],i[1],10,self.scene.space,pymunk.Body.STATIC))
                self.scene.objects.append(self.objs[-1])
            for i in mapsc:
                print(i)
                self.objs.append(Ball(i[0], i[1], i[2], self.scene.space))
                self.scene.objects.append(self.objs[-1])
            exec(codes)

    def pop(self, txt):
        print(txt)
        self.mapr = txt
        self.get_map(self.mapr)
        self.inits()

    def update(self):
        if self.mapr == "":
            for i in self.buttons:
                if i.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        self.pop(self.gm[self.buttons.index(i)])
                        break
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
                        with open(f'{os.getcwd()}/user_data/{"CMSmod"}/{self.mapr}') as mf:
                            dt = json.load(mf)
                        dt["code"] = f.read()
                        with open(f'{os.getcwd()}/user_data/{"CMSmod"}/{self.mapr}', 'w') as mf:
                            json.dump(dt, mf)
                exit()

            if event.key == pygame.K_r:
                self.inits()

    def onrender(self):
        if self.mapr == "":
            for but in range(len(self.gm)):
                #print(but.text)
                font = pygame.font.SysFont("Comic Sans MS", 10)
                text = self.gm[but]
                pygame.draw.rect(self.disp, (250, 180, 100), self.buttons[but])
                self.disp.blit(font.render(text, True, (0,0,0)), self.buttons[but][:2])