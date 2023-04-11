import random

import pygame
import pymunk
from pygame.event import Event

from scenes.abstract import AbstractPymunkScene
from scenes.components.rect import Rect
from scenes.components.terrain import Terrain, min_nfs, nfs, max_nfs, micro_nfs
from scenes.components.speedometer import Speedometer
from scenes.components.player import Player
from scenes.components.resources import *
from scenes.utils import convert

pygame.init()
pygame.font.init()


class VoxelWorld(AbstractPymunkScene):
    def reset_scene(self):
        super().reset_scene()
        self.player = Player(250, 250, 50, 50, self.space, (25, 25, 25), True)
        self.floor = Terrain(0, self.display.get_width(), 10, 200, 400, self.space)
        self.objects.extend((self.player, self.floor))
        self.menu_state = 0

    def update(self):
        if 0 <= self.menu_state <= 1:
            super().update()
        self.player.body.angle = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.move(-1)
        elif keys[pygame.K_d]:
            self.player.move(1)

        self.camera_shift = pymunk.Vec2d(self.player.body.position.x - 250, self.player.body.position.y - 250)
        self.floor.update(self.camera_shift.x)

        for obj in self.objects:
            if type(obj) == BaseResource and self.player.shape.shapes_collide(obj.rect.shape).points:
                self.player.consume_resource(obj)
                self.objects.remove(obj)
                self.space.remove(obj.rect.body, obj.rect.shape)

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
                resources = self.player.mine(self.floor,self.camera_shift + pos)
                if resources:
                    self.objects.extend(resources)

    def render(self):
        super(VoxelWorld, self).render()
        for p in self.player.dp:
            pos = [p.x - self.camera_shift[0], p.y + self.camera_shift[1]]
            pygame.draw.circle(self.display, (255, 0, 0), pos, 10)
        if 1 <= self.menu_state <= 2:
            font = pygame.font.SysFont("Comic Sans MS", 30)
            pos = " ".join([str(round(i, 2)) for i in list(self.player.body.position)])
            text = f"position: {pos}, fps: {round(self.game.clock.get_fps(), 2)}"
            self.display.blit(font.render(text, True, (0, 0, 0)), (10, 10))
