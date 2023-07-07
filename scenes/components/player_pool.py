import time

import pygame
import pymunk

from connection.manager import ConnectionManager
from scenes.components.player import Player, PlayerMessage
from typing import Dict
from uuid import UUID


class PlayerPool:
    def __init__(self, connection_manager: ConnectionManager, space: pymunk.Space) -> None:
        self.connection_manager = connection_manager
        self.pool: Dict[UUID, Player] = {}
        self.last_update: Dict[UUID, float] = {}
        self.space = space

    def update(self):
        # message = self.connection_manager.receive_chat_message()
        pass

    def add_player(self, message: PlayerMessage) -> None:
        player = Player.build_from_message(message, self.space)
        self.pool[player.id] = player
        self.last_update[player.id] = time.time()
        print(f"Player {player} is added")

    def update_player(self, message: PlayerMessage):
        player = self.pool[message.player_id]
        player.body.position = message.player_pos
        player.direction = message.player_direction
        player.state = message.player_state
        self.last_update[player.id] = time.time()
        print(f"Player {player} is updated")

    def cleanup(self):
        current_time = time.time()
        for player in list(self.pool.values()):
            if self.last_update[player.id] + 10 < current_time:
                del self.pool[player.id]
                del self.last_update[player.id]

    def render(self, display: pygame.Surface, camera_shift: pymunk.Vec2d) -> None:
        for player in self.pool.values():
            player.render(display, camera_shift)
