from typing import Tuple

import pygame
from pygame import mixer
import pymunk
from pygame import Vector2

from scenes.components.invertory import Invertory
from scenes.components.rect import Rect
from scenes.components.resources import *
from scenes.components.terrain import Terrain
from scenes.components.sprite import Sprite


class Player(Rect, Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = 1
        self.dp = []
        self.sf = pymunk.ShapeFilter(group=0b0001, categories=0b0110)
        self.shape.filter = self.sf
        self.inv = Invertory()
        self.mine_sound = mixer.Sound("./assets/sounds/noise_01.ogg")
        self.mine_sound.set_volume(0.1)
        self.add_sprite("idle", "./assets/player.png")
        self.add_sprite("run","./assets/player_run.png")
        self.add_sprite("fall","./assets/player_fall.png")
        for img in self.imgs:
            self.imgs[img] = pygame.transform.scale(self.imgs[img], (self.wigth, self.height))
        self.is_run = False
        self.is_fall = False
        self.is_run_frame = False
        self.moves = 1

    def move(self, direction: int):
        if direction != self.moves:
            for img in self.imgs:
                self.imgs[img] = pygame.transform.flip(self.imgs[img], True, False)
        # self.is_run = True
        self.is_run_frame = not self.is_run_frame
        self.moves = direction
        self.body.apply_impulse_at_local_point((direction * 20_000, 0), (0, 0))
        self.direction = direction

    def update(self, space: pymunk.Space):
        if self.is_run and self.is_run_frame and not self.is_fall and abs(self.body.velocity.x) > 20:
            # print(abs(self.body.velocity.x))
            self.active_sprite = "run"
        elif self.is_fall:
            self.active_sprite = "fall"
        else:
            self.active_sprite = "idle"
        if not space.segment_query(self.body.position, (self.body.position.x, self.body.position.y - 170), 0, self.sf):
            self.is_run = False
            self.is_fall = True
        else:
            self.is_fall = False

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        # super(Player, self).render(display, camera_shift)
        self.render_sprite(self.body.position - (25, 25) - camera_shift, display)

    def jump(self, space: pymunk.Space):
        if space.segment_query(self.body.position, (self.body.position.x, self.body.position.y - 100), 0, self.sf):
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
        self.mine_sound.play()
        resources = brick.get_resources()
        for r in resources:
            r.materialize(mouse_pos, space)
        terrain.delete_block(brick)
        return resources

    def consume_resource(self, res: BaseResource) -> None:
        self.inv.pickup(res)
