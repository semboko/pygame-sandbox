import pygame
from pygame.event import Event
from pymunk import Body

from scenes.abstract import AbstractPymunkScene
from scenes.components.random_floor import RandomFloor
from scenes.components.segment import Segment
from scenes.components.ball import Ball
from scenes.components.tank import Tank
from scenes.utils import convert


class TankScene(AbstractPymunkScene):
    tank: Tank
    floor: RandomFloor

    def reset_scene(self):
        super().reset_scene()
        self.tank = Tank(250, 160, 130, 50, self.space)
        self.floor = RandomFloor(0, self.display.get_width(), 0, 80, 30, self.space)
        self.objects.extend((self.tank, self.floor))

    def update(self):
        super().update()
        self.tank.update()

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
            ball = Ball(*convert((x, y), h), 40, self.space)
            self.objects.append(ball)

