import pygame

from scenes.abstract import AbstractPymunkScene
from pygame.event import Event
from scenes.components import Ball, Segment
import pymunk
from pymunk.constraints import PinJoint, PivotJoint, DampedSpring, DampedRotarySpring, SimpleMotor, GearJoint
from scenes.utils import convert


class PJ:
    def __init__(self, joint: pymunk.Constraint) -> None:
        self.joint = joint

    def render(self, display: pygame.Surface) -> None:
        h = display.get_height()
        if isinstance(self.joint, (PivotJoint, PinJoint)):
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

    def handle_event(self, event: Event) -> None:
        h = self.display.get_height()

        if event.type == pygame.MOUSEBUTTONDOWN and event.dict["button"] == 5:
            x, y = convert(event.dict["pos"], h)
            self.objects.append(Ball(x, y, 2, self.space))
        if event.type == pygame.MOUSEBUTTONDOWN and event.dict["button"] == 3:
            x, y = convert(event.dict["pos"], h)
            objs = self.space.point_query((x, y), 2, pymunk.ShapeFilter())
            if objs:
                body = objs[0].shape.body
                body.apply_impulse_at_local_point((0, -600000), (20, 0))

