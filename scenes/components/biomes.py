from pygame.surface import Surface
from pygame.image import load
from typing import Dict, Type
from scenes.components.resources import BaseResource, Stone, Wood, Ice


class BaseBiome:
    image: Surface = Surface((25, 25))
    resources: Dict[Type[BaseResource], int] = {}


class Flatland(BaseBiome):
    image: Surface = load("./assets/grass.jpg")
    resources: Dict[Type[BaseResource], int] = {Stone: 2, Wood: 4}


class Swamp(BaseBiome):
    image: Surface = load("./assets/swamp.jpg")
    resources: Dict[Type[BaseResource], int] = {Stone: 1, Wood: 1}


class Mine(BaseBiome):
    pass


class Mountain(BaseBiome):
    image: Surface = load("./assets/snow.jpg")
    resources: Dict[Type[BaseResource], int] = {Stone: 1, Wood: 1, Ice: 5}
