from simulating_blobs_of_fluid.simulation import Simulation

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GL import shaders

import numpy as np

import sys
import timeit


simulation = Simulation(particle_count=100, dt=0.016, box_width=250)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutCreateWindow('fluid')

    FRAGMENT_SHADER = shaders.compileShader(
        """#version 120
        void main() {
            gl_FragColor = vec4( 0, 1, 0, 1 );
        }""", GL_FRAGMENT_SHADER
    )

    shader = shaders.compileProgram(FRAGMENT_SHADER)
    shaders.glUseProgram(shader)

    glutDisplayFunc(display)
    glutIdleFunc(display)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.0, 1.0, 1.0, 200.0)
    glMatrixMode(GL_MODELVIEW)

    gluLookAt(0, 0, 180,
              0, 0, 0,
              0, 1, 0)

    glPushMatrix()
    glutMainLoop()

    return


def display():
    simulation_start = timeit.default_timer()
    simulation.step()
    simulation_end = timeit.default_timer()

    render_start = timeit.default_timer()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    scale = 0.2

    for particle in simulation.particles:
        x = particle.position.x * scale
        y = particle.position.y * scale
        z = 0

        glPushMatrix()
        glTranslatef(x, y, z)
        glutSolidSphere(1, 20, 20)
        glPopMatrix()

    glutSwapBuffers()

    render_end = timeit.default_timer()

    print("simulation took: %8.4f   render took: %8.4f    FPS: %8.4f" % (
        simulation_end - simulation_start,
        render_end - render_start,
        1.0 / (render_end - simulation_start)
    ))

    return


if __name__ == '__main__':
    main()
