import pygame


try:
    from smods.UserData import UserData
except ImportError:
    print("install \"UserDataMenager\" mod")
    exit(1)

from mods.basemod import *
from datetime import datetime

class DebugMod(BaseMod):

    name = "DebugMod"
    author = "Kolya142"
    logs: list = []

    def start(self, *args, **kwargs):
        super(DebugMod, self).start(*args, **kwargs)
        print("OnSetup")
        UserData.get_files("DebugMod")

    def update(self):
        if len(self.logs) >= 700:
            self.logs = []
        self.logs.append(f'{datetime.now():%Y-%m-%d %H:%M:%S%z}: update()')

    def onrender(self):
        self.logs.append(f'{datetime.now():%Y-%m-%d %H:%M:%S%z}: render()')

    def handle_pressed_keys(self, keys: Sequence[bool]):
        self.logs.append(f'{datetime.now():%Y-%m-%d %H:%M:%S%z}: pressed({", ".join(map(str, keys))})')

    def handle_events(self,event: Event):
        self.logs.append(f'{datetime.now():%Y-%m-%d %H:%M:%S%z}: event({event})')

    def quit(self, error: str = None):
        if error:
            UserData.set_file("DebugMod", "log.txt", "\n".join(self.logs + ["error: " + str(error)]))
        print(f'quit \n{error}')