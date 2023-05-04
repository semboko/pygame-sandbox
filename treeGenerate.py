import random
import pygame
from PIL import Image, EpsImagePlugin
from turtle import Turtle, Screen, tracer, getcanvas
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
print(tree)
EpsImagePlugin.gs_windows_binary = "C:/Program Files/gs/gs10.01.1/bin/gswin64c.exe"
fc = 50
run = True
mode = "fast" # norm, fast
def save_as_png(canvas,fileName):
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
def draw(recusion, pen):
    stack = []
    for r in recusion:
        if r == "[":
            stack.extend((pen.pos(), pen.heading()))
            pen.left(random.randint(-10, 35))
        if r == "]":
            pen.penup()
            pen.setheading(stack.pop())
            pen.setpos(stack.pop())
            pen.right(random.randint(-10, 35))
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
            pen.color("green")
            pen.forward(5)
            pen.color("black")
            pen.pensize(1)
while run:
    pen.speed(0)
    tracer(0, 0)
    pen.penup()
    pen.setpos(0,-500)
    pen.setheading(90)
    pen.pendown()
    draw(tree, pen)
    if mode == "fast":
        fc -= 1
        if fc == 0:
            run = False
        window.update()
        save_as_png(getcanvas(), f'tree-{50-fc}')
        print(f'generate tree {50-fc}-50')
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
files = os.listdir(os.getcwd())
for file in files:
    if file.endswith(".eps"):
        os.remove(file)