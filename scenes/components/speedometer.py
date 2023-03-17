import pymunk
import pygame
from pygame.surface import Surface
from pymunk import Vec2d
from math import sin, cos


class Speedometer:
    def __init__(self, center_x: int, center_y: int, min_speed: int, max_speed: int, radius: int = 60) -> None:
        self.x, self.y = center_x, center_y
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.r = radius
        self.speed = 0

    def update(self, speed: int) -> None:
        if speed < self.min_speed:
            speed = self.min_speed
        if speed > self.max_speed:
            speed = self.max_speed
        self.speed = round(speed / (self.max_speed - self.min_speed), 2)
        print(self.speed)

    def render(self, display: Surface, camera_shift: Vec2d) -> None:
        pygame.draw.circle(display, (255, 0, 0), (self.x, self.y), self.r, 2)

