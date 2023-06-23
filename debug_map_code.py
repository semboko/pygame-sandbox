import pymunk

self.scene.objects.remove(self.scene.floor)
self.scene.floor = Terrain(0, self.scene.display.get_width(), 100, 500, 400, self.scene.space)
self.scene.objects.append(self.scene.floor)

for x in range(20):
    res1 = Stone()
    res2 = Wood()
    res3 = Ice()
    res1.materialize(pymunk.Vec2d(78.91, 109.04 + x), self.scene.space)
    res2.materialize(pymunk.Vec2d(171.51, 109.69 + x), self.scene.space)
    res3.materialize(pymunk.Vec2d(268.06, 110.21 + x), self.scene.space)
    self.scene.objects.extend((res1, res2, res3))
    xs = 1210.88 + TerrainBlock.width * 2
    y = 112.98
    self.scene.floor.bricks.append(
        TerrainBlock(
            xs - xs % TerrainBlock.width - TerrainBlock.width * 1,
            y - y % TerrainBlock.height + TerrainBlock.width * x,
            self.scene.space,
            self.scene.floor.sf,
            Swamp,
        )
    )

    self.scene.floor.bricks.append(
        TerrainBlock(
            xs - xs % TerrainBlock.width - TerrainBlock.width * 2,
            y - y % TerrainBlock.height + TerrainBlock.width * x,
            self.scene.space,
            self.scene.floor.sf,
            Mountain,
        )
    )

    self.scene.floor.bricks.append(
        TerrainBlock(
            xs - xs % TerrainBlock.width - TerrainBlock.width * 3,
            y - y % TerrainBlock.height + TerrainBlock.width * x,
            self.scene.space,
            self.scene.floor.sf,
            Flatland,
        )
    )


def udm(cms_mod):
    # cms_mod.get_mod("AudioLoadLib").play("DebugMod", "jump.wav", 1)
    cms_mod.get_mod("InfJump").locked = False
    cms_mod.updates = []


self.updates = [udm]

# 285.02, 297.9
