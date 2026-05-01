
"""
A disk is a circular object in a 2d space.
"""

import numpy as np
from .dot import Dot, vec

class Disk(Dot):

    def __init__(self, xy, velocity, radius, mass=None):
        if mass is None:
            mass = np.pi * radius**2  # Assuming density = 1
        super(Disk, self).__init__(xy, velocity, radius, mass)

    @property
    def xy(self):
        return self.pos

    @xy.setter
    def xy(self, value):
        self.pos = value
