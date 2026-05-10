"""Orbit-related calculations for mission analysis."""

from pypropulsion.constants import EARTH_RADIUS, EARTH_GRAVITATIONAL_PARAMETER


def circular_orbit_velocity(altitude: float) -> float:
    """Calculate circular orbital velocity at a given altitude.

    Parameters
    ----------
    altitude:
        Orbit altitude above Earth's surface in meters.

    Returns
    -------
    float
        Circular orbital velocity in m/s.
    """
    if altitude <= 0:
        raise ValueError("Altitude must be positive.")

    orbital_radius = EARTH_RADIUS + altitude
    return (EARTH_GRAVITATIONAL_PARAMETER / orbital_radius) ** 0.5