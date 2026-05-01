

"""
Simulation of balls bouncing around in a box, with optional gravity and collisions. Based on the disksSim.py file, but simplified to use marks instead of circles, and renamed to ballSim.py to reflect the change from disks to balls.
"""

from .ball import Ball
from .box import Box
import numpy as np
from . import disksSim
import wassilypy

class BallSim(disksSim.DisksSim):

    max_dots = 15
    max_radius = 120
    max_speed = 180
    gravitational_constant = 0.1

    def make_border(self):
        return Box(self.width, self.height, self.height)

    def set_geometry(self, diagram):
        h = self.height
        mainFrame = diagram.mainFrame
        center3d = np.array([0, 0, 0])
        self.frame = mainFrame
        h32 = h * 1.1
        viewframe = mainFrame.regionFrame(
            [0,0],
            [h, h],
            [-h32, -h32],
            [h32, h32],
        )
        eyepoint = np.array([h * 1.2, h*0.7, -h * 3])
        perspective = True
        lookAt = [h/2, h/2, h/2]
        self.frame3d = viewframe.frame3d(
            eyePoint=eyepoint,
            lookAtPoint=lookAt,
            perspective=perspective,
        )
        # on the frame3d draw the box edge lines as thin black lines (xxx there is a better way)
        self.frame3d.line((0, 0, 0), (h, 0, 0)).colored("black")
        self.frame3d.line((h, 0, 0), (h, h, 0)).colored("black")
        self.frame3d.line((h, h, 0), (0, h, 0)).colored("black")
        self.frame3d.line((0, h, 0), (0, 0, 0)).colored("black")
        self.frame3d.line((0, 0, 0), (0, 0, h)).colored("black")
        self.frame3d.line((h, 0, 0), (h, 0, h)).colored("black")
        self.frame3d.line((h, h, 0), (h, h, h)).colored("black")
        self.frame3d.line((0, h, 0), (0, h, h)).colored("black")
        self.frame3d.line((0, 0, h), (h, 0, h)).colored("black")
        self.frame3d.line((h, 0, h), (h, h, h)).colored("black")
        self.frame3d.line((h, h, h), (0, h, h)).colored("black")
        self.frame3d.line((0, h, h), (0, 0, h)).colored("black")

    def mark(self, location, radius):
        return self.frame3d.circle(location, radius).colored(disksSim.randomRGBString())
    
    def make_dot(self):
        radius = np.random.uniform(self.min_radius, self.max_radius)
        xyz = np.random.uniform(radius, self.width - radius, size=3)
        speed = np.random.uniform(self.min_speed, self.max_speed)
        alpha = np.random.uniform(0, 2 * np.pi)
        beta = np.random.uniform(0, np.pi)
        dx = np.cos(alpha) * np.sin(beta)
        dy = np.sin(alpha) * np.sin(beta)
        dz = np.cos(beta)
        velocity = speed * np.array([dx, dy, dz])
        ball = Ball(xyz, velocity, radius)
        return ball
    
    def update_positions(self):
        for dot, mark in self.dot_marks:
            mark.centered(dot.pos)
