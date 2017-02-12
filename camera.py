import numpy
import math
from sdl2 import *
from structures import *

class Camera:

    def __init__(self, windowSize):
        self.offsetX = windowSize[0] / 2
        self.offsetY = windowSize[1] / 2
        self.scale = windowSize[0] / 2
        self.transform = Transform(0, 1, -3)
        self.ar = windowSize[0] / windowSize[1]
        self.near = 0.01
        self.far = 100
        self.rotX = 0
        self.rotY = 0
        self.fov = 60 * math.pi / 180

    def recalculateWindow(self, windowSize):
        self.offsetX = windowSize[0] / 2
        self.offsetY = windowSize[1] / 2
        self.scale = windowSize[0] / 2
        self.ar = windowSize[0] / windowSize[1]

    def draw(self, renderer, world):
        for g in range(0, len(world.gameObjects)):
            curG = world.gameObjects[g]
            points = curG.mesh.points + numpy.matrix([[curG.transform.x],
                                                      [curG.transform.y],
                                                      [curG.transform.z]])
            projPoints = self.perspectiveProjection(points)
            for i in range(0, points.shape[1]):
                for j in range(i+1, points.shape[1]):
                    if abs(projPoints[2, i] > 1) or abs(projPoints[2,j] > 1):
                        continue
                    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
                    SDL_RenderDrawLine(renderer, (int)(self.offsetX + self.scale * projPoints[0,i]),
                                                 (int)(self.offsetY - self.scale * projPoints[1,i]),
                                                 (int)(self.offsetX + self.scale * projPoints[0,j]),
                                                 (int)(self.offsetY - self.scale * projPoints[1,j]))

    def perspectiveProjection(self, points):
        localPoints = points - numpy.matrix([[self.transform.x],
                                             [self.transform.y],
                                             [self.transform.z]])
        localPoints = Camera.genRotX(self.rotX).dot(Camera.genRotY(self.rotY)).dot(localPoints)
        localPoints = numpy.concatenate((localPoints, numpy.ones((1, localPoints.shape[1]))))
        localPoints = Camera.perspective(self.ar, self.fov, self.near, self.far).dot(localPoints)
        for i in range(0, localPoints.shape[0]-1):
            for j in range(0, localPoints.shape[1]):
                localPoints[i,j] = localPoints[i,j] / localPoints[3,j]



        return localPoints


    def perspective(ar, fov, near, far):
        return numpy.matrix([
           [1/(math.tan(fov / 2)), 0, 0, 0],
           [0, 1/math.tan(fov / 2), 0, 0],
           [0, 0, (-near-far)/(near-far), 2*near*far/(near-far)],
           [0, 0, 1, 0]
        ]);

    def genRotZ(t):
        return numpy.matrix([
                [math.cos(t), -math.sin(t), 0],
                [math.sin(t),  math.cos(t), 0],
                [          0,            0, 1]
            ])

    def genRotY(t):
        return numpy.matrix([
                [ math.cos(t), 0, math.sin(t)],
                [           0, 1, 0          ],
                [-math.sin(t), 0, math.cos(t)]
            ])

    def genRotX(t):
        return numpy.matrix([
                [1,           0,            0],
                [0, math.cos(t), -math.sin(t)],
                [0, math.sin(t),  math.cos(t)]
            ])