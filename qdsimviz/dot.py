
"""
A dot is a circular/spherical object with common physics functionality
shared by Ball (3d) and Disk (2d).
"""

import numpy as np

def vec(coords):
    return np.array(coords, dtype=np.float64)

class Dot:

    def __init__(self, pos, velocity, radius, mass):
        self.pos = vec(pos)
        self.velocity = vec(velocity)
        self.radius = radius
        self.mass = mass

    def move(self, dt):
        self.pos += self.velocity * dt

    def collides_with(self, other):
        return np.linalg.norm(self.pos - other.pos) < self.radius + other.radius

    def bounce(self, other):
        # Elastic collision between two dots
        delta = self.pos - other.pos
        distance = np.linalg.norm(delta)
        if distance == 0:
            return  # Avoid division by zero
        normal = delta / distance
        relative_velocity = self.velocity - other.velocity
        speed = np.dot(relative_velocity, normal)
        if speed > 0:
            return  # Dots are moving apart
        inverse_mass_self = 1.0 / self.mass
        inverse_mass_other = 1.0 / other.mass
        impulse = (2 * speed) / (inverse_mass_self + inverse_mass_other)
        self.velocity -= impulse * inverse_mass_self * normal
        other.velocity += impulse * inverse_mass_other * normal

    def gravity(self, other, dt, G=1.0):
        """Apply gravitational attraction between two dots.

        Args:
            other: The other dot to attract
            dt: Time step for acceleration
            G: Gravitational constant (default 1.0)
        """
        delta = other.pos - self.pos
        distance = np.linalg.norm(delta)
        if distance < 1e-10:
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

    def boundary_bounce(self, boundary):
        self.pos, self.velocity = boundary.bounce(self.pos, self.velocity, self.radius)
