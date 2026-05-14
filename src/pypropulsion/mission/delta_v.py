"""Delta-V estimation methods for mission analysis."""

from pypropulsion.mission.orbit import circular_orbit_velocity


def estimate_leo_delta_v(
    orbit_altitude: float,
    gravity_loss: float = 1_500.0,
    drag_loss: float = 200.0,
    steering_loss: float = 100.0,
) -> float:
    """Estimate total Delta-V required to reach a circular LEO orbit."""

    if orbit_altitude <= 0.0:
        raise ValueError("Orbit altitude must be positive.")
    
    if orbit_altitude > 2_000_000.0:
        raise ValueError("estimate_leo_delta_v is intended for LEO missions only. ")

    if gravity_loss < 0.0:
        raise ValueError("Gravity loss must not be negative.")

    if drag_loss < 0.0:
        raise ValueError("Drag loss must not be negative.")

    if steering_loss < 0.0:
        raise ValueError("Steering loss must not be negative.")

    orbital_velocity = circular_orbit_velocity(orbit_altitude)

    return (
        orbital_velocity
        + gravity_loss
        + drag_loss
        + steering_loss
    )