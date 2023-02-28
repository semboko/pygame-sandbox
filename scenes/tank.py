from scenes.abstract import AbstractPymunkScene
from pygame.event import Event
import pygame
from scenes.components.tank import Tank
from scenes.components.segment import Segment
from scenes.components.random_floor import RandomFloor
from pymunk import Body


class TankScene(AbstractPymunkScene):
    tank: Tank
    floor: RandomFloor

    def reset_scene(self):
        super().reset_scene()
        self.tank = Tank(250, 160, 130, 50, self.space)
        self.floor = RandomFloor(0, self.display.get_width(), 0, 70, 20, self.space)
        self.objects.extend((self.tank, self.floor))
    
    def update(self):
        super().update()
        self.tank.update()

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if chr(event.key) == "r":
                self.reset_scene()
