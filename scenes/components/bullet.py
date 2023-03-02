from scenes.components.ball import Ball
from pymunk import Space, ShapeFilter, Body
from pygame.surface import Surface


class Bullet(Ball):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._exploded = False

    def explode(self, space: Space):
        neighbors = space.point_query(self.body.position, 150, ShapeFilter())
        for neighbor in neighbors:
            if neighbor.shape.body.body_type != Body.DYNAMIC:
                continue
            neighbor.shape.body.apply_force_at_local_point((0, 30000000))
        self._exploded = True
        self.remove(space)

    def is_outside(self, display: Surface) -> bool:
        x, y = self.body.position
        if y < 0 or x < 0 or x > display.get_width():
            return True
        return False

    def remove(self, space: Space) -> None:
        space.remove(self.body, self.shape)
        print("Bullet is removed from space")

    def ready_to_explode(self, space: Space):
        if self._exploded:
            return False
        collides_with = space.shape_query(self.shape)
        if not collides_with:
            return False
        return True
