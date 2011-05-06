#!/usr/bin/python

import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

window = 0
w_hlen, w_vlen = 800, 600
ESCAPE = '\033'

def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
    glClearColor(1.0, 1.0, 1.0, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
    ReSizeGLScene(Width, Height, first=True)

def ReSizeGLScene(Width, Height, first=False):
    if not first:
        if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small
	        Height = 1
        glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def DrawGLScene():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)



	glutSwapBuffers()

def keyPressed(*args):
	c = args[0]
	if c == ESCAPE:
		glutDestroyWindow(window)
		exit()

def main():
	global w_hlen, w_vlen
	print "Hit ESC key to quit."
	try:
		GLU_VERSION_1_2
	except:
		print "Need GLU 1.2 to run this demo"
		exit(1)

	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	glutInitWindowSize(w_hlen, w_vlen)
	glutInitWindowPosition(0, 0)

	global window
	window = glutCreateWindow("Template")

	glutDisplayFunc(DrawGLScene)
	# glutFullScreen()
	glutIdleFunc(DrawGLScene)
	glutReshapeFunc(ReSizeGLScene)
	glutKeyboardFunc(keyPressed)
	InitGL(w_hlen, w_vlen)
	glutMainLoop()

if __name__ == '__main__':
	main()
