import random

import pygame
import pymunk
from pygame.event import Event

from scenes.abstract import AbstractPymunkScene
from scenes.components.rect import Rect
from scenes.components.terrain import Terrain, min_nfs, nfs, max_nfs, micro_nfs
from scenes.components.speedometer import Speedometer
pygame.init()
pygame.font.init()



class VoxelWorld(AbstractPymunkScene):
    def reset_scene(self):
        super().reset_scene()
        self.player = Rect(250, 250, 50, 50, self.space, (25, 25, 25), True)
        self.floor = Terrain(0, self.display.get_width()*4, 10, 200, 400, int(random.random()*100_000_000), self.space, max_nfs)
        self.objects.extend((self.player,self.floor))
        self.menu_state = 0
        self.speed_x = 0

    def update(self):
        if 0 <= self.menu_state <= 1:
            super().update()
        self.player.body.angle = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.body.apply_impulse_at_world_point((-20_000, 0), self.player.body.position)
            self.speed_x -= 5_000
        elif keys[pygame.K_d]:
            self.player.body.apply_impulse_at_world_point((20_000, 0), self.player.body.position)
            self.speed_x += 5_000
        # else:
        #     self.speed_x *= 9.8

        self.camera_shift = pymunk.Vec2d(self.player.body.position.x - 250,self.player.body.position.y - 250)
        self.floor.update(self.camera_shift.x)

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_scene()
            if event.key==pygame.K_SPACE :
                self.player.body.apply_impulse_at_world_point((self.speed_x//20,0),self.player.body.position)
                #p = self.space.segment_query_first(self.player.body.position,(self.player.body.position.x, self.player.body.position.y-20), 0, self.floor.sf)
                #print(p)
                #if self.player.body.position.y-20 <= p.point.y <= self.player.body.position.y:
                self.player.body.apply_impulse_at_world_point((0, 700000), self.player.body.position)
            if event.key==pygame.K_ESCAPE:
                if self.menu_state != 2:
                    self.menu_state = 2
                else:
                    self.menu_state = 0
            if event.key==pygame.K_q:
                if self.menu_state != 1:
                    self.menu_state = 1
                else:
                    self.menu_state = 0

    def render(self):
        super(VoxelWorld, self).render()
        if 1 <= self.menu_state <= 2:
            font = pygame.font.SysFont('Comic Sans MS',30)
            pos = " ".join([str(round(i, 2)) for i in list(self.player.body.position)])
            text = f'position: {pos}, fps: {round(self.game.clock.get_fps(), 2)}, seed: {str(self.floor.seed)}, nfs_func: {self.floor.nfs_name}'
            self.display.blit(
                font.render(text,True,(0,0,0)),
                (10,10)
            )
