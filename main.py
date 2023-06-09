import os
import traceback
import types
from pickle import load as pload
from typing import List, Optional, Sequence, Type

import pygame

from mods.basemod import BaseMod
from scenes.abstract import AbstractScene
from scenes.water import WaterScene
from scenes.carscene import CarScene

# from scenes.CMS import CMS
from scenes.constraints import ConstraintScene
from scenes.gravity import GravityScene
from scenes.VoxelWorld import VoxelWorld
from log import create_logger


class Game:
    def __init__(self):
        self.sc = None
        self.res = (1500, 500)
        self.scene: Optional[AbstractScene] = None
        self.mods: List[BaseMod] = []
        self.clock = pygame.time.Clock()
        self.log = create_logger("main", "./log/main.log")
        self.glog = create_logger("game", "./log/game.log")
        self.fps = 60

    def __enter__(self):
        pygame.init()
        pygame.mixer.init()
        self.sc = pygame.display.set_mode(self.res)
        return self

    def __exit__(self, exc_class, exc_message, traceback_obj):
        if exc_message:
            eror = f'error class({exc_class}), message({exc_message}), traceback(\n{traceback_obj.tb_frame.f_locals}\n)'
            self.glog.error(eror)
            self.log.error(eror)
        for mod in self.mods:
            mod.quit(exc_message)
        pygame.quit()
        pygame.mixer.quit()

    def load_scene(self, scene: Type[AbstractScene]):
        self.scene = scene(self.sc, self.fps, self.glog, self.clock)

    def load_mods(self, mods: List[Type[BaseMod]]) -> None:
        for Mod in mods:
            m = Mod(self.sc, self.scene, self.clock, self.glog)
            print(f"mod loading: {m.name} by {m.author}")
            self.mods.append(m)

        for m in self.mods:
            m.mods = self.mods

    def run(self):
        for mod in self.mods:
            mod.start()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.log.debug(f'key down \'{event.unicode}\'')
                if event.type == pygame.KEYUP:
                    self.log.debug(f'key up \'{event.unicode}\'')
                if event.type == pygame.QUIT:
                    if event.type == pygame.KEYDOWN:
                        self.log.debug(f'quit')
                    for mod in self.mods:
                        mod.quit()
                    return
                self.scene.handle_event(event)
                for mod in self.mods:
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


def read_mods(local_dir: str) -> List[Type[BaseMod]]:
    from smods import mods
    return mods


with Game() as g:
    g.load_scene(VoxelWorld)
    g.load_mods(read_mods("smods"))
    g.run()
