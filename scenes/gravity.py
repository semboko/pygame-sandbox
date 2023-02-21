from typing import Tuple

import pygame.draw
import pymunk
from pygame.event import Event
from pygame.surface import Surface

from scenes.abstract import AbstractScene

from .utils import convert
from logging import getLogger

log = getLogger()

class Ball:
    def __init__(self, x: int, y: int, r: int, space: pymunk.Space, btype: int = pymunk.Body.DYNAMIC):
        self.body = pymunk.Body(body_type=btype)
        self.body.position = x, y
        self.pos = x, y
        self.shape = pymunk.Circle(self.body, r)
        self.shape.density = 1
        self.shape.elasticity = 0.9
        self.r = r
        space.add(self.body, self.shape)

    def render(self, display: Surface) -> None:
        h = display.get_height()
        pygame.draw.circle(display, (244, 0, 0), convert(self.body.position, h), self.r)
        log.info(f"circle by id {id(self)}: angle = {self.body.angle}, pos = {tuple(self.body.position)}")
        # Create a new pygame.Rect object for the ball
        self.rect = pygame.Rect(*tuple(convert((self.body.position.x - self.r, (self.body.position.y - self.r)+2 * self.r), display.get_height())), 2 * self.r, 2 * self.r)
        #pygame.draw.rect(display, (50, 50, 50), self.rect)


class Segment:
    def __init__(
            self, a: Tuple[int, int], b: Tuple[int, int], r: int, space: pymunk.Space, btype: int = pymunk.Body.DYNAMIC
    ):
        self.body = pymunk.Body(body_type=btype)
        self.shape = pymunk.Segment(self.body, a, b, r)
        self.shape.elasticity = 0.9
        self.r = r
        space.add(self.body, self.shape)

        # Create a new pygame.Rect object for the segment
        min_x = min(a[0], b[0]) - r
        max_x = max(a[0], b[0]) + r
        min_y = min(a[1], b[1]) - r
        max_y = max(a[1], b[1]) + r
        self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def render(self, display: Surface) -> None:
        h = display.get_height()
        pygame.draw.line(display, (0, 0, 0), convert(self.shape.a, h), convert(self.shape.b, h), self.r)


class GravityScene(AbstractScene):
    space: pymunk.Space
    circle: Ball
    segment: Segment
    pause: bool
    renders_objs: list
    move_old: tuple
    movement: bool

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.reset_scene()

    def handle_events(self, events: Tuple[Event], mouse: Tuple[int, int]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause = True
                elif event.key == pygame.K_r:
                    self.reset_scene()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.pause = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.dict["button"] == 1:
                    self.renders_objs.append(Ball(*convert(event.pos, self.size_sc[1]), 15, self.space))
                elif event.dict["button"] == 3:
                    for obj in self.renders_objs:
                        if isinstance(obj, Ball):
                            print(obj.rect.colliderect(pygame.Rect(mouse[0]-20, mouse[1]-20, 40, 40)))
                            if obj.rect.colliderect(pygame.Rect(mouse[0] - obj.r, mouse[1] - obj.r, obj.r*2, obj.r*2)):


                                self.movement = True
                                self.moving_obj = obj
            if event.type == pygame.MOUSEBUTTONUP:
                if event.dict["button"] == 3:
                    self.movement = False
                    self.moving_obj = None
            if event.type == pygame.MOUSEMOTION and self.movement:
                dx, dy = event.pos[0] - self.move_old[0], event.pos[1] - self.move_old[1]
                dx *= 5
                dy *= 5
                self.move_old = event.pos
                new_pos = self.moving_obj.body.position[0] - dx, self.moving_obj.body.position[1] + dy
                query_info = self.space.point_query_nearest(new_pos, 0, pymunk.ShapeFilter())
                if query_info is None or query_info.shape in (self.moving_obj.shape, self.segment.shape):
                    self.moving_obj.body.position = new_pos
                    self.moving_obj.pos = new_pos
            self.move_old = mouse

    def reset_scene(self):
        # Reset the objects in the scene to their initial positions
        self.renders_objs = []
        self.move_old = (0, 0)
        self.movement = False
        self.space: pymunk.Space = pymunk.Space()
        self.space.gravity = 0, -1000
        self.space.damping = 0.5  # Set the friction coefficient of the space object
        self.pause = False
        self.segment = Segment((0, 100), (500, 50), 5, self.space, btype=pymunk.Body.KINEMATIC)
        self.renders_objs.append(self.segment)
        self.renders_objs.append(Segment((497, 300), (497, 50), 5, self.space, btype=pymunk.Body.KINEMATIC))
        self.renders_objs.append(Segment((0, 300), (0, 50), 5, self.space, btype=pymunk.Body.KINEMATIC))

    def update(self):
        if not self.pause:
            self.space.step(1 / self.fps)
        self.clean_up()


    def clean_up(self):
        for i in self.renders_objs:
            if not isinstance(i, Segment):
                if i.pos[0] < 0 or i.pos[0] > self.size_sc[0] or i.pos[1] < 0 or i.pos[1] > self.size_sc[1]:
                    del i

    def render(self, obj=None):
        self.display.fill((255, 255, 255))
        for obj in self.renders_objs:
            obj.render(self.display)
        #pygame.draw.rect(self.display, (25, 25, 25), pygame.Rect(self.move_old[0]-20, self.move_old[1]-20, 40, 40))