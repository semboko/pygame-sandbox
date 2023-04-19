from pygame.surface import Surface
from pygame.image import load
from scenes.components.resources import BaseResource, Stone, Snow, Grass


class BaseBiome:
    image: Surface = Surface((25, 25))
    resource: BaseResource = BaseResource()


class Flatland(BaseBiome):
    image: Surface = load("./assets/grass.jpg")
    resource: Grass = Grass


class Swamp(BaseBiome):
    image: Surface = load("./assets/swamp.jpg")
    resource: Stone = Stone


class Mine(BaseBiome):
    pass


class Mountain(BaseBiome):
    image: Surface = load("./assets/snow.jpg")
    resource: Snow = Snow
