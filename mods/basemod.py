from typing import Sequence

from pygame.event import Event
from pygame.surface import Surface
from pygame.time import Clock

from scenes.abstract import AbstractScene


class BaseMod:
    name: str = "Mod"
    author: str = "Author"

    def __init__(self, display: Sequence, scene: AbstractScene, clock: Clock):
        self.disp = display
        self.scene = scene
        self.clock = clock
        self.mods = []

    def get_mod(self, name):
        for i in self.mods:
            if i.name == name:
                return i

    def handle_command(self, command: str):
        pass

    def start(self):
        pass

    def update(self):
        pass

    def onrender(self):
        pass

    def handle_events(self, event: Event):
        pass

    def handle_pressed_keys(self, keys: Sequence[bool]):
        pass

    def quit(self, error: str = None):
        pass
