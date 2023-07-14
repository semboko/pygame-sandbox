import time
import uuid
from enum import Enum
from typing import Tuple

import pygame
import pymunk
from pygame import Vector2, mixer

from scenes.components.invertory import Invertory
from scenes.components.rect import Rect
from scenes.components.resources import *
from scenes.components.sprite import Sprite
from scenes.components.terrain import Terrain
from dataclasses import dataclass
from uuid import UUID


class PlayerState(Enum):
    IDLE = "idle"
    RUN = "run"
    FALL = "fall"
    MINE = "mine"


@dataclass
class PlayerMessage:
    player_id: UUID
    player_pos: pymunk.Vec2d
    player_direction: int
    player_state: PlayerState
    player_username: str


class Player(Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = 1
        self.dp = []
        self.sf = pymunk.ShapeFilter(group=0b0001, categories=0b0110)
        self.shape.filter = self.sf
        self.inv = Invertory()
        self.mine_sound = mixer.Sound("./assets/sounds/noise_01.ogg")
        self.mine_sound.set_volume(0.1)
        self.sprite = Sprite()
        self.sprite.add_sprite(PlayerState.IDLE.value, "./assets/player.png")
        self.sprite.add_sprite(PlayerState.RUN.value, "./assets/player_run.png")
        self.sprite.add_sprite(PlayerState.FALL.value, "./assets/player_fall.png")
        self.sprite.add_sprite(PlayerState.MINE.value, "./assets/player_mine.png")
        for img in self.sprite.imgs:
            self.sprite.imgs[img] = pygame.transform.scale(self.sprite.imgs[img], (self.wigth, self.height))

        self.state = PlayerState.IDLE
        self.animation_time = 0
        self.moves = 1
        self.id = kwargs.get("id_") or uuid.uuid4()
        self.username: str = kwargs.get("username", "Anonimus")

        self.font = pygame.font.SysFont("Arial", 14)

    def move(self, direction: int):
        if direction != self.moves:
            for img in self.sprite.imgs:
                self.sprite.imgs[img] = pygame.transform.flip(self.sprite.imgs[img], True, False)

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

        self.sprite.active_sprite = self.state.value

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        # super(Player, self).render(display, camera_shift)
        self.sprite.render_sprite(self.body.position - (25, 25) - camera_shift, display)
        username_img = self.font.render(self.username, True, (0, 0, 0))
        dest_point = convert(self.body.position + (-30, 50) - camera_shift, display.get_height())
        display.blit(username_img, dest_point)

    def jump(self, space: pymunk.Space):
        if space.segment_query(self.body.position, (self.body.position.x, self.body.position.y - 100), 0, self.sf):
            self.body.apply_impulse_at_local_point((0, 700000), (0, 0))

    def mine(self, terrain: Terrain, mouse_pos: pymunk.Vec2d) -> Optional[Tuple[BaseResource]]:
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
        self.state = PlayerState.MINE
        self.mine_sound.play()
        resources = brick.get_resources()
        for r in resources:
            r.materialize(mouse_pos, space)
        terrain.delete_block(brick)
        return resources

    def consume_resource(self, res: BaseResource) -> None:
        self.inv.pickup(res)

    def get_message(self) -> PlayerMessage:
        return PlayerMessage(
            player_id=self.id,
            player_pos=self.body.position,
            player_direction=self.direction,
            player_state=self.state,
            player_username=self.username
        )

    @classmethod
    def build_from_message(cls, message: PlayerMessage, space: Space) -> 'Player':
        return Player(
            id_=message.player_id,
            x=message.player_pos.x,
            y=message.player_pos.y,
            width=50,
            height=50,
            space=space,
            username=message.player_username
        )
