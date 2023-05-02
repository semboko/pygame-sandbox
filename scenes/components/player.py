import time
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
from enum import Enum


class PlayerState(Enum):
    IDLE = "idle"
    RUN = "run"
    FALL = "fall"
    MINE = "mine"


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
        self.add_sprite(PlayerState.IDLE.value, "./assets/player.png")
        self.add_sprite(PlayerState.RUN.value, "./assets/player_run.png")
        self.add_sprite(PlayerState.FALL.value, "./assets/player_fall.png")
        self.add_sprite(PlayerState.MINE.value, "./assets/player_mine.png")
        for img in self.imgs:
            self.imgs[img] = pygame.transform.scale(self.imgs[img], (self.wigth, self.height))

        self.state = PlayerState.IDLE
        self.animation_time = 0
        self.moves = 1

    def move(self, direction: int):
        if direction != self.moves:
            for img in self.imgs:
                self.imgs[img] = pygame.transform.flip(self.imgs[img], True, False)

        self.state = PlayerState.RUN if self.state == PlayerState.IDLE else PlayerState.IDLE
        self.animation_time = 2

        self.moves = direction
        self.body.apply_impulse_at_local_point((direction * 20_000, 0), (0, 0))
        self.direction = direction

    def update(self, space: pymunk.Space):
        self.animation_time -= 1
        if self.animation_time <= 0:
            self.state = PlayerState.IDLE

        if self.body.velocity.y < -1:
            self.state = PlayerState.FALL

        self.active_sprite = self.state.value

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        # super(Player, self).render(display, camera_shift)
        self.render_sprite(self.body.position - (25, 25) - camera_shift, display)

    def jump(self, space: pymunk.Space):
        if space.segment_query(self.body.position, (self.body.position.x, self.body.position.y - 100), 0, self.sf):
            self.body.apply_impulse_at_local_point((0, 700000), (0, 0))

    def mine(self, terrain: Terrain, mouse_pos: pymunk.Vec2d) -> Optional[Tuple[BaseResource]]:
        self.state = PlayerState.MINE
        self.animation_time = 20
        space = terrain.space
        distance = self.body.position.get_distance(mouse_pos)
        if distance > 150:
            return
        if self.moves > 0:
            if self.body.position.x > mouse_pos.x:
                return
        else:
            if self.body.position.x < mouse_pos.x:
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
