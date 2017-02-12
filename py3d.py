import sys
import time
import ctypes
import numpy
import math
from sdl2 import *

from structures import *
from camera import *

windowSize = (800, 600)

leftMouseDown = False
rightMouseDown = False
bracketDown = False

mouseDX, mouseDY = 0, 0
mouseX, mouseY = 0, 0

deltaTime = 0.00000001

def run():
    lastTime = time.perf_counter()

    points = numpy.matrix([
        [1, 1, 1],
        [1, 1, -1],
        [1, -1, 1],
        [1, -1, -1],
        [-1, 1, 1],
        [-1, 1, -1],
        [-1, -1, 1],
        [-1, -1, -1]]).T

    world = World()
    numObjects = 20
    mod = 10

    for i in range(0, numObjects):
        world.gameObjects.append(GameObject(Mesh(points), Transform(3 * (i % mod), 0, 3 * (i // mod))))

    #world.gameObjects.append(GameObject(Mesh(points), Transform(0,0,5)))
    global window, renderer, texture, deltaTime

    SDL_Init(SDL_INIT_VIDEO)
    SDL_SetRelativeMouseMode(1)
    SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, b"nearest")

    window = SDL_CreateWindow(b"py3d", SDL_WINDOWPOS_UNDEFINED,
                              SDL_WINDOWPOS_UNDEFINED, windowSize[0], windowSize[1], SDL_WINDOW_RESIZABLE)

    renderer = SDL_CreateRenderer(window, -1, 0)
    texture = SDL_CreateTexture(
        renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STATIC, windowSize[0], windowSize[1])

    x = 0; y = 0; z = 0
    rotY = 0; rotX = 0
    slowRate = 0.95; moveSpeed = 2.5; rotSpeed = 0.001
    fovSpeed = 0.5; fov = 0

    global camera
    camera = Camera(windowSize)

    global running
    running = True

    while running:
        deltaTime = time.perf_counter() - lastTime
        lastTime = time.perf_counter()

        handleEvents()

        keystate = SDL_GetKeyboardState(None)

        x, y, z, fov = 0, 0, 0, 0

        if keystate[SDL_SCANCODE_SPACE]: y=moveSpeed * deltaTime
        if keystate[SDL_SCANCODE_LSHIFT]: y=-moveSpeed * deltaTime
        if keystate[SDL_SCANCODE_D]: x=moveSpeed * deltaTime
        if keystate[SDL_SCANCODE_A]: x=-moveSpeed * deltaTime
        if keystate[SDL_SCANCODE_W]: z=moveSpeed * deltaTime
        if keystate[SDL_SCANCODE_S]: z=-moveSpeed * deltaTime
        if keystate[SDL_SCANCODE_F]: fov=fovSpeed * deltaTime
        if keystate[SDL_SCANCODE_R]: fov=-fovSpeed * deltaTime

        rotY = (mouseDX) * -rotSpeed;
        rotX = (mouseDY) * -rotSpeed;

        camera.rotX += rotX
        camera.rotY += rotY
        camera.fov += fov
        camera.transform.x += x * math.cos(camera.rotY) - z * math.sin(camera.rotY)
        camera.transform.y += y if y != 0 else z * math.sin(camera.rotX)
        camera.transform.z += z * math.cos(camera.rotY) + x * math.sin(camera.rotY)

        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255)
        SDL_RenderClear(renderer)
        camera.draw(renderer, world)

        SDL_RenderPresent(renderer)

    SDL_DestroyTexture(texture)
    SDL_DestroyRenderer(renderer)
    SDL_DestroyWindow(window)
    SDL_Quit()
    return 0


def handleEvents():
    global leftMouseDown, rightMouseDown, mouseX, mouseY, mouseDX, mouseDY, windowSize, camera
    
    mouseDX = 0
    mouseDY = 0

    event = SDL_Event()
    while SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == SDL_QUIT:
            global running
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button.button == SDL_BUTTON_LEFT:
                leftMouseDown = True
                SDL_SetRelativeMouseMode(1)
            elif event.button.button == SDL_BUTTON_RIGHT:
                rightMouseDown = True
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button.button == SDL_BUTTON_LEFT:
                leftMouseDown = False
            elif event.button.button == SDL_BUTTON_RIGHT:
                rightMouseDown = False
        elif event.type == SDL_MOUSEMOTION:
            mouseX = event.motion.x
            mouseY = event.motion.y
            mouseDX = event.motion.xrel
            mouseDY = event.motion.yrel
        elif event.type == SDL_KEYDOWN:
            if event.key.keysym.sym == SDLK_ESCAPE:
                SDL_SetRelativeMouseMode(0)
        elif event.type == SDL_WINDOWEVENT and event.window.event == SDL_WINDOWEVENT_RESIZED:
            windowSize = (event.window.data1, event.window.data2)
            camera.recalculateWindow(windowSize)

if __name__ == "__main__":
    sys.exit(run())
