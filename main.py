from typing import Optional, Type

import pygame

from scenes.abstract import AbstractScene
from scenes.gravity import GravityScene


class Game:
    def __init__(self):
        self.sc = None
        self.res = (500, 500)
        self.scene: Optional[AbstractScene] = None
        self.clock = pygame.time.Clock()
        self.fps = 60

    def __enter__(self):
        pygame.init()
        self.sc = pygame.display.set_mode(self.res)
        return self

    def __exit__(self, exc_class, exc_message, traceback_obj):
        pygame.quit()

    def load_scene(self, scene: Type[AbstractScene]):
        self.scene = scene(self.sc, self.fps)

    def run(self):
        while True:
            for event in pygame.event.get() :
                if event.type==pygame.QUIT :
                    return
                self.scene.handle_events((event,))
            self.scene.update()
            self.scene.render()
            pygame.display.update()
            self.clock.tick(self.fps)


with Game() as g:
    g.load_scene(GravityScene)
    g.run()
