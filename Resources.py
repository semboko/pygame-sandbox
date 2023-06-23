self.scene.objects.remove(self.scene.floor)
self.scene.floor = Terrain(0, self.scene.display.get_width(), 100, 500, 400, self.scene.space)
self.scene.objects.append(self.scene.floor)

for x in range(100):
    xs = 700 + TerrainBlock.width * 2
    y = 152.98

    self.scene.floor.bricks.append(
        TerrainBlock(
            xs - xs % TerrainBlock.width - TerrainBlock.width * 3,
            y - y % TerrainBlock.height + TerrainBlock.width * x,
            self.scene.space,
            self.scene.floor.sf,
            Flatland,
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
