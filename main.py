from typing import Optional, Type, Sequence

import pygame
import os

from scenes.abstract import AbstractScene
from scenes.gravity import GravityScene
# from scenes.CMS import CMS
from scenes.constraints import ConstraintScene
from scenes.carscene import CarScene
from scenes.VoxelWorld import VoxelWorld
from pickle import load as pload
from mods.basemod import BaseMod


class Game:
    def __init__(self):
        self.sc = None
        self.res = (1500, 500)
        self.scene: Optional[AbstractScene] = None
        self.mods: Sequence[BaseMod] = []
        self.clock = pygame.time.Clock()
        self.fps = 60

    def __enter__(self):
        pygame.init()
        self.sc = pygame.display.set_mode(self.res)
        return self

    def __exit__(self, exc_class, exc_message, traceback_obj):
        for mod in self.mods :
            mod.quit(exc_message)
        pygame.quit()

    def load_scene(self, scene: Type[AbstractScene]):
        self.scene = scene(self.sc, self.fps, self)

    def load_mods(self, mods: Sequence[Type[BaseMod]]) -> None:

        for Mod in mods:
            m = Mod(self.sc, self.scene, self.clock)
            print(f'mod loading: {m.name} by {m.author}')
            self.mods.append(m)

        for m in self.mods:
            m.mods = self.mods

    def run(self):
        for mod in self.mods :
            mod.start()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for mod in self.mods :
                        mod.quit()
                    return
                self.scene.handle_event(event)
                for mod in self.mods :
                    mod.handle_pressed_keys(pygame.key.get_pressed())
                for mod in self.mods:
                    mod.handle_events(event)
            self.scene.update()
            for mod in self.mods:
                mod.update()
            self.scene.render()
            for mod in self.mods:
                mod.onrender()
            pygame.display.update()
            self.clock.tick(self.fps)


with Game() as g:
    g.load_scene(VoxelWorld)
    modss = []
    for modf in os.listdir(os.getcwd() + "/smods"):
        # if len(modf.split(".")) != 1:
        #     continue
        if modf == "__pycache__":
            continue
        with open(os.getcwd() + "/smods/" + modf) as f:
            exec(f.read())
            modss.append(eval(modf.split(".")[0]))
    g.load_mods(modss)
    g.run()