import tkinter

from math import *
from time import sleep
from numpy import array

from processing import Vector2D, Vector3D, rotation_2d, rotation_z, rotation_y, rotation_x



SCREEN_SIZE = (                1000,                 1000)
INIT_OFFSET = ( .5 * SCREEN_SIZE[0],  .5 * SCREEN_SIZE[1])

root = tkinter.Tk()
root.geometry(f'{SCREEN_SIZE[0]}x{SCREEN_SIZE[1]}')

canvas = tkinter.Canvas(master=root, background='white', width=SCREEN_SIZE[0], height=SCREEN_SIZE[1])
canvas.place(x=-2, y=-2)
canvas.offset = INIT_OFFSET

points = [
    Vector3D( 100,  100,  100),
    Vector3D( 100,  100, -100),
    Vector3D( 100, -100,  100),
    Vector3D( 100, -100, -100),
    Vector3D(-100,  100,  100),
    Vector3D(-100,  100, -100),
    Vector3D(-100, -100,  100),
    Vector3D(-100, -100, -100),
]

while True:

    for p in points:
        p.draw(canvas)
        p.rotateby(rotation_y)
        p.rotateby(rotation_z)
        p.rotateby(rotation_y)
        p.rotateby(rotation_x)

    root.update()
    canvas.delete('all')
    sleep(0.01)