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

    def mine(self, terrain: Terrain, mouse_pos: pymunk.Vec2d) -> BaseResource:
        space = terrain.space
        distance = self.body.position.get_distance(mouse_pos)
        if distance > 80:
            return
        query = space.point_query(mouse_pos, 0, self.sf)
        if not query:
            return
        tb = query[0]
        if tb:
            br = BaseResource()
            br.materialize(tb.point + pymunk.Vec2d(0, 25), space)
            terrain.delete_block(tb.shape.body)
            return br