import tkinter

from math import *
from time import sleep
from numpy import array, ndarray 

from processing import Vector3D, rotation_z, rotation_y, rotation_x

SCREEN_SIZE = (                1000,                 1000)
INIT_OFFSET = ( .5 * SCREEN_SIZE[0],  .5 * SCREEN_SIZE[1])

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

class App(tkinter.Tk):

    def __init__(self, model):
        super().__init__()

        self.isRunning  = False
        self.isRotating = False

        self.geometry(f'{SCREEN_SIZE[0]}x{SCREEN_SIZE[1]}')
        self.protocol('WM_DELETE_WINDOW', exit)
        self.bind('<Key>', self.key)

        self.canvas = tkinter.Canvas(
            master=self,
            background='white',
            width=SCREEN_SIZE[0],
            height=SCREEN_SIZE[1],
        )
        self.canvas.place(x=-2, y=-2)
        self.canvas.offset = INIT_OFFSET

        self.model: Model = model

    def exit(self): self.isRunning = False

    def run(self):
        self.isRunning = True

        while self.isRunning:
            self.model.draw(self.canvas)
            if self.isRotating: model.rotateby(rotation_x @ rotation_y @ rotation_z @ rotation_z)

            self.update()
            self.canvas.delete('all')
            sleep(0.01)


    def key(self, event: tkinter.Event):

        match event.keysym:
            case 'Up':
                self.model.translateby(Vector3D(0,-10, 0))
            case 'Down':
                self.model.translateby(Vector3D(0, 10, 0))
            case 'Left':
                self.model.translateby(Vector3D(-10,  0, 0))
            case 'Right':
                self.model.translateby(Vector3D(10,  0, 0))

            case 'r':
                self.isRotating = not self.isRotating

# points = [
#     Vector3D( 100,  100, -100),
#     Vector3D( 100, -100, -100),
#     Vector3D(-100, -100, -100),
#     Vector3D(-100,  100, -100),
#     Vector3D( 100,  100,  100),
#     Vector3D( 100, -100,  100),
#     Vector3D(-100, -100,  100),
#     Vector3D(-100,  100,  100),
# ]

# conn = [
#     (0, 1),
#     (1, 2),
#     (2, 3),
#     (3, 0),
#     (4, 5),
#     (5, 6),
#     (6, 7),
#     (7, 4),
#     (0, 4),
#     (1, 5),
#     (2, 6),
#     (3, 7),
# ]

points = [
    Vector3D(100, 50, 0),
    Vector3D(-50,-50, 0),
    Vector3D( 50,-50, 0),
    Vector3D(  0,  0,25),
]

conn = [
    (0, 1),
    (1, 2),
    (2, 0),
    (0, 3),
    (1, 3),
    (2, 3),
]


if __name__ == '__main__':
    model = Model(points, conn)
    app = App(model)
    app.run()