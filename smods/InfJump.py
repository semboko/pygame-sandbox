import pygame

from mods.basemod import *
from scenes import VoxelWorld

class InfJump(BaseMod):

    name = "InfJump"
    author = "Kolya142"
    locked = False

    def start(self, *args, **kwargs):
        super(InfJump, self).start(*args, **kwargs)

    def handle_pressed_keys(self, keys: Sequence[bool]):
        if not self.locked:
            rc = self.scene.space.segment_query(self.scene.player.body.position,(self.scene.player.body.position.x,self.scene.player.body.position.y - 100), 0, self.scene.player.sf)
            if keys[pygame.K_SPACE] and not rc:
                self.scene.player.body.apply_impulse_at_local_point((0,400000),(0,0))