from pygame.surface import Surface
import pymunk
import pygame
from scenes.utils import convert
from scenes.components.pj import PJ
from scenes.components.rect import Rect
from scenes.components.ball import Ball


class Suspension:
    def __init__(self, car_body: pymunk.Body, car_width: int, car_height: int, cf: pymunk.ShapeFilter, side: int, space: pymunk.Space):
        car_x, car_y = car_body.position
        arm_width, arm_height = car_width//2, 5
        self.arm = Rect(
            int(car_x + (car_width / 2 + arm_width / 2) * side),
            int(car_y - car_height / 2 + arm_height / 2),
            arm_width, arm_height, space, (255, 255, 0))
        self.arm.shape.filter = cf
        space.add(pymunk.PivotJoint(
            car_body,
            self.arm.body,
            ((car_width/2 - arm_height) * side, (-car_height/2 + arm_height)),
            (side * (-arm_width/2 + arm_height), 0)
        ))
        arm_x, arm_y = self.arm.body.position
        self.wheel = Ball(arm_x + (arm_width / 2 + arm_height) * side, arm_y, arm_width // 2, space)
        self.wheel.shape.filter = cf
        space.add(pymunk.PivotJoint(self.arm.body, self.wheel.body, ((arm_width / 2 - arm_height) * side, 0), (0, 0)))
        self.spring = pymunk.DampedSpring(car_body, self.arm.body, ((car_width/2) * side, 0), (0, 0), 5, -44000, 10)
        space.add(self.spring)
        angle_limit = (0, .8) if side == -1 else (-.8, 0)
        space.add(pymunk.RotaryLimitJoint(car_body, self.arm.body, *angle_limit))

    def render(self, display: Surface):
        self.wheel.render(display)
        self.arm.render(display)
        PJ(self.spring).render(display)


class Car:
    def __init__(self, x: int, y: int, width: int, height: int, space: pymunk.Space) -> None:
        self.cf = pymunk.ShapeFilter(group=0b1)
        self.car_body = Rect(x, y, width, height, space)
        self.car_body.body.mass = 500
        self.car_body.shape.filter = self.cf
        self.front_suspension = Suspension(self.car_body.body, width, height, self.cf, 1, space)
        self.rear_suspension = Suspension(self.car_body.body, width, height, self.cf, -1, space)

    def render(self, display: Surface) -> None:
        self.car_body.render(display)
        self.front_suspension.render(display)
        self.rear_suspension.render(display)
