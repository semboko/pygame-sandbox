from scenes.components.rect import Rect


class Player(Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = 1

    def move(self, direction: int):
        self.body.apply_impulse_at_local_point((direction * 20_000, 0), (0, 0))
        self.direction = direction

    def jump(self):
        self.body.apply_impulse_at_local_point((0, 700000), (0, 0))
