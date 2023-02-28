import pygame

from scenes.abstract import AbstractPymunkScene
from pygame.event import Event
from scenes.components.car import Car
from scenes.components.segment import Segment
import pymunk


class CarScene(AbstractPymunkScene):
    def reset_scene(self):
        super().reset_scene()
        self.car = Car(250, 250, 100, 50, self.space)
        self.floor = Segment((0, 20), (500, 20), 5, self.space, btype=pymunk.Body.STATIC)
        self.objects.extend((self.car, self.floor))

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if chr(event.key) == "r":
                self.reset_scene()
