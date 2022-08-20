import sys
import numpy as np
import sdl2
from OpenGL.GL import *
from OpenGL.GLU import *
import math

N = 50

def InitGL(Width, Height):             
    glClearColor(0.0, 0.0, 0.0, 0.0) 
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)               
    glEnable(GL_DEPTH_TEST)            
    glShadeModel(GL_SMOOTH)            
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def map(valor, v0, vf, m0, mf):
    return m0+(((valor-v0)*(mf-m0))/(vf-v0))

def coordenadaEsferica(i,j):
    theta = map(i,0,N,-math.pi/2,math.pi/2)
    phy = map(j,0,N,0,2*math.pi)
    x = r * math.cos(theta)*math.cos(phy)
    y = r * math.sin(theta)
    z = r * math.cos(theta)*math.sin(phy)
    return x, y, z

def paraboloide_z(x,y):
    return x**2 + y**2

dx = 0.1
dy = 0.1
def paraboloide():
    for i in np.arange(-1,1, dx):
        glBegin(GL_TRIANGLE_STRIP)
        xO = i
        x = xO
        x+=dx
        for j in np.arange(-1,1, dy):
            y = j
            z = paraboloide_z(xO,y)
            glColor3f(0.9,0.9,-1*(z-0.5))
            glVertex3f(xO,y,z)
            z = paraboloide_z(x,y)
            glVertex3f(x,y,z)
        glEnd()

a=0
r=1
def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()       
    glTranslatef(0.0,0.0,-7.0)
    glRotatef(a,0.0,1.0,0.0) 
    paraboloide()     
    a+=0.50

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 2)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 1)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)
sdl2.SDL_GL_SetSwapInterval(1)
window = sdl2.SDL_CreateWindow(b"Implicita", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, WINDOW_HEIGHT, sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_SHOWN)
if not window:
    sys.stderr.write("Error: Could not create window\n")
    exit(1)
glcontext = sdl2.SDL_GL_CreateContext(window)
InitGL(WINDOW_WIDTH,WINDOW_HEIGHT)
running = True
event = sdl2.SDL_Event()
while running:
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == sdl2.SDL_QUIT:
            running = False
        if event.type == sdl2.events.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                running = False
    desenha()
    sdl2.SDL_GL_SwapWindow(window)
