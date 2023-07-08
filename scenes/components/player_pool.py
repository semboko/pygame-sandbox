import time
from dataclasses import dataclass
from typing import Dict
from uuid import UUID

import pygame
import pymunk

from scenes.components.player import Player, PlayerMessage
from scenes.utils import convert
from servconnction.menage import ConnectionManager


class PlayerPool:

    def __init__(self, connection_manager: ConnectionManager, space: pymunk.Space):
        self.connection_manager = connection_manager
        self.pool: Dict[UUID, Player] = {}
        self.last_update: Dict[UUID, float] = {}
        self.space = space

    def update(self):
        message = self.connection_manager.receive_player_message

    def add_player(self, message: PlayerMessage):
        player = Player.build_from_message(message, self.space)
        print(f'added player {message}')
        self.pool[message.player_id] = player
        self.last_update[message.player_id] = time.time()

    def cleanup(self):
        t = time.time()
        for player in list(self.pool.values()):
            if t - self.last_update[player.id] > 10:
                del self.pool[player.id]
                del self.last_update[player.id]

    def render(self, display: pygame.Surface, camera_shift: pymunk.Vec2d):
        for player in self.pool:
            self.pool[player].render(display, camera_shift)
            pos = convert(self.pool[player].body.position - camera_shift,
                          display.get_height())
            pygame.draw.rect(display, (0, 0, 251), (*pos - pymunk.Vec2d(25, 25), *(50, 50)))

    def update_player(self, message: PlayerMessage):
        player = self.pool[message.player_id]
        player.body.position = message.player_pos
        player.direction = message.player_direction
        self.last_update[player.id] = time.time()
