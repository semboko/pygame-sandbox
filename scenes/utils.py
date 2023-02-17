from typing import Tuple

import pymunk.vec2d


def convert(vector: pymunk.vec2d, screen_h: int) -> Tuple[int, int]:
    x, y = vector
    return int(x), screen_h - int(y)
