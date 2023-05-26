from typing import Dict, Type

from pygame.image import load
from pygame.surface import Surface

from scenes.components.resources import BaseResource, Ice, Stone, Wood


class BaseBiome:
    image: Surface = Surface((25, 25))
    resources: Dict[Type[BaseResource], int] = {}
    name: str = "type"


class Flatland(BaseBiome):
    image: Surface = load("./assets/grass.jpg")
    resources: Dict[Type[BaseResource], int] = {Stone: 2, Wood: 4}
    name: str = "Flatland"


class Swamp(BaseBiome):
    image: Surface = load("./assets/swamp.jpg")
    resources: Dict[Type[BaseResource], int] = {Stone: 1, Wood: 1}
    name: str = "Swamp"


class Mine(BaseBiome):
    pass


class Mountain(BaseBiome):
    image: Surface = load("./assets/snow.jpg")
    resources: Dict[Type[BaseResource], int] = {Stone: 1, Ice: 5}
    name: str = "Mountain"
