import pickle
import random

import pygame
import pymunk
from pygame.event import Event

from scenes.components.resources import BaseResource
from scenes.abstract import AbstractPymunkScene
from scenes.components.player import Player
from scenes.components.resources import *
from scenes.components.terrain import Terrain, TerrainBlock
from scenes.components.biomes import BaseBiome, Flatland, Mountain, Swamp
from scenes.components.sprite import Sprite
from scenes.components.tile import Background
from scenes.utils import convert

pygame.init()
pygame.font.init()


class VoxelWorld(AbstractPymunkScene):
    def reset_scene(self):
        super().reset_scene()
        self.player = Player(250, 250, 50, 60, self.space, (25, 25, 25), True)
        self.floor = Terrain(0, self.display.get_width(), 10, 200, 400, self.space)
        self.objects.extend((self.player, self.floor))
        self.menu_state = 0
        self.bg = Background(self.display.get_width())

    def update(self):
        if 0 <= self.menu_state <= 1:
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

        self.camera_shift = pymunk.Vec2d(self.player.body.position.x - 250, self.player.body.position.y - 250)
        self.floor.update(self.camera_shift.x)

        for obj in self.objects:
            if issubclass(type(obj), BaseResource) and self.player.shape.shapes_collide(obj.rect.shape).points:
                self.player.consume_resource(obj)
                self.objects.remove(obj)
                self.space.remove(obj.rect.body, obj.rect.shape)

    def save(self):
        resources = [
            o
            for o in self.objects
            if type(o).__base__ == BaseResource
        ]
        data = {
            "player": {
                "position": self.player.body.position,
                "inventory": self.player.inv.icons,
                "resources": resources
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
            self.floor.load(data["terrain"])
            for resource in data["player"]["resources"]:
                resource: BaseResource
                self.objects.append(resource)
                resource.materialize(resource.rect.body.position, self.space)

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_scene()
            if event.key == pygame.K_SPACE:
                self.player.jump(self.floor.space)
            if event.key == pygame.K_ESCAPE:
                if self.menu_state != 2:
                    self.menu_state = 2
                else:
                    self.menu_state = 0
            if event.key == pygame.K_q:
                if self.menu_state != 1:
                    self.menu_state = 1
                else:
                    self.menu_state = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                pos = convert(event.pos, self.size_sc[1])
                resources = self.player.mine(self.floor, self.camera_shift + pos)
                if resources:
                    self.objects.extend(resources)

    def render(self):
        # self.display.fill((255, 255, 255))
        self.bg.render(self.display, self.camera_shift)
        for obj in self.objects:
            obj.render(self.display, self.camera_shift)
        for p in self.player.dp:
            pos = [p.x - self.camera_shift[0], p.y + self.camera_shift[1]]
            pygame.draw.circle(self.display, (255, 0, 0), pos, 10)
        if 1 <= self.menu_state <= 2:
            font = pygame.font.SysFont("Comic Sans MS", 30)
            pos = " ".join([str(round(i, 2)) for i in list(self.player.body.position)])
            text = f"position: {pos}, fps: {round(self.game.clock.get_fps(), 2)}"
            self.display.blit(font.render(text, True, (0, 0, 0)), (10, 10))
        self.player.inv.render(self.display)
