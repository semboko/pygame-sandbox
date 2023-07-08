import pickle
import random
import time
from typing import List

import pygame
import pymunk
from pygame.event import Event
from re import fullmatch as rematch

from scenes.components.resources import BaseResource
from scenes.abstract import AbstractPymunkScene
from scenes.components.player import Player
from scenes.components.resources import *
from scenes.components.terrain import Terrain, TerrainBlock
from scenes.components.biomes import BaseBiome, Flatland, Mountain, Swamp
from scenes.components.sprite import Sprite
from scenes.components.tile import Background
from scenes.utils import convert
from log import logger
from scenes.components.menu.main_menu import create_menu
from clparser import Parser, Token
from servconnction.menage import ConnectionManager
from scenes.components.player_pool import PlayerPool

pygame.init()
pygame.font.init()


class VoxelWorld(AbstractPymunkScene):
    def reset_scene(self):
        super().reset_scene()
        self.player = Player(250, 250, 50, 60, self.space, (25, 25, 25), True)
        self.floor = Terrain(0, self.display.get_width() + 200, 10, 200, 400, self.space)
        self.objects.extend((self.player, self.floor))
        self.bg = Background(self.display.get_width())
        self.menu = create_menu(self.display)
        self._commands_buffer: List[str] = []
        self._pars = Parser()
        self.connection_menager = ConnectionManager("localhost", 6379)
        self.remote_players = PlayerPool(self.connection_menager, self.space)

    def update(self):
        if not self.menu.active:
            super().update()
        self.player.body.angle = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.move(-1)
            self.player.is_run = True
        elif keys[pygame.K_d]:
            self.player.move(1)
            self.player.is_run = True
        elif keys[pygame.K_LCTRL] and keys[pygame.K_s]:
            print("saving...")
            self.save()
        elif keys[pygame.K_LCTRL] and keys[pygame.K_l]:
            print("loading...")
            self.load("save.g2")
        else:
            self.player.is_run = False
        self.player.update(self.space)
        command = self.menu.pop_buffer()
        if command:
            print("command: " + command)
            self._commands_buffer.append(command)
            self.handle_command()

        self.camera_shift = pymunk.Vec2d(self.player.body.position.x - 250, self.player.body.position.y - 250)
        self.floor.update(self.camera_shift.x)
        self.connection_menager.send_player_message(self.player)
        self.remote_players.cleanup()
        # print(self.remote_players.last_update, time.time())
        # print(self.remote_players.pool)
        message = self.connection_menager.receive_player_message()
        while message:
            if message and message.player_id != self.player.id:
                # print(f'update: {message}')
                if message.player_id not in self.remote_players.pool:
                    self.remote_players.add_player(message)
                else:
                    self.remote_players.update_player(message)
            message = self.connection_menager.receive_player_message()

        for obj in self.objects:
            if issubclass(type(obj), BaseResource) and self.player.shape.shapes_collide(obj.rect.shape).points:
                self.player.consume_resource(obj)
                self.objects.remove(obj)
                self.space.remove(obj.rect.body, obj.rect.shape)

    def save(self):
        logger.info("Saved into file")
        resources = [
            o
            for o in self.objects
            if type(o).__base__ == BaseResource
        ]
        data = {
            "player": {
                "position": self.player.body.position,
                "inventory": self.player.inv.icons,
                "resources": resources,
                "seed": self.floor.seed
            },
            "terrain": [
                o.save()
                for o in self.floor.bricks
            ]
        }
        with open("save.g2", "wb") as file:
            pickle.dump(data, file)

    def load(self, save_name: str):
        with open(save_name, "rb") as file:
            data = pickle.load(file)
        self.player.body.position = data["player"]["position"]
        self.player.inv.icons = data["player"]["inventory"]
        self.floor.noise.seed(data["player"]["seed"])
        self.floor.load(data["terrain"])
        for resource in data["player"]["resources"]:
            resource: BaseResource
            self.objects.append(resource)
            resource.materialize(resource.rect.body.position, self.space)

    def handle_command(self):
        command = self._commands_buffer[-1]
        self._pars.set_line(command)
        token = self._pars.get_tokens()
        if not token:
            return
        token = token[0]
        print(f"VoxelWorld, handle_command, token is ({token.__str__()})")

        value: List[Token] = token.value

        if token.type == "call1" and value[0] == "msg":
            self.connection_menager.send_chat_message(value[1].value)
            return

        if value[2] is None:
            return

        if token.type == "call" and value[0] == "set" and value[1] == "gravity" and value[2].type == "Number":
            gravity = value[2].value
            self.space.gravity = pymunk.Vec2d(self.space.gravity.x, -gravity)

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not self.menu.active:
                self.reset_scene()
            if event.key == pygame.K_SPACE:
                self.player.jump(self.floor.space)
            if event.key == pygame.K_ESCAPE:
                self.menu.active = not self.menu.active
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            self.menu.handle_mouse(event)
        if event.type == pygame.KEYDOWN:
            self.menu.handle_keyboard(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                pos = convert(event.pos, self.size_sc[1])
                resources = self.player.mine(self.floor, self.camera_shift + pos)
                if resources:
                    self.objects.extend(resources)

    def render(self):
        self.bg.render(self.display, self.camera_shift)
        self.remote_players.render(self.display, self.camera_shift)
        for obj in self.objects:
            obj.render(self.display, self.camera_shift)
        for p in self.player.dp:
            pos = [p.x - self.camera_shift[0], p.y + self.camera_shift[1]]
            pygame.draw.circle(self.display, (255, 0, 0), pos, 10)
        if self.menu.active:
            self.menu.render(self.display)
        self.player.inv.render(self.display)

    def pop_buffer(self) -> Optional[str]:
        return None if len(self._commands_buffer) == 0 else self._commands_buffer.pop(0)

