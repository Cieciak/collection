from numpy import array, ndarray, float64
from math import *
from tkinter import Canvas

class Vector2D:
    DRAW_RADIUS = 4
    DRAW_FILL = 'red'

    def __init__(self, /, x: int, y: int):
        self.__array = array([x, y], dtype=float64)

    @classmethod
    def fromArray(cls, arr: ndarray):
        return cls(arr[0], arr[1])

    def draw(self, canvas: Canvas):
        canvas.create_oval(
            self.__array[0] - self.DRAW_RADIUS + canvas.offset[0],
            self.__array[1] - self.DRAW_RADIUS + canvas.offset[1],
            self.__array[0] + self.DRAW_RADIUS + canvas.offset[0],
            self.__array[1] + self.DRAW_RADIUS + canvas.offset[1],
            fill=self.DRAW_FILL,
        )

    def rotateby(self, matrix: ndarray):
        self.__array @= matrix
    
    def xy(self): return self.__array[0], self.__array[1]

## 2D math

rotation_2d = array(
    [[cos(pi / 100), -sin(pi / 100)],
     [sin(pi / 100),  cos(pi / 100)],]
)

class Vector3D:
    PROJECTON = array(
        [[1, 0, 0],
         [0, 1, 0],]
    )

    def __init__(self, /, x: int, y: int, z: int):
        self.__array = array([x, y, z], dtype=float64)

    def __add__(u, v):
        return Vector3D.fromArray(u.array + v.array)
    
    def __iadd__(u, v):
        u.__array += v.array
        return u

    @classmethod
    def fromArray(cls, arr: ndarray):
        return cls(arr[0], arr[1], arr[2])

    @property
    def array(self) -> ndarray:
        return self.__array

    def project(self) -> Vector2D:
        return Vector2D.fromArray(self.PROJECTON @ self.__array)

    def draw(self, canvas: Canvas):
        Vector2D.fromArray(self.PROJECTON @ self.__array).draw(canvas)

    def rotateby(self, matrix: ndarray):
        self.__array @= matrix

## 3D math

rotation_z = array(
    [[cos(pi/200), -sin(pi/200), 0],
     [sin(pi/200),  cos(pi/200), 0],
     [          0,            0, 1],]
)

rotation_x = array(
    [[1,            0,            0],
     [0,  cos(pi/200), -sin(pi/200)],
     [0,  sin(pi/200),  cos(pi/200)]
    ]
)

rotation_y = array(
    [[cos(pi/200), 0, -sin(pi/200)],
     [          0, 1,            0],
     [sin(pi/200), 0,  cos(pi/200)]
    ]
)