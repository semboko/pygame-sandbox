import pygame
import pymunk
from pygame.event import Event

from scenes.abstract import AbstractPymunkScene
from scenes.components.car import Car
from scenes.components.segment import Segment


class CarScene(AbstractPymunkScene):
    def reset_scene(self):
        super().reset_scene()
        self.car = Car(250, 250, 100, 50, self.space)
        self.floor = Segment((0, 20), (self.display.get_width(), 20), 5, self.space, btype=pymunk.Body.STATIC)
        self.floor.shape.friction = .9
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

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_r:
                self.reset_scene()
            if event.key == pygame.K_SPACE:
                self.car.jump(self.floor.shape)
