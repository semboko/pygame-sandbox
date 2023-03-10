import pygame
import pymunk
from pygame.event import Event

from scenes.abstract import AbstractPymunkScene
from scenes.components.car import Car
from scenes.components.floor import RandomFloor


class CarScene(AbstractPymunkScene):
    car: Car
    floor: RandomFloor

    def reset_scene(self):
        super().reset_scene()
        self.car = Car(250, 250, 100, 50, self.space)
        self.floor = RandomFloor(0, self.display.get_width(), 0, 200, 20, self.space)
        self.objects.extend((self.car, ))

    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.car.motor.rate += .5
        elif keys[pygame.K_d]:
            self.car.motor.rate -= .5
        else:
            self.car.motor.rate = int(self.car.motor.rate * 0.96)

        self.floor.update_segments(self.car.get_camera_shift())

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_scene()
            if event.key == pygame.K_SPACE:
                self.car.jump()
            if event.key == pygame.K_b:
                self.car.switch_wd()

    def render(self):
        super().render()
        self.floor.render(self.display, self.car.get_camera_shift())
