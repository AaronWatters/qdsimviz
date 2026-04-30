
"""
A disk is a circular object in a 2d space.
"""

import numpy as np

def vec(xy):
    return np.array(xy, dtype=np.float64)

class Disk:

    def __init__(self, xy, velocity, radius, mass=None):
        self.xy = vec(xy)
        self.velocity = vec(velocity)
        self.radius = radius
        self.mass = mass
        if mass is None:
            self.mass = np.pi * radius**2  # Assuming density = 1

    def move(self, dt):
        self.xy += self.velocity * dt

    def collides_with(self, other):
        return np.linalg.norm(self.xy - other.xy) < self.radius + other.radius
    
    def bounce(self, other):
        # Elastic collision between two disks
        delta = self.xy - other.xy
        distance = np.linalg.norm(delta)
        if distance == 0:
            return  # Avoid division by zero
        normal = delta / distance
        relative_velocity = self.velocity - other.velocity
        speed = np.dot(relative_velocity, normal)
        if speed > 0:
            return  # Disks are moving apart
        inverse_mass_self = 1.0 / self.mass
        inverse_mass_other = 1.0 / other.mass
        impulse = (2 * speed) / (inverse_mass_self + inverse_mass_other)
        self.velocity -= impulse * inverse_mass_self * normal
        other.velocity += impulse * inverse_mass_other * normal

    def gravity(self, other, dt, G=1.0):
        """Apply gravitational attraction between two disks.
        
        Args:
            other: The other disk to attract
            dt: Time step for acceleration
            G: Gravitational constant (default 1.0)
        """
        delta = other.xy - self.xy
        distance = np.linalg.norm(delta)
        if distance == 0 or distance < 1e-10:
            return  # Avoid division by zero
        normal = delta / distance
        # Gravitational force: F = G * m1 * m2 / r^2
        force_magnitude = G * self.mass * other.mass / (distance ** 2)
        # Acceleration: a = F / m
        acceleration_self = force_magnitude / self.mass
        acceleration_other = force_magnitude / other.mass
        # Update velocities
        self.velocity += acceleration_self * normal * dt
        other.velocity -= acceleration_other * normal * dt

    def boundary_bounce(self, page):
        self.xy, self.velocity = page.bounce(self.xy, self.velocity, self.radius)
