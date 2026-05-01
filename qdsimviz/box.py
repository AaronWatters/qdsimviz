"""
A box is a rectangular region in 3d space in which
to run a simulation.
"""

import numpy as np
from .dot import vec

class Box:

    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth

    def inside(self, xyz):
        x, y, z = xyz
        return (0 <= x < self.width and
                0 <= y < self.height and
                0 <= z < self.depth)

    def intersects_boundary(self, xyz, radius):
        x, y, z = xyz
        return (x - radius < 0 or x + radius >= self.width or
                y - radius < 0 or y + radius >= self.height or
                z - radius < 0 or z + radius >= self.depth)

    def bounce(self, xyz, velocity, radius):
        x, y, z = xyz
        vx, vy, vz = velocity
        if x - radius < 0:
            x = radius
            if vx < 0:
                vx = -vx
        elif x + radius >= self.width:
            x = self.width - radius - 1
            if vx > 0:
                vx = -vx
        if y - radius < 0:
            y = radius
            if vy < 0:
                vy = -vy
        elif y + radius >= self.height:
            y = self.height - radius - 1
            if vy > 0:
                vy = -vy
        if z - radius < 0:
            z = radius
            if vz < 0:
                vz = -vz
        elif z + radius >= self.depth:
            z = self.depth - radius - 1
            if vz > 0:
                vz = -vz
        return vec((x, y, z)), vec((vx, vy, vz))
