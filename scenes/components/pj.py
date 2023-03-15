import pygame
import pymunk
from pymunk import DampedSpring, PinJoint, PivotJoint

from scenes.utils import convert


class PJ:
    def __init__(self, joint: pymunk.Constraint) -> None:
        self.joint = joint

    def render(self, display: pygame.Surface, camera_shift: pymunk.Vec2d) -> None:
        h = display.get_height()
        if isinstance(self.joint, (PivotJoint, PinJoint, DampedSpring)):
            anchor_a = self.joint.a.local_to_world(self.joint.anchor_a) - camera_shift
            anchor_b = self.joint.b.local_to_world(self.joint.anchor_b) - camera_shift
        else:
            anchor_a = self.joint.a.position
            anchor_b = self.joint.b.position
        x1 = convert(anchor_a, h)
        x2 = convert(anchor_b, h)
        pygame.draw.line(display, (255, 255, 0), x1, x2, 3)
