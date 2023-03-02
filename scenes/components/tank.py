from typing import List, Sequence

import pygame
import pymunk
from math import cos, sin
from pygame import draw
from pygame.surface import Surface
from pymunk import Body, GearJoint, PivotJoint, Poly, Shape, ShapeFilter, SimpleMotor, Space, DampedRotarySpring, RatchetJoint, RotaryLimitJoint

from scenes.components.ball import Ball
from scenes.components.rect import Rect
from scenes.utils import convert


class Tank:
    wheel_holder: Rect
    collision_filter: ShapeFilter
    wheels: List[Ball]
    motor: SimpleMotor
    turret_shape: Shape

    def __init__(self, x, y, width, height, space: Space):
        self.width = width
        self.height = height
        self.collision_filter = ShapeFilter(group=0b1)

        self.add_wheel_holder(x, y - height // 4, width, height // 2, space)
        self.add_wheels(x, y, width, height, space)
        self.add_turret(width, height, space)
        self.add_gun(x, y, width, height, space)
        self.add_bullet()
        self.add_motor(space)

    def add_wheel_holder(self, x, y, width: int, height: int, space: Space):
        self.wheel_holder = Rect(x, y, width, height, space, color=(60, 163, 31))
        self.wheel_holder.body.mass = 10000
        self.wheel_holder.shape.filter = self.collision_filter

    def add_wheels(self, x: int, y: int, body_width: int, body_height: int, space: Space):
        wheel_diameter = body_height // 2
        wheels_number = (body_width // wheel_diameter) + 1
        wh_body = self.wheel_holder.body
        self.wheels = []
        wheel_x = x + body_width // 2
        wheel_y = y - body_height // 2
        for _ in range(wheels_number):
            wheel = Ball(wheel_x, wheel_y, wheel_diameter // 2, space)
            wheel.shape.density = 0.7
            wheel.shape.filter = self.collision_filter
            wheel.shape.friction = 1
            wheel.shape.elasticity = 0.2
            space.add(PivotJoint(wheel.body, wh_body, (0, 0), wh_body.world_to_local((wheel_x, wheel_y))))
            if self.wheels:
                space.add(GearJoint(wheel.body, self.wheels[-1].body, 0, 1))
            self.wheels.append(wheel)
            wheel_x -= wheel_diameter

    def add_motor(self, space: Space):
        self.motor = SimpleMotor(self.wheel_holder.body, self.wheels[-1].body, 0)
        space.add(self.motor)

    def add_turret(self, width, height, space: Space):
        vertices = (
            (-width // 4, height // 4),
            (width // 4, height // 4),
            (width // 4, height // 1.5),
            (-width // 4, height // 1.5),
        )
        self.turret_shape = Poly(self.wheel_holder.body, vertices)
        self.turret_shape.filter = self.collision_filter
        space.add(self.turret_shape)

    def add_gun(self, x, y, width, height, space: Space):
        self.gun = Rect(x + width//2, y + height//4, width, 5, space, color=(49, 122, 28))
        self.gun.body.mass = 20
        self.gun.shape.filter = self.collision_filter
        space.add(PivotJoint(self.gun.body, self.wheel_holder.body, (-width//2, 2), (0, height//2)))
        self.gun_joint = RotaryLimitJoint(self.gun.body, self.wheel_holder.body, -.2, 0)
        space.add(self.gun_joint)

    def add_bullet(self):
        space = self.wheel_holder.body.space
        width, height = self.width, self.height
        x, y = self.wheel_holder.body.position
        self.bullet = Ball(x, y + height//4, 4, space)
        self.bullet.shape.elasticity = .1
        self.bullet.body.mass = 400
        self.bullet_holder = PivotJoint(self.gun.body, self.bullet.body, (width//2, 0), (0, 0))
        space.add(self.bullet_holder)
        self.bullet.shape.filter = self.collision_filter

    def shot(self) -> Ball:
        space = self.bullet.body.space
        space.remove(self.bullet_holder)
        r = self.bullet.shape.radius
        x = r * cos(self.gun.body.angle)
        y = r * sin(self.gun.body.angle)
        force = (x * 10000000, y * 10000000)
        self.bullet.body.apply_force_at_local_point(force, (0, 0))
        self.wheel_holder.body.apply_force_at_local_point((-force[0]*5, -force[1]*5), (0, 0))
        prev_bullet = self.bullet
        self.add_bullet()
        return prev_bullet

    def update_velocity(self, keys: Sequence[bool]):
        if keys[pygame.K_d]:
            self.motor.rate += 1
            return
        if keys[pygame.K_a]:
            self.motor.rate -= 1
            return

        self.motor.rate *= 0.8

    def update_gun_angle(self, keys: Sequence[bool]):
        if keys[pygame.K_UP]:
            self.gun_joint.min -= .05
            self.gun_joint.max -= .05
        if keys[pygame.K_DOWN]:
            self.gun_joint.min += .05
            self.gun_joint.max += .05

    def update(self):
        keys = pygame.key.get_pressed()
        self.update_velocity(keys)
        self.update_gun_angle(keys)

    def render(self, display: Surface):
        self.wheel_holder.render(display)
        h = display.get_height()
        turret_vert = [convert(self.turret_shape.body.local_to_world(v), h) for v in self.turret_shape.get_vertices()]
        draw.polygon(display, (60, 163, 31), turret_vert)
        self.gun.render(display)
        self.bullet.render(display)
        for wheel in self.wheels:
            wheel.render(display)
