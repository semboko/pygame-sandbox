from mods.basemod import *
from typing import Union
import os

class UserData(BaseMod):

    name = "UserDataMenager"
    author = "Kolya142"

    def start(self, *args, **kwargs):
        super(UserData, self).start(*args, **kwargs)

    @staticmethod
    def get_files(name: str) -> tuple:
        dirs = f'{os.getcwd()}/user_data/{name}'
        if not os.path.exists(dirs):
            os.mkdir(dirs)
        return os.listdir(dirs)

    @staticmethod
    def set_file(dirpath: str, file: str, data: Union[str, bytes]) -> None:
        dirs = f'{os.getcwd()}/user_data/{dirpath}/{file}'

        if isinstance(data, str):
            with open(dirs, 'w') as f:
                f.write(data)
        elif isinstance(data, bytes):
            with open(dirs, 'wb') as f:
                f.write(data)

    @staticmethod
    def get_file(dirpath: str, file: str, isbytesdata: bool = False) -> Union[str, bytes]:
        dirs = f'{os.getcwd()}/user_data/{dirpath}/{file}'

        if not isbytesdata:
            with open(dirs, 'r') as f:
                return f.read()
        else:
            with open(dirs, 'rb') as f:
                return f.read()
