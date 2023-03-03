from typing import List, Sequence

import pygame
import pymunk
from pymunk.vec2d import Vec2d
from math import cos, sin, degrees
from pygame import draw
from pygame.surface import Surface
from pymunk import Body, GearJoint, PivotJoint, Poly, Shape, ShapeFilter, SimpleMotor, Space, DampedRotarySpring, RatchetJoint, RotaryLimitJoint

from scenes.components.ball import Ball
from scenes.components.bullet import Bullet
from scenes.components.rect import Rect
from scenes.utils import convert


TANK_WIDTH = 250
TANK_HEIGHT = 74
WHEEL_R = 9


class TankBase:
    def __init__(self, tank_x: int, tank_y: int, cf: ShapeFilter, space: Space):
        self.collision_filter = cf
        self.width = 213
        self.height = 44

        delta_x, delta_y = -18.5, -15

        self.body = Body()
        self.body.position = tank_x + delta_x, tank_y + delta_y

        raw_vertices = (
            Vec2d(0, 30),
            Vec2d(0, 50),
            Vec2d(10, 51),
            Vec2d(37, 72),
            Vec2d(172, 72),
            Vec2d(200, 58),
            Vec2d(204, 40),
            Vec2d(73, 36),
            Vec2d(50, 30),
            Vec2d(0, 30)
        )
        self.relative_verts = [
            convert(v + (-self.width/2 + delta_x, -self.height/2 + delta_y), self.height) for v in raw_vertices
        ]
        self.shape = Poly(self.body, self.relative_verts)
        self.shape.density = 1
        space.add(self.body, self.shape)

        self.image = pygame.image.load("./scenes/assets/body.png")
        self.rect = self.image.get_rect()

    def render(self, display: Surface):
        h = display.get_height()
        bb = self.shape.bb
        self.rect.x, self.rect.y = convert((bb.left, bb.top), h)
        image = pygame.transform.rotate(self.image, degrees(self.body.angle))
        display.blit(image, self.rect)

        # verts = [convert(self.body.local_to_world(v), h) for v in self.shape.get_vertices()]
        # draw.polygon(display, (60, 163, 31), verts)


class TankWheel:
    def __init__(self, global_x: int, global_y: int, space: Space) -> None:
        self.body = Body()
        self.body.position = global_x, global_y

        self.shape = pymunk.Circle(self.body, WHEEL_R)
        self.shape.density = 1

        space.add(self.body, self.shape)

        self.image = pygame.image.load("./scenes/assets/wheel.png")
        self.rect = self.image.get_rect()

    def render(self, display: Surface) -> None:
        h = display.get_height()
        bb = self.shape.bb
        self.rect.x, self.rect.y = convert((bb.left, bb.top), h)
        image = pygame.transform.rotate(self.image, degrees(self.body.angle))
        display.blit(image, self.rect)


class Tank:
    wheel_holder: Rect
    collision_filter: ShapeFilter
    wheels: Sequence[TankWheel]
    motor: SimpleMotor
    turret_shape: Shape

    def __init__(self, x, y, space: Space):
        self.collision_filter = ShapeFilter(group=0b1)
        self.space = space

        self.tank_base = TankBase(x, y, self.collision_filter, space)
        self.wheels = self.add_wheels(x, y)
        # self.add_turret(width, height, space)
        # self.add_gun(x, y, width, height, space)
        # self.add_bullet()
        # self.add_motor(space)

    def add_wheels(self, x: int, y: int) -> Sequence[TankWheel]:
        wheel_coords = ((37, 55), (57, 55), (76, 55))
        wheels = []
        for coord in wheel_coords:
            wheel_x = x - TANK_WIDTH/2 + coord[0] + WHEEL_R/2
            wheel_y = y - TANK_HEIGHT//2 + coord[1]
            wheels.append(TankWheel(wheel_x, wheel_y, self.space))
        return wheels

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
        self.gun_joint = RotaryLimitJoint(self.gun.body, self.wheel_holder.body, -.1, 0)
        space.add(self.gun_joint)

    def add_bullet(self):
        space = self.wheel_holder.body.space
        width, height = TANK_WIDTH, TANK_HEIGHT
        x, y = self.wheel_holder.body.position
        self.bullet = Bullet(x, y + height//4, 4, space)
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
        relative_angle = self.gun.body.angle - self.wheel_holder.body.angle
        if keys[pygame.K_UP] and relative_angle < 1.2:
            self.gun_joint.min -= .01
            self.gun_joint.max -= .01
        if keys[pygame.K_DOWN] and relative_angle > 0:
            self.gun_joint.min += .01
            self.gun_joint.max += .01

    def update(self):
        keys = pygame.key.get_pressed()
        self.update_velocity(keys)
        self.update_gun_angle(keys)

    def render(self, display: Surface):
        self.tank_base.render(display)
        for wheel in self.wheels:
            wheel.render(display)
