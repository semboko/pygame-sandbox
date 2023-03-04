from typing import List, Sequence, Tuple, Union

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


def raw_to_poly(raw: Union[Tuple[Vec2d, ...], Tuple[Tuple[int, int], ...]], width: int, height: int) -> List[Tuple[int, int]]:
    return [(vx - width/2, height/2 - vy) for vx, vy in raw]


def get_center(verts: Sequence[Vec2d]) -> Vec2d:
    xs = []
    ys = []
    for x, y in verts:
        xs.append(x)
        ys.append(y)
    return Vec2d(sum(xs)/len(xs), sum(ys)/len(ys))


class TankBase:
    def __init__(self, left_x: int, top_y: int, cf: ShapeFilter, space: Space):
        self.collision_filter = cf
        self.width = 213
        self.height = 44

        cx, cy = left_x + self.width/2, top_y - self.height/2

        self.body = Body()
        self.body.position = cx, cy

        raw_vertices = (
            Vec2d(0, 0),
            Vec2d(0, 20),
            Vec2d(10, 20),
            Vec2d(37, 33),
            Vec2d(172, 33),
            Vec2d(200, 28),
            Vec2d(204, 10),
            Vec2d(73, 6),
            Vec2d(48, 0),
            Vec2d(0, 0)
        )
        self.local_verts = raw_to_poly(raw_vertices, self.width, self.height)
        self.shape = Poly(self.body, self.local_verts)
        self.shape.density = 1
        self.shape.filter = cf
        space.add(self.body, self.shape)

        self.image = pygame.image.load("./scenes/assets/body.png")
        self.rect = self.image.get_rect()

    def render(self, display: Surface):
        h = display.get_height()
        bb = self.shape.bb
        x, y = self.body.position
        self.rect.x, self.rect.y = convert((x - self.width/2, y + self.height/2), h)
        image = pygame.transform.rotate(self.image, degrees(self.body.angle))
        display.blit(image, self.rect)

        # verts = [convert(self.body.local_to_world(v), h) for v in self.shape.get_vertices()]
        # draw.polygon(display, (60, 163, 31), verts, 1)

        # draw.circle(display, (255, 255, 0), convert(self.body.position, h), 2, 1)


class TankWheel:
    def __init__(self, global_x: int, global_y: int, cf: ShapeFilter, space: Space) -> None:
        self.body = Body()
        self.body.position = global_x, global_y
        self.body.mass = 500

        self.shape = pymunk.Circle(self.body, WHEEL_R)
        self.shape.density = 1
        self.shape.friction = 1
        self.shape.filter = cf

        space.add(self.body, self.shape)

        self.image = pygame.image.load("./scenes/assets/wheel.png")
        self.rect = self.image.get_rect()

    def attach_to(self, tank_base: Body, space: Space) -> pymunk.PivotJoint:
        wlocal_x, wlocal_y = tank_base.world_to_local(self.body.position)
        wheel_attachment = PivotJoint(tank_base, self.body, (wlocal_x, wlocal_y), (0, 0))
        space.add(wheel_attachment)
        return wheel_attachment

    def render(self, display: Surface) -> None:
        h = display.get_height()
        self.rect.x, self.rect.y = convert(self.body.position, h)
        image = pygame.transform.rotate(self.image, degrees(self.body.angle))
        display.blit(image, self.rect)

        # draw.circle(display, (255, 0, 0), convert(self.body.position, h), WHEEL_R)
        # alpha = self.body.angle
        # line_end = cos(alpha) * WHEEL_R, sin(alpha) * WHEEL_R
        # draw.line(
        #     display, (0, 0, 0), convert(self.body.position, h), convert(self.body.local_to_world(line_end), h), 1
        # )


class MotorWheel(TankWheel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pygame.image.load("./scenes/assets/motor_wheel.png")


class Turret:
    def __init__(self, left_x: int, top_y: int, cf: ShapeFilter, space: Space):
        self.body = Body()
        self.width = 126
        self.height = 22
        self.body.position = left_x + self.width//2, top_y - self.height//2

        raw_verts = (
            (0, 0), (132, 0), (132, 22), (0, 22)
        )
        self.shape = Poly(self.body, raw_to_poly(raw_verts, self.width, self.height))
        self.shape.density = 1
        self.shape.filter = cf

        self.image = pygame.image.load("./scenes/assets/turret.png")
        self.rect = self.image.get_rect()
        space.add(self.body, self.shape)

    def attach_to(self, tank_base: Body, space: Space):
        bb = self.shape.bb
        lb_x, lb_y = bb.left, bb.bottom
        rb_x, rb_y = bb.right, bb.bottom
        pj1 = PivotJoint(tank_base, self.body, tank_base.world_to_local((lb_x, lb_y)), self.body.world_to_local((lb_x, lb_y)))
        pj2 = PivotJoint(tank_base, self.body, tank_base.world_to_local((rb_x, rb_y)), self.body.world_to_local((rb_x, rb_y)))
        space.add(pj1, pj2)

    def render(self, display: Surface):
        h = display.get_height()

        x, y = self.body.position
        image = pygame.transform.rotate(self.image, degrees(self.body.angle))

        self.rect.x, self.rect.y = convert((x - self.width/2, y + self.height/2 + 17), h)
        display.blit(image, self.rect)

        # verts = [convert(self.body.local_to_world(v), h) for v in self.shape.get_vertices()]
        # draw.polygon(display, (60, 163, 31), verts, 1)


class TankGun:
    def __init__(self, left_x: int, top_y: int, cf: ShapeFilter, space: Space):
        pass

    def render(self, display: Surface):
        pass


class Tank:
    tank_base: TankBase
    collision_filter: ShapeFilter
    wheels: Sequence[TankWheel]
    motor: SimpleMotor
    turret_shape: Shape

    def __init__(self, x, y, space: Space):
        self.collision_filter = ShapeFilter(group=0b1)
        self.space = space

        self.top_y = y + TANK_HEIGHT/2
        self.left_x = x - TANK_WIDTH/2

        self.tank_base = TankBase(self.left_x, self.top_y-30, self.collision_filter, space)
        self.wheels = self.get_wheels()
        self.motor_wheel = self.get_motor_wheel()
        self.motor = self.get_motor()
        self.turret = self.get_turret()
        self.gun = self.get_gun()
        # self.add_bullet()
        # self.add_motor(space)

    def get_wheels(self) -> Sequence[TankWheel]:
        wheel_xs = (38, 57, 76, 95, 115, 135, 160)
        wheel_y = self.top_y - 60
        wheels = []
        for wheel_x in wheel_xs:
            wheel_x = self.left_x + wheel_x
            new_wheel = TankWheel(wheel_x, wheel_y, self.collision_filter, self.space)
            new_wheel.attach_to(self.tank_base.body, self.space)
            wheels.append(new_wheel)
        front_wheel = TankWheel(self.left_x + 184, self.top_y - 50, self.collision_filter, self.space)
        front_wheel.attach_to(self.tank_base.body, self.space)
        wheels.append(front_wheel)
        return wheels

    def get_motor_wheel(self) -> MotorWheel:
        mw = MotorWheel(self.left_x + 14, self.top_y - 41, self.collision_filter, self.space)
        mw.attach_to(self.tank_base.body, self.space)
        return mw

    def get_motor(self) -> SimpleMotor:
        motor = SimpleMotor(self.tank_base.body, self.motor_wheel.body, 0)
        self.space.add(motor)
        for wheel in self.wheels:
            gear = GearJoint(self.motor_wheel.body, wheel.body, 0, 1)
            self.space.add(gear)
        return motor

    def get_turret(self) -> Turret:
        turret = Turret(self.left_x + 36, self.top_y - 15, self.collision_filter, self.space)
        turret.attach_to(self.tank_base.body, self.space)
        return turret

    def get_gun(self) -> TankGun:
        gun = TankGun(self.left_x + 155, self.top_y - 22, self.collision_filter, self.space)
        return gun

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
        # self.update_gun_angle(keys)

    def render(self, display: Surface):
        draw.circle(display, (255, 255, 0), convert((self.left_x + TANK_WIDTH//2, self.top_y - TANK_HEIGHT//2), display.get_height()), 5, 1)
        for wheel in self.wheels:
            wheel.render(display)
        self.motor_wheel.render(display)
        self.tank_base.render(display)
        self.gun.render(display)
        self.turret.render(display)
