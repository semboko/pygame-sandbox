import os
import random
from typing import Optional, Tuple, List

import pygame
import pymunk
from vnoise import Noise
from pygame.surface import Surface
from pymunk import Body, Space

from scenes.components.biomes import BaseBiome, Flatland, Mountain, Swamp
from scenes.components.rect import Rect
from scenes.components.resources import BaseResource
from scenes.components.sprite import Sprite
from scenes.utils import convert

tree_imgs: List[Surface] = []
tree_folder = os.getcwd() + "/assets/tree/"
for i, tree_img in enumerate(os.listdir(tree_folder)):
    tree_imgs.append(pygame.image.load(tree_folder + tree_img))
    tree_imgs[i] = pygame.transform.scale(tree_imgs[i], (460, 500))

plant_imgs: List[Surface] = []
plant_folder = os.getcwd() + "/assets/plant/"
for i, plant_img in enumerate(os.listdir(plant_folder)):
    plant_imgs.append(pygame.image.load(plant_folder + plant_img))
    plant_imgs[i] = pygame.transform.scale(plant_imgs[i], (70, 40))


class TerrainBlock(Rect):
    width: int = 25
    height: int = 25
    underlying_block_height: int = 200

    biome: BaseBiome

    def __init__(self, x: float, y: float, space: pymunk.Space, sf: pymunk.ShapeFilter, biome: BaseBiome = Flatland):
        super().__init__(x, y, self.width, self.height, space, (25, 255, 25))
        self.body.body_type = Body.STATIC
        self.shape.filter = sf
        self.biome = biome
        self.underlying_block: Optional[Rect] = None
        self.space = space
        self.topobjs: List[Sprite] = []

    def set_underlying_block(self) -> None:
        x, top_block_y = self.body.position
        top_y = top_block_y - self.width / 2
        bottom_y = top_y - self.underlying_block_height
        y = (top_y + bottom_y) / 2
        self.underlying_block = Rect(x, y, self.width, self.underlying_block_height, self.space)
        self.underlying_block.body.body_type = Body.STATIC

    def add_top_object(self, obj):
        self.topobjs.append(obj)

    def save(self):
        return self.body.position, self.biome.name

    def get_resources(self) -> Tuple[BaseResource]:
        result = []
        for res, quantity in self.biome.resources.items():
            for i in range(quantity):
                result.append(res())
        self.topobjs = []
        return tuple(result)

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        h = display.get_height()
        adj = pymunk.Vec2d(self.width / 2, -self.height / 2)
        pos = self.body.position - adj - camera_shift

        display.blit(self.biome.image, convert(pos, h))

        if self.underlying_block:
            self.underlying_block.render(display, camera_shift)

        for obj in self.topobjs:
            obj.render(display, camera_shift)


class FalseTerrain:
    def __init__(self, *args, **kwargs):
        pass

    def get_noise(self, *args, **kwargs):
        pass

    def get_block(self, *args, **kwargs):
        pass

    def get_y(self, *args, **kwargs):
        pass

    def get_biome(self, *args, **kwargs):
        pass

    def get_brick_by_body(self, *args, **kwargs):
        pass

    def delete_block(self, *args, **kwargs):
        pass

    def load(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        pass


class Terrain:
    def __init__(self, x_min: int, x_max: int, y_min: int, y_max: int, steps: int, space: Space):
        self.space = space
        self.noise = Noise()
        self.seed = int(random.uniform(1000, 100_000))
        self.noise.seed(self.seed)
        self.sf = pymunk.ShapeFilter(group=0b0010, categories=0b1101)
        self.objects = []
        self.bricks = []
        self.x_max, self.x_min, self.y_max, self.y_min = x_max, x_min, y_max, y_min
        self.abs_min_y = -300

        for x in range(x_min, x_max, TerrainBlock.width):
            y_top = int(self.get_y(x))
            block = self.get_block(x, y_top)
            self.bricks.append(block)

    def get_noise(self, x: float, noise=560) -> float:
        return self.noise.noise1(x / noise * 1.1, 1, 2, 190)

    def get_block(self, x: int, y: int = None) -> TerrainBlock:
        if not y:
            noise_value = self.get_noise(x)
            biome = self.get_biome(noise_value)
            y = self.get_y(x)
        else:
            biome = self.get_biome(y)
        block = TerrainBlock(x, y, self.space, self.sf, biome)
        if len(self.space.point_query((x, y), 1, pymunk.ShapeFilter())) > 1:
            block.body.body_type = pymunk.Body.STATIC
        block.set_underlying_block()
        nv = abs(self.get_noise(x, 650))
        nv1 = abs(self.get_noise(x + TerrainBlock.width, 650))
        sprite = Sprite()
        if 0.5 < nv < 0.8:
            sprite.add_sprite("flower", "assets/flower.png")
            sprite.active_sprite = "flower"
            sprite.pos = convert((x, y + 50), 500)
            block.add_top_object(sprite)
        elif 0.4 < nv < 0.6:
            sprite.add_sprite("rock", "assets/rock.png")
            sprite.active_sprite = "rock"
            sprite.pos = convert((x - 10, y + 20), 500)
            block.add_top_object(sprite)
        if 0.4 < nv < 0.6 and not 0.4 < nv1 < 0.6 and not nv - 0.1 < nv1 < nv + 0.1:
            sprite.imgs["tree"] = tree_imgs[int(nv * (len(tree_imgs) - 1))]
            sprite.active_sprite = "tree"
            sprite.pos = (
                x - sprite.imgs["tree"].get_width() / 2,
                (500 - block.body.position.y) - sprite.imgs["tree"].get_height(),
            )
            block.add_top_object(sprite)
        if 0.4 < nv:
            sprite.imgs["plant"] = plant_imgs[int(nv * (len(plant_imgs) - 1))]
            sprite.active_sprite = "plant"
            sprite.pos = (
                x - sprite.imgs["plant"].get_width() / 2,
                (500 - block.body.position.y) - sprite.imgs["plant"].get_height(),
            )
            block.add_top_object(sprite)
        return block

    def get_y(self, x: float) -> float:
        y = self.y_min + (self.y_max - self.y_min) * self.get_noise(x)
        return y - y % TerrainBlock.height

    def get_biome(self, noise_value: float) -> BaseBiome:
        if noise_value > 0.8:
            return Mountain()
        elif noise_value < -90:
            return Swamp()
        else:
            return Flatland()

    def get_brick_by_body(self, body: Body) -> Optional[TerrainBlock]:
        for b in self.bricks:
            if b.body == body:
                return b

    def delete_block(self, brick: TerrainBlock, *, full=False) -> None:
        old_x, old_y = brick.body.position
        if old_y > self.get_y(old_x) or full:
            self.space.remove(brick.body, brick.shape)
            self.bricks.remove(brick)
            return
        brick_idx = self.bricks.index(brick)
        self.space.remove(brick.body, brick.shape, brick.underlying_block.body, brick.underlying_block.shape)
        # new_brick = self.get_block(old_x, old_y - brick.height)
        # self.bricks[brick_idx] = new_brick

    def load(self, data: List[Tuple[pymunk.Vec2d, str]]):
        for brick in self.bricks:
            if brick is None:
                continue
            self.space.remove(brick.body, brick.shape)
            if brick.underlying_block is not None:
                self.space.remove(brick.underlying_block.body, brick.underlying_block.shape)
        self.bricks = []
        for d in data:
            name = d[1]
            pos = d[0]
            if name == "Flatland":
                bl = TerrainBlock(pos.x, pos.y, self.space, self.sf, Flatland)
                bl.set_underlying_block()
                self.bricks.append(bl)
            elif name == "Mountain":
                bl = TerrainBlock(pos.x, pos.y, self.space, self.sf, Mountain)
                bl.set_underlying_block()
                self.bricks.append(bl)
            elif name == "Swamp":
                bl = TerrainBlock(pos.x, pos.y, self.space, self.sf, Swamp)
                bl.set_underlying_block()
                self.bricks.append(bl)

    def update(self, x_shift: float) -> None:
        lb = self.bricks[0]
        rb = self.bricks[-1]

        lbx = lb.body.position.x
        if x_shift - 50 < lbx:
            self.delete_block(rb, full=True)
            y_top = int(self.get_y(lbx - TerrainBlock.width))
            block = self.get_block(lbx - TerrainBlock.width, y_top)
            self.bricks.insert(0, block)
            return

        rbx = rb.body.position.x
        if x_shift > rbx - 1505:
            self.delete_block(lb, full=True)
            y_top = int(self.get_y(rbx + TerrainBlock.width))
            block = self.get_block(rbx + TerrainBlock.width, y_top)
            self.bricks.append(block)

    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        for s in self.bricks:
            s.render(display, camera_shift)
        for o in self.objects:
            o.render(display, camera_shift)
        # for i in range(self.x_min, self.x_max):
        #     col = max(min(int(self.get_noise(i) * 255), 255), 0)
        #     pygame.draw.rect(display, (col, col, col), (i-camera_shift.x, 500-self.get_noise(i)*(self.y_max-self.y_min)+camera_shift.y, 1, 1))
