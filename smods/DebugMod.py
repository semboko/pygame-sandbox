import pygame

from mods.basemod import *


class DebugMod(BaseMod):
    name = "DebugMod"
    author = "Kolya142"
    scenet = ""

    def start(self, *args, **kwargs):
        super(DebugMod, self).start(*args, **kwargs)
        print("OnSetup")
        self.scenet = type(self.scene).__name__
        print(self.scenet)

    #     def update(self) :
    #         print("OnUpdate")

    #     def onrender(self) :
    #         print("OnRender")

    #     def handle_pressed_keys(self, keys: Sequence[bool]):
    #         print(keys[pygame.K_a], keys[pygame.K_SPACE], keys[pygame.K_d])

    #     def handle_events(self,event: Event) :
    #         print(f'event: {event}')

    def quit(self, error: str = None):
        print(f"quit \n{error}")
