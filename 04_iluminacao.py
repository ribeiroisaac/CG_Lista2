from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
import sys
import sdl2

def Normal(a, b, c):
    x = 0
    y = 1
    z = 2
    v0 = a
    v1 = b
    v2 = c
    U = (v2[x] - v0[x], v2[y] - v0[y], v2[z] - v0[z])
    V = (v1[x ] -v0[x], v1[y] - v0[y], v1[z] - v0[z])
    N = ((U[y] * V[z] - U[z] * V[y]), (U[z] * V[x] - U[x] * V[z]), (U[x] * V[y] - U[y] * V[x]))
    NLength = sqrt(N[x] * N[x] + N[y] * N[y] + N[z] * N[z])
    return (N[x] / NLength, N[y] / NLength, N[z] / NLength)

def desenha():
	glPushMatrix()
	glRotatef(0.0, 1.0, 0.0, 0.0)
	raio = 1
	l = 4   # Quntidade de lados da base
	h = 5   # Altura

	radius = 2
	vertices = []
	
	glBegin(GL_POLYGON)
	for i in range(0, l):
		a = (i/l) * 2 * pi
		x = radius * cos(a) - raio
		y = radius * sin(a) - raio
		vertices += [(x,y)]

		glVertex3f(x, 0, y)
	glEnd()

	glBegin(GL_TRIANGLES)
	for i in range(0, l):
		glNormal3fv(Normal((vertices[i][0], 0.0, vertices[i][1]),(-raio, -raio, h),(vertices[(i+1) % l][0], 0.0, vertices[(i+1) % l][1])))
		glVertex3f(vertices[i][0], 0.0,  vertices[i][1])
		glVertex3f(-raio, h, -raio)
		glVertex3f(vertices[(i+1) % l][0], 0.0, vertices[(i+1) % l][1])
	glEnd()

	glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glRotatef(0.04,0,1,0)
    desenha()

def InitGL(width, height):
    mat_ambient = (0.8, 0.0, 0.0, 1.0)
    mat_diffuse = (1.0, 0.0, 0.0, 1.0)
    mat_specular = (1.0, 0.5, 0.5, 1.0)
    mat_shininess = (10,)
    light_position = (1, 0, 0)
    glClearColor(0.0,0.0,0.0,0.0)
    glShadeModel(GL_SMOOTH)
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    glClearColor(0.0, 0.0, 0.0, 0.0) 
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)               
    glEnable(GL_DEPTH_TEST)            
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    glTranslatef(0.0,-3.0,-3)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,0,10,0,0,0,0,1,0)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 2)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 1)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)
sdl2.SDL_GL_SetSwapInterval(1)
window = sdl2.SDL_CreateWindow(b"4", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, WINDOW_HEIGHT, sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_SHOWN)
if not window:
    sys.stderr.write("Error: Could not create window\n")
    exit(1)
glcontext = sdl2.SDL_GL_CreateContext(window)
InitGL(WINDOW_WIDTH, WINDOW_HEIGHT)
running = True
event = sdl2.SDL_Event()
while running:
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == sdl2.SDL_QUIT:
            running = False
        if event.type == sdl2.events.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                running = False
    display()
    sdl2.SDL_GL_SwapWindow(window)
