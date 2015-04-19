"""
Contains all physical constants
"""
from phys_util.units import farad, meter, second, henry

# pylint: disable=invalid-name
epsilon0 = 8.854187817e-12 * farad / meter
c = 299792458 * meter / second
mu0 = 1.2566370614e-6 * henry / meter
