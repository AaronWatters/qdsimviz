"""
A page is a rectangular region in which
to run a simulation.
"""

import wassilypy
import numpy as np
from .dot import vec

class Page:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def inside(self, xy):
        x, y = xy
        return 0 <= x < self.width and 0 <= y < self.height
    
    def intersects_boundary(self, xy, radius):
        x, y = xy
        return (x - radius < 0 or x + radius >= self.width or
                y - radius < 0 or y + radius >= self.height)
    
    def bounce(self, xy, velocity, radius):
        x, y = xy
        vx, vy = velocity
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
        return vec((x, y)), vec((vx, vy))
