import pymunk.vec2d
from typing import Tuple

def convert(vector: pymunk.vec2d, screen_h: int) -> Tuple[int, int]:
    x, y = vector
    return int(x), screen_h-int(y)