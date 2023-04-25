try:
    import cv2
except ImportError:
    import os
    os.system("pip install opencv-python")
    import cv2
from mods.basemod import *


class Animate(BaseMod):
    name = "Animate-for-sandbox"
    author = "Kolya142"

    @staticmethod
    def save_img(filename, data: list):
        cv2.imwrite(filename, data)

    @staticmethod
    def Video(filename, imgs: tuple, fps=60, size=(1500, 500), typew=cv2.VideoWriter_fourcc(*'DIVX')):
        out = cv2.VideoWriter(filename, typew, fps, size)
        for img in imgs:
            img1 = cv2.imread(img)
            out.write(img1)
        out.release()
