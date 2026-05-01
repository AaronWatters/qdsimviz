
"""
A ball is a spherical object in a 3d space.
"""

import numpy as np
from .dot import Dot, vec

class Ball(Dot):

    def __init__(self, xyz, velocity, radius, mass=None):
        if mass is None:
            mass = (4.0 / 3.0) * np.pi * radius**3  # Assuming density = 1
        super(Ball, self).__init__(xyz, velocity, radius, mass)

    @property
    def xyz(self):
        return self.pos

    @xyz.setter
    def xyz(self, value):
        self.pos = value
