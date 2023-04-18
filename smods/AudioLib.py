from mods.basemod import *
from pygame import mixer
try:
    from smods.UserData import UserData
except ImportError:
    print("install \"UserDataMenager\" mod")
    exit(1)
import os

mixer.init()

class AudioLib(BaseMod):

    name = "AudioLoadLib"
    author = "Kolya142"

    def start(self, *args, **kwargs):
        pass

    @staticmethod
    def play(dirpath: str, name: str, volume: float) -> None:
        dirs = f'{os.getcwd()}/user_data/{dirpath}/{name}'
        if name not in UserData.get_files(dirpath):
            return
        mixer.music.load(dirs)
        mixer.music.set_volume(volume)
        mixer.music.play()