from pygame.surface import Surface
from pygame.image import load


class BaseBiome:
    image: Surface = Surface((25, 25))


class Flatland(BaseBiome):
    image: Surface = load("./assets/grass.jpg")


class Swamp(BaseBiome):
    pass


class Mine(BaseBiome):
    pass


class Mountain(BaseBiome):
    pass
