from typing import Optional

from pygame.surface import Surface
from pygame.image import load
from pygame.transform import rotate
from pymunk import Body, Poly, Space
from pymunk.vec2d import Vec2d
from math import degrees

from scenes.components.rect import Rect
from scenes.utils import convert


class BaseResource:
    icon: Surface = Surface((16, 16))
    rect: Optional[Rect]

    def materialize(self, pos: Vec2d, space: Space):
        w, h = self.icon.get_size()
        self.rect = Rect(round(pos.x), round(pos.y), w, h, space)
        self.rect.body.apply_force_at_local_point((0, 40000), (0, -7.5))

    def render(self, display: Surface, camera_shift: Vec2d) -> None:
        h = display.get_height()
        pos = self.rect.body.position - camera_shift
        icon = rotate(self.icon, degrees(self.rect.body.angle))
        display.blit(icon, convert(pos, h))


class Stone(BaseResource):
    icon = load("./assets/StoneIcon.png", "png")


class Wood(BaseResource):
    icon = load("./assets/WoodIcon.png")


class Ice(BaseResource):
    icon = load("./assets/IceIcon.png")
