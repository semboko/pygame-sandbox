from typing import Tuple

import pygame
import pymunk


class Animator:
    frames = []
    frame = 0

    def next_frame(self, pos=None, angle=None, *, frame=None):
        if self.frame == len(self.frames):
            self.frame = 0
        if frame:
            self.frame = frame
        frame = self.frames[self.frame]
        posses = []
        angles = []
        if "pos" in frame and pos:
            p = frame["pos"]
            oldp = pos
            for i in range(0, 10):
                k = i / 100
                x = (oldp[0] * (1 - k)) + (p[0] * k)
                y = (oldp[1] * (1 - k)) + (p[1] * k)
                oldp = (x, y)
                posses.append(oldp)

        if "angle" in frame and angle:
            p = frame["angle"]
            oldp = angle
            for i in range(0, 10):
                k = i / 100
                oldp = (oldp * (1 - k)) + (p * k)
                angles.append(oldp)

        self.frame += 1
        return posses, angles
