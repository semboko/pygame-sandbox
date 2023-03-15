import pygame
import pymunk
from pygame.event import Event

from scenes.abstract import AbstractPymunkScene
from scenes.components.car import Car
from scenes.components.terrain import Terrain


class CarScene(AbstractPymunkScene):
    def reset_scene(self):
        super().reset_scene()
        self.car = Car(250, 250, 100, 50, self.space)
        self.floor = Terrain(0, self.display.get_width(), 0, 20, 20, self.space)
        self.objects.extend((self.car, self.floor))

    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.car.motor.rate += .5
        elif keys[pygame.K_d]:
            self.car.motor.rate -= .5
        else:
            self.car.motor.rate = int(self.car.motor.rate * 0.96)

        self.camera_shift = pymunk.Vec2d(self.car.get_x_shift(), 0)
        self.floor.update(self.camera_shift.x)

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_scene()
            if event.key == pygame.K_SPACE:
                self.car.jump()
