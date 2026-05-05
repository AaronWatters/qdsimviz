import numpy as np

from qdsimviz.disk import Disk


def test_bounce_uses_inverse_mass_weighting():
    light = Disk((0, 0), (1, 0), radius=1, mass=1)
    heavy = Disk((1.5, 0), (0, 0), radius=1, mass=3)

    light.bounce(heavy)

    np.testing.assert_allclose(light.velocity, [-0.5, 0.0])
    np.testing.assert_allclose(heavy.velocity, [0.5, 0.0])


def test_gravity_attracts_based_on_mass():
    """Heavier objects should accelerate less from gravitational attraction."""
    light = Disk((0, 0), (0, 0), radius=1, mass=1)
    heavy = Disk((10, 0), (0, 0), radius=1, mass=4)

    light.gravity(heavy, dt=1.0, G=1.0)

    # Light disk accelerates toward heavy disk
    assert light.velocity[0] > 0
    # Heavy disk accelerates toward light disk (in negative direction)
    assert heavy.velocity[0] < 0
    # Light disk should accelerate faster (lower mass)
    assert abs(light.velocity[0]) > abs(heavy.velocity[0])