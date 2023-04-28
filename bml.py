def ddd(cms_mod):
    if cms_mod.scene.player.body.position.y < 40:
        cms_mod.pop("main.json")

self.updates = [ddd]
