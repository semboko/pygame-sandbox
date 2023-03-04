import pygame
from pygame.event import Event
from pymunk import Body

from scenes.abstract import AbstractPymunkScene
from scenes.components.random_floor import RandomFloor
from scenes.components.segment import Segment
from scenes.components.bullet import Bullet
from scenes.components.ball import Ball
from scenes.components.tank import Tank
from scenes.utils import convert


class TankScene(AbstractPymunkScene):
    tank: Tank
    floor: RandomFloor

    def reset_scene(self):
        super().reset_scene()
        self.tank = Tank(250, 160, self.space)
        self.floor = RandomFloor(0, self.display.get_width(), 0, 30, 30, self.space)
        self.objects.extend((self.tank, self.floor))

    def update(self):
        super().update()
        self.tank.update()
        # self.update_bullets()
        # self.update_balls()

    def update_bullets(self):
        for obj in self.objects:
            if not isinstance(obj, Bullet):
                continue
            if obj.is_outside(self.display):
                obj.remove(self.space)
                self.objects.remove(obj)
                continue
            if obj.ready_to_explode(self.space):
                obj.explode(self.space)
                self.objects.remove(obj)

    def update_balls(self):
        for obj in self.objects:
            if isinstance(obj, Ball):
                _, y = obj.body.position
                if y < 0:
                    self.space.remove(obj.body, obj.shape)
                    self.objects.remove(obj)
                    print("Ball is removed")

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == ord("r"):
                self.reset_scene()

            # Whitespace
            if event.key == 32:
                bullet = self.tank.shot()
                self.objects.append(bullet)

        if event.type == pygame.MOUSEBUTTONDOWN:
            h = self.display.get_height()
            x, y = event.dict["pos"]
            ball = Ball(*convert((x, y), h), 10, self.space, color=(55, 252, 10))
            ball.body.mass = 100
            self.objects.append(ball)

