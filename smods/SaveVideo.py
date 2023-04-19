import pygame
import os
from mods.basemod import *

class SaveVideo(BaseMod):

    name = "SaveVideo"
    author = "Kolya142"
    nam = 0
    on = False

    def start(self, *args, **kwargs):
        super(SaveVideo, self).start(*args, **kwargs)

    def onrender(self):
        if self.on:
            view = pygame.surfarray.array3d(self.disp)
            view = view.transpose([1,0,2])
            view = cv2.cvtColor(view,cv2.COLOR_RGB2BGR)
            self.get_mod("Animate-for-sandbox").save_img(f"user_data/Save_video/img{self.nam}.jpg", view)
            self.nam += 1

    def handle_pressed_keys(self, keys: Sequence[bool]):
        if keys[pygame.K_KP0]:
            self.on = True

    def quit(self, error: str = None):
        if self.on:
            font = pygame.font.SysFont("Comic Sans MS",30)
            text = f"saving video, please wait"
            self.disp.blit(font.render(text,True,(0,0,0)),(self.scene.size_sc[0]//2, self.scene.size_sc[1]//2))
            pygame.display.update()
            imgs = []
            for i in range(self.nam):
                imgs.append(f"user_data/Save_video/img{i}.jpg")
            self.get_mod("Animate-for-sandbox").Video(f"user_data/Save_video/save{type(self.scene).__name__}({self.nam}).mp4", imgs, typew = cv2.VideoWriter_fourcc(*'mp4v'))