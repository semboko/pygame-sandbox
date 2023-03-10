import pygame
import pymunk
from pymunk import DampedSpring, PinJoint, PivotJoint, Vec2d

from scenes.utils import convert


class PJ:
    def __init__(self, joint: pymunk.Constraint) -> None:
        self.joint = joint

    def render(self, display: pygame.Surface, pymunk_shift: Vec2d = Vec2d(0, 0)) -> None:
        h = display.get_height()
        if isinstance(self.joint, (PivotJoint, PinJoint, DampedSpring)):
            anchor_a = - pymunk_shift + self.joint.a.local_to_world(self.joint.anchor_a)
            anchor_b = - pymunk_shift + self.joint.b.local_to_world(self.joint.anchor_b)
        else:
            anchor_a = - pymunk_shift + self.joint.a.position
            anchor_b = - pymunk_shift + self.joint.b.position
        x1 = convert(anchor_a, h)
        x2 = convert(anchor_b, h)
        pygame.draw.line(display, (255, 255, 0), x1, x2, 3)
