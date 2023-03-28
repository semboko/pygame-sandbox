import random
from typing import Tuple

import pymunk

from scenes.components.segment import Segment
from pymunk import Space, Body
from pygame.surface import Surface
from scenes.components.rect import Rect

from noise.perlin import SimplexNoise


class TerrainBlock(Rect):
    width: int = 25
    height: int = 25

    def __init__(self, x: float, y: float, space: pymunk.Space, sf):
        super().__init__(x, y, self.width, self.height, space, (25, 255, 25))
        self.body.body_type = Body.STATIC
        self.shape.filter = sf


def max_nfs(noise, y_top, y_min, y_max):
    if noise < 0.4 and y_top < y_max:
        y_top += random.randint(1, 6) * TerrainBlock.height
    elif noise < 0.5 and y_top < y_max:
        y_top += random.randint(1, 3) * TerrainBlock.height
    elif noise == 0.5:
        y_top = y_top
    elif noise > 0.5 and y_top > y_min:
        y_top -= random.randint(1, 4) * TerrainBlock.height
    elif noise > 0.6 and y_top > y_max:
        y_top -= random.randint(1, 7) * TerrainBlock.height
    return y_top


def nfs(noise, y_top, y_min, y_max):
    if noise < 0.3 and y_top < y_max:
        y_top += random.randint(1, 3) * TerrainBlock.height
    elif noise < 0.5 and y_top < y_max:
        y_top += random.randint(1, 2) * TerrainBlock.height
    elif noise == 0.5:
        y_top = y_top
    elif noise > 0.5 and y_top > y_min:
        y_top -= random.randint(1, 2) * TerrainBlock.height
    elif noise > 0.9 and y_top > y_max:
        y_top -= random.randint(1, 3) * TerrainBlock.height
    return y_top


def min_nfs(noise, y_top, y_min, y_max):
    if noise < 0.01 and y_top < y_max:
        y_top += random.randint(1, 3) * TerrainBlock.height
    elif noise < 0.5 and y_top < y_max:
        y_top += random.randint(1, 2) * TerrainBlock.height
    elif noise == 0.5:
        y_top = y_top
    elif noise > 0.5 and y_top > y_min:
        y_top -= random.randint(1, 2) * TerrainBlock.height
    elif noise > 0.99 and y_top > y_max:
        y_top -= random.randint(1, 3) * TerrainBlock.height
    return y_top


def micro_nfs(noise, y_top, y_min, y_max):
    if noise < 0.000000001 and y_top < y_max:
        y_top += random.randint(1, 3) * TerrainBlock.height
    elif noise < 0.1 and y_top < y_max:
        y_top += random.randint(1, 2) * TerrainBlock.height
    elif noise == 0.5:
        y_top = y_top
    elif noise > 0.9 and y_top > y_min:
        y_top -= random.randint(1, 2) * TerrainBlock.height
    elif noise > 0.999999 and y_top > y_max:
        y_top -= random.randint(1, 3) * TerrainBlock.height
    return y_top


class Terrain:
    def __init__(
        self, x_min: int, x_max: int, y_min: int, y_max: int, steps: int, space: Space
    ):
        self.space = space
        self.noise = SimplexNoise()
        self.sf = pymunk.ShapeFilter(group=0b10)
        self.bricks = []
        self.x_max, self.x_min, self.y_max, self.y_min = x_max, x_min, y_max, y_min
        self.abs_min_y = -10

        for x in range(x_min, x_max, TerrainBlock.width):
            self.bricks.append(TerrainBlock(x, self.get_y(x), space, self.sf))

    def get_y(self, x: float) -> float:
        return self.y_min + (self.y_max - self.y_min) * self.noise.noise2(x/700, 0)

    def get_color(self, o, n):
        value = (n - self.y_min) / self.y_max
        # if o in [(128,198,57), (227,242,239)]:
        #    return (90,77,65)
        if value <= 0.1:
            if not o in [(25, 25, 255), (90, 77, 65)]:
                n = random.random()
                if o != (0, 0, 0):
                    return (90, 77, 65)
                if n < 0.5:
                    return (25, 25, 255)
                else:
                    return (90, 77, 65)
            return o
        if value <= 0.2:
            if o == (0, 0, 0):
                return (221, 221, 48)
            else:
                return (90, 77, 65)
        if value <= 0.85:
            return (128, 198, 57)
        else:
            return (227, 242, 239)

    def update(self, x_shift: float) -> None:
        lb = self.bricks[0]
        rb = self.bricks[-1]

        lbx = lb.body.position.x
        if x_shift + 50 < lbx:
            self.bricks.insert(0, TerrainBlock(lbx - TerrainBlock.width, self.get_y(lbx), self.space, self.sf))

        rbx = rb.body.position.x
        if x_shift > rbx - 1000:
            self.bricks.append(TerrainBlock(rbx + TerrainBlock.width, self.get_y(rbx), self.space, self.sf))

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        for s in self.bricks:
            s.render(display, camera_shift)
