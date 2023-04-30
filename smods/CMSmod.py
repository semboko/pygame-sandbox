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
from scenes.components.pj import PJ
from smods.UserData import *

maps = []
ml = ""
pj = []
mapsc = []
lines = None
codes = ""
blocks = []
player = (250, 250)
finish = (0, 0)

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
        y = 30
        self.buttons = [pygame.rect.Rect((20, y + i * 30, 80, 20)) for i in range(len(self.gm))]
        self.scene: VoxelWorld
        # self.buttons[0].on_click(self.buttons[0].text)
        # self.get_map(self.mapr)
        # self.inits()
        self.pop("main.json")

    def get_maps(self):
        return os.listdir(f'{os.getcwd()}/user_data/CMSmod/')

    def get_map(self, name: str):
        global player, codes, maps, mapsc, lines, blocks, finish, pj, ml
        pj = []
        maps = []
        ml = ""
        mapsc = []
        lines = None
        codes = ""
        blocks = []
        player = (250, 250)
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
                for i in datas["blocks"].split("\n") :
                    j: str = i[:len(i) - 1].split(" ")
                    if j==[""] :
                        continue
                    blocks.append((float(j[0]) / xs,500 - float(j[1]) / ys))
                i = datas["player"]
                player = (float(i[:len(i) - 1].split(" ")[0]),500 - float(i[:len(i) - 1].split(" ")[1]))
                finish = (20, 520)
                if "pj" in datas:
                    for i in datas["pj"].split("\n") :
                        j: str = i[:len(i) - 1].split(" ")
                        if j==[""] :
                            continue
                        pj.append(
                            ((float(j[0]) / xs,500 - float(j[1]) / ys),(float(j[2]) / xs,500 - float(j[3]) / ys)))
                if "mlv" in datas:
                    i = datas["mlv"]
                    finish = (float(i[:len(i) - 1].split(" ")[0]) + 20,500 - float(i[:len(i) - 1].split(" ")[1]) + 20)
                    ml = datas["ml"]
                codes = datas["code"]
                self.terrains = datas["terrain"]

    def inits(self):
        if not self.locked:
            self.scene.player.body.position = player
            self.scene: VoxelWorld
            for i in maps :
                # print(i)
                self.objs.append(Segment(i[0],i[1],10,self.scene.space,pymunk.Body.STATIC))
                self.scene.objects.append(self.objs[-1])
            for i in mapsc:
                # print(i)
                self.objs.append(Ball(i[0], i[1], i[2], self.scene.space))
                self.scene.objects.append(self.objs[-1])
            for i in blocks:
                # print(i)
                self.scene.floor.bricks.append(TerrainBlock(i[0], i[1], self.scene.space, self.scene.floor.sf))
            exec(codes)
            if pj:
                for i in pj:
                    print(i)
                    if not self.scene.space.point_query(i[0], 1, pymunk.ShapeFilter()) or not self.scene.space.point_query(i[1], 1, pymunk.ShapeFilter()):
                        continue
                    obj1 = self.scene.space.point_query(i[0], 1, pymunk.ShapeFilter())[0]
                    obj2 = self.scene.space.point_query(i[1], 1, pymunk.ShapeFilter())[0]
                    if obj1.shape.body == obj2.shape.body:
                        continue
                    spring = pymunk.DampedSpring(obj1.shape.body, obj2.shape.body, (0, 0), (0, 0), obj1.shape.body.position.get_distance(obj2.shape.body.position) / 10, 600, 0.3)
                    self.objs.append(PJ(spring))
                    self.scene.objects.append(self.objs[-1])
                    self.scene.space.add(spring)
            if not self.terrains :
                for i in self.scene.floor.bricks :
                    if i in self.scene.objects :
                        self.scene.objects.remove(i)
                    self.scene.space.remove(i.body, i.shape)
                self.scene.objects.remove(self.scene.floor)
                self.scene.floor = FalseTerrain()
                self.scene.floor.space = self.scene.space

    def pop(self, txt):
        # print(txt)
        self.mapr = txt
        self.scene.objects = []
        self.scene.space = pymunk.Space()
        self.scene.reset_scene()
        self.objs = []
        self.get_map(self.mapr)
        self.inits()

    def update(self):
        if finish != (20, 520) :
            finishs = (finish[0]+30, finish[1]-30)
            if self.scene.player.body.position.get_distance(finishs) < 40:
                self.pop(ml)
        if self.mapr == "main.json":
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
        if finish!=(20, 520) :
            print(finish)
            pygame.draw.rect(self.disp, (100, 255, 0), (finish[0]-self.scene.camera_shift.x, (500-finish[1])+self.scene.camera_shift.y, 60, 60))
        if self.mapr == "main.json":
            for but in range(len(self.gm)):
                #print(but.text)
                font = pygame.font.SysFont("Comic Sans MS", 10)
                text = self.gm[but]
                pygame.draw.rect(self.disp, (250, 180, 100), self.buttons[but])
                self.disp.blit(font.render(text, True, (0,0,0)), self.buttons[but][:2])