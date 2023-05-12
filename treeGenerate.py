import random
import time

import pygame
from PIL import Image, EpsImagePlugin
from turtle import Turtle, Screen, tracer, getcanvas
from math import sin, cos
import os
import keyboard

rules = {"1": "21", "0": "1[0]0"}
axiom = "3333333330"

def repl(l):
    if l in rules:
        return rules[l]
    return l

def get(iters: int = 7):
    s = axiom
    for i in range(iters):
        s = ''.join(list(map(repl, s)))
    return s

pen = Turtle()
window = Screen()
tree = get(10)
# window.screensize(1000, 1000)
# window.setup(1000, 1000, 0, 0)
print(tree)
EpsImagePlugin.gs_windows_binary = "C:/Program Files/gs/gs10.01.1/bin/gswin64c.exe"
fc = 80
mfc = fc
run = True
mode = "fast" # norm, fast
def save_as_png(canvas,fileName):
    fileName = "assets/tree/" + fileName
    canvas.postscript(file = fileName + '.eps')
    img = Image.open(fileName + '.eps')
    img = img.convert("RGBA")
    pixarr = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixarr[x, y] == (255, 255, 255, 255):
                pixarr[x, y] = (0, 0, 0, 0)
    #img = Image.fromarray(pixarr)
    img.save(fileName + '.png', 'png')
clamp = lambda mn, v, mx : max(min(v, mx), mn)
def draw(recusion, pen, color, color2):
    stack = []
    pen.color(color2)
    for r in recusion:
        r1 = random.randint(0, 3000)
        if r1 < 3:
            pen.pensize(r1)
        if r == "[":
            stack.extend((pen.pos(), pen.heading()))
            pen.left(random.randint(-20, 35))
        if r == "]":
            pen.penup()
            pen.setheading(stack.pop())
            pen.setpos(stack.pop())
            pen.right(random.randint(-20, 35))
            pen.pendown()
        if r == "1":
            pen.forward(20)
        if r == "2":
            pen.forward(10)
        if r == "3":
            pen.pensize(3)
            pen.forward(20)
            pen.pensize(1)
        if r == "0":
            pen.pensize(5)
            pen.color(color)
            pen.forward(5)
            pen.color(color2)
            pen.pensize(1)
while run:
    # https://www.shadertoy.com/view/dtt3WS
    # col.x = 0.2 + abs(0.3 + sin(x) - cos(x) + (0.01 * 21. * sin(x)));
    # col.y = 0.4 + cos(x) * sin(x) + (0.1 * cos(x));
    # col.z = 0.5 * sin(x) + (0.3 * cos(x));
    # col.x = pow(col.x,1. / 2.2);
    # col.y = pow(col.y,1. / 2.2);
    # col.z = pow(col.z,1. / 2.2);
    gamma = 1/2.2
    x = time.time()
    treecolor = (clamp(0, int(abs(0.2 + abs(0.3 + sin(x) - cos(x) + (0.01 * 21. * sin(x))) ** gamma)*1), 1),
                 clamp(0, int(abs(0.4 + cos(x) * sin(x) + (0.1 * cos(x)) ** gamma)*1), 1),
                 clamp(0, int(abs(0.5 * sin(x) + (0.3 * cos(x)) ** gamma)*1), 1))
    x = time.time()*100
    treecolor2 = (clamp(0,int(abs(abs(sin(x) - cos(x) + (0.01 * 0.21 * cos(x))) ** gamma) * 0.94),1),
                 clamp(0,int(abs(0.1 + cos(x) * sin(x) + (0.7 * cos(x)) ** gamma) * 0.94),1),
                 clamp(0,int(abs(0.2 * sin(x) + (0.3 * cos(x)) ** gamma) * 0.94),1))
    pen.speed(0)
    tracer(0, 0)
    pen.penup()
    pen.setpos(0,-500)
    pen.setheading(90)
    pen.pendown()
    draw(tree, pen, treecolor, treecolor2)
    if mode == "fast":
        fc -= 1
        if fc == 0:
            run = False
        window.update()
        save_as_png(getcanvas(), f'tree-{mfc-fc}')
        print(f'generate tree {mfc-fc}-{mfc}')
        window.clear()
        continue
    while True:
        window.update()
        if not keyboard.is_pressed('r'):
            break
    while True:
        window.update()
        if keyboard.is_pressed('s') :
            save_as_png(getcanvas(), "tree")
        if keyboard.is_pressed('r'):
            window.clear()
            break
files = os.listdir(os.getcwd() + "assets/tree")
for file in files:
    if file.endswith(".eps"):
        os.remove(os.getcwd() + "assets/tree/" + file)