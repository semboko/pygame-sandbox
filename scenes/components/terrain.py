import random
from typing import Tuple

import pymunk

from scenes.components.segment import Segment
from pymunk import Space, Body
from pygame.surface import Surface
from scenes.components.rect import Rect

class TerrainBlock(Rect):

    width: int = 25
    height: int = 25

    def __init__(self, x: int, y: int, space: pymunk.Space, sf) :
        super().__init__(x, y, self.width, self.height, space, (25,255,25))
        self.body.body_type = Body.STATIC
        self.shape.filter = sf
def max_nfs(noise, y_top, y_min, y_max):
    if noise < .4 and y_top < y_max :
        y_top += random.randint(1,6) * TerrainBlock.height
    elif noise < .5 and y_top < y_max :
        y_top += random.randint(1,3) * TerrainBlock.height
    elif noise==.5 :
        y_top = y_top
    elif noise > .5 and y_top > y_min :
        y_top -= random.randint(1,4) * TerrainBlock.height
    elif noise > .6 and y_top > y_max :
        y_top -= random.randint(1,7) * TerrainBlock.height
    return y_top
def nfs(noise, y_top, y_min, y_max):
    if noise < .3 and y_top < y_max :
        y_top += random.randint(1,3) * TerrainBlock.height
    elif noise < .5 and y_top < y_max :
        y_top += random.randint(1,2) * TerrainBlock.height
    elif noise==.5 :
        y_top = y_top
    elif noise > .5 and y_top > y_min :
        y_top -= random.randint(1,2) * TerrainBlock.height
    elif noise > .9 and y_top > y_max :
        y_top -= random.randint(1,3) * TerrainBlock.height
    return y_top
def min_nfs(noise, y_top, y_min, y_max):
    if noise < .01 and y_top < y_max :
        y_top += random.randint(1,3) * TerrainBlock.height
    elif noise < .5 and y_top < y_max :
        y_top += random.randint(1,2) * TerrainBlock.height
    elif noise==.5 :
        y_top = y_top
    elif noise > .5 and y_top > y_min :
        y_top -= random.randint(1,2) * TerrainBlock.height
    elif noise > .99 and y_top > y_max :
        y_top -= random.randint(1,3) * TerrainBlock.height
    return y_top
def micro_nfs(noise, y_top, y_min, y_max):
    if noise < .000000001 and y_top < y_max :
        y_top += random.randint(1,3) * TerrainBlock.height
    elif noise < .1 and y_top < y_max :
        y_top += random.randint(1,2) * TerrainBlock.height
    elif noise==.5 :
        y_top = y_top
    elif noise > .9 and y_top > y_min :
        y_top -= random.randint(1,2) * TerrainBlock.height
    elif noise > .999999 and y_top > y_max :
        y_top -= random.randint(1,3) * TerrainBlock.height
    return y_top
class Terrain:
    def __init__(self, x_min: int, x_max: int, y_min: int, y_max: int, steps: int, seed: str, space: Space, noise_filter = nfs):
        self.space = space
        self.sf = pymunk.ShapeFilter(group=0b10)
        # self.segments = []
        self.seed = seed
        self.bricks = []
        self.x_max, self.x_min, self.y_max, self.y_min = x_max, x_min, y_max, y_min
        self.abs_min_y = -10
        random.seed(seed)
        y_top = y_min
        for x_start in range(x_min, x_max, TerrainBlock.width):
            x = x_start + TerrainBlock.width//2
            noise = random.random()
            y_top = noise_filter(noise, y_top, y_min, y_max)

            for y_start in range(y_top,  self.abs_min_y, -TerrainBlock.height):
                y = y_start - TerrainBlock.height//2
                brick = TerrainBlock(x, y, space, self.sf)
                self.bricks.append(brick)
        # self.seg_width = (x_max - x_min)//steps
        # for x in range(x_min, x_max, self.seg_width):
        #     p1 = self.segments[-1].shape.b if self.segments else (x, random.randint(y_min, y_max))
        #     p2 = (p1[0] + self.seg_width, random.randint(y_min, y_max))
        #     self.segments.append(self.create_segment(p1, p2))
        self.nfs_name = noise_filter.__name__
        self.nfs_func = noise_filter

    def update(self, x_shift: float) -> None:
        # left_x = self.segments[0].shape.a[0]
        # right_x = self.segments[-1].shape.b[0]
        # shift_x = x_shift
        # if shift_x + 50 < left_x:
        #     b = self.segments[0].shape.a
        #     a = pymunk.Vec2d(b.x - self.seg_width, random.randint(self.y_min, self.y_max))
        #     self.segments.insert(0, self.create_segment(a, b))
        #     self.space.remove(self.segments[-1].body, self.segments[-1].shape)
        #     del (self.segments[-1])
        # if shift_x > right_x - 1000:
        #     a = self.segments[-1].shape.b
        #     b = pymunk.Vec2d(a.x + self.seg_width, random.randint(self.y_min, self.y_max))
        #     self.segments.append(self.create_segment(a, b))
        #     self.space.remove(self.segments[0].body, self.segments[0].shape)
        #     del (self.segments[0])
        ###################################################################################
        ###################################################################################
        # self.x_max,self.x_min,self.y_max,self.y_min = x_max,x_min,y_max,y_min
        # self.abs_min_y = -5
        # random.seed(seed)
        # y_top = y_min
        # for x_start in range(x_min,x_max,TerrainBlock.width) :
        #     x = x_start + TerrainBlock.width // 2
        #     noise = random.random()
        #     y_top = noise_filter(noise,y_top,y_min,y_max)
        #
        #     for y_start in range(y_top,self.abs_min_y,-TerrainBlock.height) :
        #         y = y_start - TerrainBlock.height // 2
        #         brick = TerrainBlock(x,y,space,self.sf)
        #         self.bricks.append(brick)
        if x_shift < self.bricks[0].body.position.x:
            x = self.bricks[0].body.position.x - TerrainBlock.width // 2 - TerrainBlock.width // 2
            noise = int(random.random())
            y_top = self.nfs_func(noise,self.y_min,self.y_min,self.y_max * 20)

            for y_start in range(y_top,self.abs_min_y,-TerrainBlock.height) :
                y = y_start - TerrainBlock.height // 2
                brick = TerrainBlock(x,y,self.space,self.sf)
                self.bricks.insert(0, brick)
                self.space.remove(self.bricks[-1].shape,self.bricks[-1].body)
                del (self.bricks[-1])

        # bugs: in ~5971.52+ x coord generation stopped
        if x_shift + 700 > self.bricks[0].body.position.x:
            x = self.bricks[-1].body.position.x + TerrainBlock.width // 2
            noise = int(random.random())
            y_top = self.nfs_func(noise,self.y_min,self.y_min,self.y_max * 20)

            for y_start in range(y_top,self.abs_min_y,-TerrainBlock.height) :
                y = y_start - TerrainBlock.height // 2
                brick = TerrainBlock(x,y,self.space,self.sf)
                self.bricks.insert(0, brick)
                self.space.remove(self.bricks[0].shape,self.bricks[0].body)
                del (self.bricks[0])
    def render(self, display: Surface, camera_shift: pymunk.Vec2d) -> None:
        for s in self.bricks:
            s.render(display, camera_shift)
