import random
from typing import Tuple

import pygame
import pymunk

from scenes.components.biomes import BaseBiome, Flatland, Mine, Swamp, Mountain
from pymunk import Space, Body
from pygame.surface import Surface
from scenes.components.rect import Rect
from scenes.utils import convert

from noise.perlin import SimplexNoise


class TerrainBlock(Rect):
    width: int = 25
    height: int = 25

    biome: BaseBiome

    def __init__(self, x: float, y: float, space: pymunk.Space, sf: pymunk.ShapeFilter, biome: BaseBiome = Flatland):
        super().__init__(x, y, self.width, self.height, space, (25, 255, 25))
        self.body.body_type = Body.STATIC
        self.shape.filter = sf
        self.biome = biome

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        h = display.get_height()
        adj = pymunk.Vec2d(self.width/2, -self.height/2)
        pos = self.body.position - adj - camera_shift

        display.blit(self.biome.image, convert(pos, h))


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
            self.bricks.append(self.get_block(x))

    def get_noise(self, x: float) -> float:
        return self.noise.noise2(x/700, 0)

    def get_block(self, x: int) -> TerrainBlock:
        noise_value = self.get_noise(x)
        biome = self.get_biome(noise_value)
        block = TerrainBlock(x, self.get_y(x), self.space, self.sf, biome)
        return block

    def get_y(self, x: float) -> float:
        return self.y_min + (self.y_max - self.y_min) * self.get_noise(x)

    def get_biome(self, noise_value: float) -> BaseBiome:
        if noise_value > 0.8:
            return Mountain()
        elif noise_value < -0.8:
            return Swamp()
        else:
            return Flatland()

    def update(self, x_shift: float) -> None:
        lb = self.bricks[0]
        rb = self.bricks[-1]

        lbx = lb.body.position.x
        if x_shift + 50 < lbx:
            self.bricks.insert(0, self.get_block(lbx - TerrainBlock.width))

        rbx = rb.body.position.x
        if x_shift > rbx - 1000:
            self.bricks.append(self.get_block(rbx + TerrainBlock.width))

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        for s in self.bricks:
            s.render(display, camera_shift)
