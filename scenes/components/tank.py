import pymunk
from pygame.surface import Surface
from pygame import draw
from pymunk import Space, Body, Poly, ShapeFilter, Shape, PivotJoint, SimpleMotor, GearJoint
from scenes.utils import convert
from scenes.components.ball import Ball
from typing import List, Sequence
import pygame


class Tank:
    body: Body
    shape: Shape
    collision_filter: ShapeFilter
    wheels: List[Ball]
    motor: SimpleMotor
    turret_shape: Shape

    def __init__(self, x, y, width, height, space: Space):
        self.add_body(x, y, width, height, space)
        self.add_wheels(x, y, width, height, space)
        self.add_turret(x, y, width, height, space)
        self.add_motor(space)

    def add_body(self, x, y, width: int, height: int, space: Space):
        self.body = Body()
        self.collision_filter = ShapeFilter(group=0b1)
        vertices = (
            (x - width/2, y - height/2),
            (x + width/2, y - height/2),
            (x + width/2, y),
            (x - width/2, y),
        )

        self.shape = Poly(self.body, vertices)
        self.shape.density = 1
        self.shape.filter = self.collision_filter
        space.add(self.body, self.shape)

    def add_wheels(self, x: int, y: int, body_width: int, body_height: int, space: Space):
        wheel_diameter = body_height//2
        wheels_number = (body_width // wheel_diameter) + 1

        self.wheels = []
        wheel_x = x + body_width//2
        wheel_y = y - body_height//2
        for _ in range(wheels_number):
            wheel = Ball(wheel_x, wheel_y, wheel_diameter//2, space)
            wheel.shape.density = .7
            wheel.shape.filter = self.collision_filter
            wheel.shape.friction = 1
            wheel.shape.elasticity = .2
            space.add(PivotJoint(wheel.body, self.body, (0, 0), self.body.world_to_local((wheel_x, wheel_y))))
            if self.wheels:
                space.add(GearJoint(wheel.body, self.wheels[-1].body, 0, 1))
            self.wheels.append(wheel)
            wheel_x -= wheel_diameter

    def add_motor(self, space: Space):
        self.motor = SimpleMotor(self.body, self.wheels[-1].body, 0)
        space.add(self.motor)

    def add_turret(self, x, y, width, height, space: Space):
        vertices = (
            (x - width//4, y),
            (x + width//4, y),
            (x + width//4, y + height//2),
            (x - width//4, y + height//2),
        )
        self.turret_shape = Poly(self.body, vertices)
        self.turret_shape.filter = self.collision_filter
        space.add(self.turret_shape)

    def add_gun(self, x, y ,width, height, space: Space):
        pass

    def update_velocity(self, keys: Sequence[bool]):
        if keys[pygame.K_d]:
            self.motor.rate += 1
            return
        if keys[pygame.K_a]:
            self.motor.rate -= 1
            return

        self.motor.rate *= .8

    def update(self):
        keys = pygame.key.get_pressed()
        self.update_velocity(keys)

    def render(self, display: Surface):
        h = display.get_height()
        vert = [convert(self.body.local_to_world(v), h) for v in self.shape.get_vertices()]
        draw.polygon(display, (212, 212, 212), vert)

        turret_vert = [convert(self.body.local_to_world(v), h) for v in self.turret_shape.get_vertices()]
        draw.polygon(display, (212, 212, 212), turret_vert)

        for wheel in self.wheels:
            wheel.render(display)
