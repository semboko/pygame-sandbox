import os
import random
import time
from math import cos, sin
from turtle import Screen, Turtle, getcanvas, tracer

import keyboard
import pygame
from PIL import EpsImagePlugin, Image

rules = {"X": "F−[[X]+X]+F[+FX]−X", "F": "FF"}
axiom = "X"


def repl(l):
    if l in rules:
        return rules[l]
    return l


def get(iters: int = 7):
    s = axiom
    for i in range(iters):
        s = "".join(list(map(repl, s)))
    return s


pen = Turtle()
window = Screen()
plant = get(6)
# window.screensize(1000, 1000)
# window.setup(1000, 1000, 0, 0)
print(plant)
EpsImagePlugin.gs_windows_binary = "C:/Program Files/gs/gs10.01.1/bin/gswin64c.exe"
fc = 80
mfc = fc
run = True
mode = "fast"  # norm, fast


def save_as_png(canvas, fileName):
    fileName = "assets/plant/" + fileName
    canvas.postscript(file=fileName + ".eps")
    img = Image.open(fileName + ".eps")
    img = img.convert("RGBA")
    pixarr = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixarr[x, y] == (255, 255, 255, 255):
                pixarr[x, y] = (0, 0, 0, 0)
    # img = Image.fromarray(pixarr)
    img.save(fileName + ".png", "png")


clamp = lambda mn, v, mx: max(min(v, mx), mn)


def draw(recusion, pen, color):
    stack = []
    pen.color(color)
    for r in recusion:
        r1 = random.randint(0, 3000)
        if r1 < 3:
            pen.pensize(r1)
        if r == "[":
            stack.extend((pen.pos(), pen.heading()))
        if r == "]":
            pen.penup()
            pen.setheading(stack.pop())
            pen.setpos(stack.pop())
            pen.pendown()
        if r == "F":
            pen.forward(10)
        if r == "-":
            pen.left(random.randint(-10, 25))
        if r == "+":
            pen.right(random.randint(-10, 25))


while run:
    # https://www.shadertoy.com/view/dtt3WS
    # col.x = 0.2 + abs(0.3 + sin(x) - cos(x) + (0.01 * 21. * sin(x)));
    # col.y = 0.4 + cos(x) * sin(x) + (0.1 * cos(x));
    # col.z = 0.5 * sin(x) + (0.3 * cos(x));
    # col.x = pow(col.x,1. / 2.2);
    # col.y = pow(col.y,1. / 2.2);
    # col.z = pow(col.z,1. / 2.2);
    gamma = 1 / 2.2
    x = time.time()
    plantcolor = (
        clamp(0, int(abs(0.2 + abs(0.3 + sin(x) - cos(x) + (0.01 * 21.0 * sin(x))) ** gamma) * 1), 1),
        clamp(0, int(abs(0.4 + cos(x) * sin(x) + (0.1 * cos(x)) ** gamma) * 1), 1),
        clamp(0, int(abs(0.5 * sin(x) + (0.3 * cos(x)) ** gamma) * 1), 1),
    )
    pen.speed(0)
    tracer(0, 0)
    pen.penup()
    pen.setpos(0, -1000)
    pen.setheading(90)
    pen.pendown()
    draw(plant, pen, plantcolor)
    if mode == "fast":
        fc -= 1
        if fc == 0:
            run = False
        window.update()
        save_as_png(getcanvas(), f"plant-{mfc-fc}")
        print(f"generate plant {mfc-fc}-{mfc}")
        window.clear()
        continue
    while True:
        window.update()
        if not keyboard.is_pressed("r"):
            break
    while True:
        window.update()
        if keyboard.is_pressed("s"):
            save_as_png(getcanvas(), "plant")
        if keyboard.is_pressed("r"):
            window.clear()
            break
files = os.listdir(os.getcwd() + "assets/plant")
for file in files:
    if file.endswith(".eps"):
        os.remove(os.getcwd() + "assets/plant/" + file)
