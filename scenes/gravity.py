from logging import getLogger
from typing import Tuple

import pygame.draw
import pymunk
from pygame.event import Event

from scenes.abstract import AbstractScene
from scenes.components import Ball, Segment
from scenes.components.pj import PJ

from .utils import convert

log = getLogger()


class GravityScene(AbstractScene):
    space: pymunk.Space
    circle: Ball
    segment: Segment
    pause: bool
    renders_objs: list
    move_old: tuple
    movement: bool
    co1: Ball
    co2: Ball
    mode: bool

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.reset_scene()

    def handle_event(self, event: Event) -> None:
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
                if not self.mode:
                    self.renders_objs.append(Ball(*convert(event.pos, self.size_sc[1]), 15, self.space))
                else:
                    self.co1 = pymunk.Vec2d(*event.pos)
            if event.dict["button"] == 2:
                for obj in self.renders_objs:
                    if isinstance(obj, Ball):
                        if obj.body.position.get_distance(convert(event.pos, self.size_sc[1])) <= obj.shape.radius:
                            self.co1 = obj
            if event.dict["button"] == 4:
                self.mode = False
            if event.dict["button"] == 5:
                self.mode = True
            # elif event.dict["button"] == 3:
            # for obj in self.renders_objs:
            #     if isinstance(obj, Ball):
            #         print(obj.rect.colliderect(pygame.Rect(mouse[0] - 20, mouse[1] - 20, 40, 40)))
            #         if obj.rect.colliderect(
            #             pygame.Rect(mouse[0] - obj.r, mouse[1] - obj.r, obj.r * 2, obj.r * 2)
            #         ):
            #             self.movement = True
            #             self.moving_obj = obj
            #             obj.body.position = convert(mouse, self.display.get_height())
        # if event.type == pygame.MOUSEBUTTONUP:
        #     if event.dict["button"] == 3:
        #         self.movement = False
        #         self.moving_obj = None
        # if event.type == pygame.MOUSEMOTION and self.movement:
        #     dx, dy = event.pos[0] - self.move_old[0], event.pos[1] - self.move_old[1]
        #     dx *= 5
        #     dy *= 5
        #     self.move_old = event.pos
        #     new_pos = self.moving_obj.body.position[0] - dx, self.moving_obj.body.position[1] + dy
        #     query_info = self.space.point_query_nearest(new_pos, 0, pymunk.ShapeFilter())
        #     if query_info is None or query_info.shape in (self.moving_obj.shape, self.segment.shape):
        #         self.moving_obj.body.position = new_pos
        #         self.moving_obj.pos = new_pos
        #     self.move_old = mouse

        if event.type == pygame.MOUSEBUTTONUP:
            if event.dict["button"] == 1:
                if self.mode:
                    self.co2 = pymunk.Vec2d(*event.pos)
                    seg = Segment(
                        convert(self.co1, self.size_sc[1]),
                        convert(self.co2, self.size_sc[1]),
                        5,
                        self.space,
                        btype=pymunk.Body.KINEMATIC,
                    )
                    # self.space.add(seg.body, seg.shape)
                    self.renders_objs.append(seg)
            if event.dict["button"] == 2:
                self.co2 = None
                for obj in self.renders_objs:
                    if isinstance(obj, Ball):
                        if obj.body.position.get_distance(convert(event.pos, self.size_sc[1])) <= obj.shape.radius:
                            if event.dict["button"] == 2:
                                self.co2 = obj
                                break
                if self.co2 and self.co1 and self.co1 != self.co2:
                    join = pymunk.DampedSpring(
                        self.co1.body,
                        self.co2.body,
                        (0, 0),
                        (0, 0),
                        self.co1.body.position.get_distance(self.co2.body.position) / 10,
                        600,
                        0.3,
                    )
                    self.renders_objs.append(PJ(join))
                    self.space.add(join)

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
        self.co2 = None
        self.co1 = None
        self.mode = False
        self.renders_objs.append(self.segment)
        self.renders_objs.append(Segment((497, 300), (497, 50), 5, self.space, btype=pymunk.Body.KINEMATIC))
        self.renders_objs.append(Segment((0, 300), (0, 50), 5, self.space, btype=pymunk.Body.KINEMATIC))

    def update(self):
        if not self.pause:
            self.space.step(1 / self.fps)
        # self.clean_up()

    def clean_up(self):
        for i in self.renders_objs:
            if not isinstance(i, Segment):
                if i.pos[0] < 0 or i.pos[0] > self.size_sc[0] or i.pos[1] < 0 or i.pos[1] > self.size_sc[1]:
                    del i

    def render(self, obj=None):
        self.display.fill((255, 255, 255))
        for obj in self.renders_objs:
            obj.render(self.display, pymunk.vec2d.Vec2d(0, 0))
