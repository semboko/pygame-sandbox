from typing import Optional, Type

import pygame

from scenes.abstract import AbstractScene


class Game:
    def __init__(self):
        self.sc = None
        self.res = (500, 500)
        self.scene: Optional[AbstractScene] = None

    def __enter__(self):
        pygame.init()
        self.sc = pygame.display.set_mode(self.res)

    def __exit__(self, exc_class, exc_message, traceback_obj):
        pygame.quit()

    def render(self):
        self.sc.fill((255, 255, 255))

    def load_scene(self, scene: Type[AbstractScene]):
        self.scene = scene(self.sc)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.scene.handle_events(tuple(pygame.event.get()))
            self.scene.update()
            self.scene.render()
            pygame.display.update()


with Game() as g:
    g.load_scene(...)
    g.run()
