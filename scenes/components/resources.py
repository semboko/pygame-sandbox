from pygame.surface import Surface
from pymunk.vec2d import Vec2d
from pymunk import Body, Poly, Space
from scenes.utils import convert
from typing import Optional
from scenes.components.rect import Rect


class BaseResource:
    icon: Surface = Surface((15, 15))
    rect: Optional[Rect]

    def materialize(self, pos: Vec2d, space: Space):
        self.rect = Rect(round(pos.x), round(pos.y), 15, 15, space)
        self.rect.body.apply_force_at_local_point((0, 40000), (0, -7.5))

    def render(self, display: Surface, camera_shift: Vec2d) -> None:
        h = display.get_height()
        pos = self.rect.body.position - camera_shift
        display.blit(self.icon, convert(pos, h))


class Stone(BaseResource):
    pass


class Wood(BaseResource):
    pass


class Ice(BaseResource):
    pass
