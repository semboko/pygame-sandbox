import pymunk
from scenes.components.rect import Rect
from scenes.components.terrain import Terrain
from pygame import Vector2
from typing import Tuple
from scenes.components.resources import *


class Player(Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = 1
        self.dp = []
        self.sf = pymunk.ShapeFilter(group = 0b0001, categories = 0b0110)
        self.shape.filter = self.sf

    def move(self, direction: int):
        self.body.apply_impulse_at_local_point((direction * 20_000, 0), (0, 0))
        self.direction = direction

    def jump(self):
        self.body.apply_impulse_at_local_point((0, 700000), (0, 0))

    def mine(self, terrain: Terrain, mouse_pos: pymunk.Vec2d) -> Optional[Tuple[BaseResource]]:
        space = terrain.space
        distance = self.body.position.get_distance(mouse_pos)
        if distance > 150:
            return
        query = space.point_query(mouse_pos, 0, self.sf)
        if not query:
            return
        brick = terrain.get_brick_by_body(query[0].shape.body)
        if not brick:
            return
        resources = brick.get_resources()
        for r in resources:
            r.materialize(mouse_pos, space)
        terrain.delete_block(brick)
        return resources

    def consume_resource(self, res: BaseResource) -> None:
        pass
