from pygame.surface import Surface
import pymunk
import pygame
from scenes.utils import convert
from scenes.components.pj import PJ
from scenes.components.rect import Rect
from scenes.components.ball import Ball


class Car:
    def __init__(self, x: int, y: int, width: int, height: int, space: pymunk.Space) -> None:
        self.cf = pymunk.ShapeFilter(group=0b1)
        self.car_body = Rect(x, y, width, height, space)
        self.car_body.body.mass = 500
        self.car_body.shape.filter = self.cf
        self.add_rear_suspension(x, y, width, height, space)

    def add_rear_suspension(self, x, y, width, height, space: pymunk.Space):
        self.rear_sleeve = Ball(x - 5 * width / 6, y - height, 5, space)
        self.rear_joint = pymunk.PinJoint(self.car_body.body, self.rear_sleeve.body, (-width//2, -height//2), (0, 0))
        self.rear_spring = pymunk.DampedSpring(
            self.car_body.body, self.rear_sleeve.body, (-width/2, 0), (0, 0), 5, -10000, 10
        )
        self.rear_wheel = Ball(*self.rear_sleeve.body.position, 15, space)
        self.rear_wheel.body.mass = 100
        self.rear_wheel_attachment = pymunk.PivotJoint(self.rear_sleeve.body, self.rear_wheel.body, (0, 0), (0, 0))
        # self.rear_limit = pymunk.SlideJoint(self.car_body.body, self.rear_sleeve.body, (-width/2, -height/2), (0, 0), height, height+50)
        space.add(self.rear_joint, self.rear_spring, self.rear_wheel_attachment)
        self.rear_wheel.shape.filter = self.cf
        self.rear_sleeve.shape.filter = self.cf

    def render(self, display: Surface) -> None:
        self.car_body.render(display)
        self.rear_sleeve.render(display)
        PJ(self.rear_joint).render(display)
        PJ(self.rear_spring).render(display)
        PJ(self.rear_wheel_attachment).render(display)
        self.rear_wheel.render(display)
