import pymunk
from pygame.surface import Surface

from scenes.components.ball import Ball
from scenes.components.pj import PJ
from scenes.components.rect import Rect


class Suspension:
    def __init__(
        self,
        car_body: pymunk.Body,
        car_width: int,
        car_height: int,
        cf: pymunk.ShapeFilter,
        side: int,
        space: pymunk.Space,
    ):
        car_x, car_y = car_body.position
        arm_width, arm_height = car_width // 2, 5
        self.arm = Rect(
            int(car_x + (car_width / 2 + arm_width / 2) * side),
            int(car_y - car_height / 2 + arm_height / 2),
            arm_width,
            arm_height,
            space,
            (255, 255, 0),
        )
        self.arm.shape.filter = cf
        space.add(
            pymunk.PivotJoint(
                car_body,
                self.arm.body,
                ((car_width / 2 - arm_height) * side, (-car_height / 2 + arm_height)),
                (side * (-arm_width / 2 + arm_height), 0),
            )
        )
        arm_x, arm_y = self.arm.body.position
        self.wheel = Ball(arm_x + (arm_width / 2 + arm_height) * side, arm_y, arm_width // 3, space)
        self.wheel.shape.filter = cf
        self.wheel.shape.friction = 1
        space.add(pymunk.PivotJoint(self.arm.body, self.wheel.body, ((arm_width / 2 - arm_height) * side, 0), (0, 0)))
        self.spring = pymunk.DampedSpring(car_body, self.arm.body, ((car_width / 2) * side, 0), (0, 0), 5, -74000, 10)
        space.add(self.spring)
        angle_limit = (0.2, 0.8) if side == -1 else (-0.8, 0.2)
        space.add(pymunk.RotaryLimitJoint(car_body, self.arm.body, *angle_limit))

    def render(self, display: Surface, camera_shift: pymunk.Vec2d):
        self.wheel.render(display, camera_shift)
        self.arm.render(display, camera_shift)
        PJ(self.spring).render(display, camera_shift)


class Car:
    def __init__(self, x: int, y: int, width: int, height: int, space: pymunk.Space) -> None:
        self.cf = pymunk.ShapeFilter(group=0b1)
        self.car_body = Rect(x, y, width, height, space, debug=True)
        self.car_body.body.mass = 500
        self.car_body.body.center_of_gravity = (width / 2, -height)
        self.car_body.shape.filter = self.cf
        self.front_suspension = Suspension(self.car_body.body, width, height, self.cf, 1, space)
        self.rear_suspension = Suspension(self.car_body.body, width, height, self.cf, -1, space)

        self.init_x = x

        space.add(pymunk.GearJoint(self.front_suspension.wheel.body, self.rear_suspension.wheel.body, 0, 1))
        self.motor = pymunk.SimpleMotor(self.front_suspension.wheel.body, self.rear_suspension.arm.body, -1)
        space.add(self.motor)

    def get_x_shift(self) -> float:
        return self.car_body.body.position.x - self.init_x

    def jump(self):
        _, car_y = self.car_body.body.position
        if car_y > 150:
            return

        self.car_body.body.apply_impulse_at_local_point((0, 700000), (0, 0))

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        self.car_body.render(display, camera_shift)
        self.front_suspension.render(display, camera_shift)
        self.rear_suspension.render(display, camera_shift)
