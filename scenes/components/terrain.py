import random
from typing import Tuple, Optional

import pygame
import pymunk

from scenes.components.biomes import BaseBiome, Flatland, Mine, Swamp, Mountain
from pymunk import Space, Body
from pygame.surface import Surface
from scenes.components.rect import Rect
from scenes.components.resources import BaseResource
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

    @staticmethod
    def get_resources() -> Tuple[BaseResource]:
        return (BaseResource(), )

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
        self.sf = pymunk.ShapeFilter(group=0b0010, categories = 0b1101)
        self.bricks = []
        self.x_max, self.x_min, self.y_max, self.y_min = x_max, x_min, y_max, y_min
        self.abs_min_y = -300

        for x in range(x_min, x_max, TerrainBlock.width):
            y_top = int(self.get_y(x))
            for y_start in range(y_top,self.abs_min_y,-TerrainBlock.height) :
                block = self.get_block(x, y_start)
                if y_start != y_top:
                    block.biome.image = pygame.image.load("assets/stone1.png")
                self.bricks.append(block)

    def get_noise(self, x: float) -> float:
        return self.noise.noise2(x/700, 0)

    def get_block(self, x: int, y: int = None) -> TerrainBlock:
        if not y:
            noise_value = self.get_noise(x)
            biome = self.get_biome(noise_value)
            y = self.get_y(x)
        else:
            biome = self.get_biome(y)
        block = TerrainBlock(x, y, self.space, self.sf, biome)
        return block

    def get_y(self, x: float) -> float:
        y = self.y_min + (self.y_max - self.y_min) * self.get_noise(x)
        return y - y % TerrainBlock.height

    def get_biome(self, noise_value: float) -> BaseBiome:
        if noise_value > 0.8:
            return Mountain()
        elif noise_value < -0.8:
            return Swamp()
        else:
            return Flatland()

    def get_brick_by_body(self, body: Body) -> Optional[TerrainBlock]:
        for b in self.bricks:
            if b.body == body:
                return b

    def delete_block(self, brick: TerrainBlock) -> None:
        self.bricks.remove(brick)
        self.space.remove(brick.body, brick.shape)

    def update(self, x_shift: float) -> None:
        lb = self.bricks[0]
        rb = self.bricks[-1]

        lbx = lb.body.position.x
        if x_shift + 50 < lbx:
            y_top = int(self.get_y(lbx - TerrainBlock.width))
            for y_start in range(y_top, self.abs_min_y, -TerrainBlock.height) :
                block = self.get_block(lbx - TerrainBlock.width, y_start)
                if y_start != y_top:
                    block.biome.image = pygame.image.load("assets/stone1.png")
                self.bricks.insert(0, block)

        rbx = rb.body.position.x
        if x_shift > rbx - 1000:
            y_top = int(self.get_y(rbx + TerrainBlock.width))
            for y_start in range(y_top,self.abs_min_y,-TerrainBlock.height) :
                block = self.get_block(rbx + TerrainBlock.width, y_start)
                if y_start != y_top:
                    block.biome.image = pygame.image.load("assets/stone1.png")
                self.bricks.append(block)

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:

        for s in self.bricks:
            s.render(display, camera_shift)
