import tkinter

from math import *
from time import sleep
from numpy import array, ndarray 

from processing import Vector2D, Vector3D, rotation_2d, rotation_z, rotation_y, rotation_x

SCREEN_SIZE = (                1000,                 1000)
INIT_OFFSET = ( .5 * SCREEN_SIZE[0],  .5 * SCREEN_SIZE[1])

def exit(): root.running = False

root = tkinter.Tk()
root.geometry(f'{SCREEN_SIZE[0]}x{SCREEN_SIZE[1]}')
root.running = True
root.protocol('WM_DELETE_WINDOW', exit)

canvas = tkinter.Canvas(master=root, background='white', width=SCREEN_SIZE[0], height=SCREEN_SIZE[1])
canvas.place(x=-2, y=-2)
canvas.offset = INIT_OFFSET

class Model:

    def __init__(self, points: list[Vector3D] = list(), connections: list[tuple[int, int]] = list()):
        self.__points: list[Vector3D] = points
        self.__connections: list[tuple[int, int]] = connections

    def draw(self, canvas: tkinter.Canvas):
        for p in self.__points: p.draw(canvas)

        for start, end in self.__connections:
            x0, y0 = self.__points[start].project().xy()
            x1, y1 = self.__points[end].project().xy()
            canvas.create_line(
                x0 + canvas.offset[0], y0 + canvas.offset[1],
                x1 + canvas.offset[0], y1 + canvas.offset[1],
            )

    def translateby(self, v: Vector3D):
        for p in self.__points: p += v

    def rotateby(self, matrix: ndarray):
        for p in self.__points: p.rotateby(matrix)

points = [
    Vector3D( 100,  100, -100),
    Vector3D( 100, -100, -100),
    Vector3D(-100, -100, -100),
    Vector3D(-100,  100, -100),
    Vector3D( 100,  100,  100),
    Vector3D( 100, -100,  100),
    Vector3D(-100, -100,  100),
    Vector3D(-100,  100,  100),
]

conn = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
]

model = Model(points, conn)
model.translateby(Vector3D(100, 0, 0))

while root.running:

    model.draw(canvas)
    model.rotateby(rotation_x @ rotation_y @ rotation_z @ rotation_z)

    root.update()
    canvas.delete('all')
    sleep(0.01)