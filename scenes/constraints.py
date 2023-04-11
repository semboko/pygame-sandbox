import pygame
import pymunk
from pygame.event import Event
from pymunk.constraints import DampedRotarySpring, DampedSpring, GearJoint, PinJoint, PivotJoint, SimpleMotor

from scenes.abstract import AbstractPymunkScene
from scenes.components import Ball, Segment
from scenes.utils import convert


class PJ:
    def __init__(self, joint: pymunk.Constraint) -> None:
        self.joint = joint

    def render(self, display: pygame.Surface) -> None:
        h = display.get_height()
        if isinstance(self.joint, (PivotJoint, PinJoint, DampedSpring)):
            anchor_a = self.joint.a.local_to_world(self.joint.anchor_a)
            anchor_b = self.joint.b.local_to_world(self.joint.anchor_b)
        else:
            anchor_a = self.joint.a.position
            anchor_b = self.joint.b.position
        x1 = convert(anchor_a, h)
        x2 = convert(anchor_b, h)
        pygame.draw.line(display, (255, 255, 0), x1, x2, 3)


class ConstraintScene(AbstractPymunkScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ball1 = Ball(250, 250, 30, self.space)
        ball2 = Ball(350, 250, 30, self.space)

        self.space.add(PivotJoint(ball1.body, self.space.static_body, (250, 250)))
        # spring = PinJoint(ball1.body, ball2.body, (0, -30), (-30, 0))
        # self.space.add(spring)

        self.space.add(SimpleMotor(ball1.body, self.space.static_body, 3.14))
        self.space.add(GearJoint(ball1.body, ball2.body, 0, 0.5))

        floor = Segment((0, 20), (500, 20), 5, self.space, btype=pymunk.Body.STATIC)

        self.objects.extend((ball1, ball2, floor))

    def handle_event(self, event: Event) -> None:
        h = self.display.get_height()

        if event.type == pygame.MOUSEBUTTONDOWN and event.dict["button"] == 5:
            x, y = convert(event.dict["pos"], h)
            self.objects.append(Ball(x, y, 2, self.space))
        if event.type == pygame.MOUSEBUTTONDOWN and event.dict["button"] == 3:
            x, y = convert(event.dict["pos"], h)
            objs = self.space.point_query((x, y), 2, pymunk.ShapeFilter())
            if len(objs) == 1:
                body = objs[0].shape.body
                body.apply_impulse_at_local_point((0, -20000), (20, 0))
