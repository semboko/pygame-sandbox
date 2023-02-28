from scenes.abstract import AbstractPymunkScene
from pygame.event import Event
import pygame
from scenes.components.tank import Tank
from scenes.components.segment import Segment
from pymunk import Body


class TankScene(AbstractPymunkScene):
    tank: Tank
    floor: Segment

    def reset_scene(self):
        super().reset_scene()
        self.tank = Tank(250, 160, 130, 50, self.space)
        self.floor = Segment((0, 20), (self.display.get_height(), 100), 5, self.space, btype=Body.STATIC)
        self.floor.shape.friction = 1
        self.objects.extend((self.tank, self.floor))
    
    def update(self):
        super().update()
        self.tank.update()

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if chr(event.key) == "r":
                self.reset_scene()
