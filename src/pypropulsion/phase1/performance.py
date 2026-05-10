"""Basic rocket engine performance calculations for Phase 1."""

from pypropulsion.constants import STANDARD_GRAVITY


def effective_exhaust_velocity(
    specific_impulse: float,
    gravity: float = STANDARD_GRAVITY,
) -> float:
    """Calculate effective exhaust velocity.

    Parameters
    ----------
    specific_impulse:
        Specific impulse in seconds.
    gravity:
        Reference gravitational acceleration in m/s^2.

    Returns
    -------
    float
        Effective exhaust velocity in m/s.
    """
    if specific_impulse <= 0:
        raise ValueError("Specific impulse must be positive.")

    return specific_impulse * gravity


def total_mass_flow_rate(
    thrust: float,
    specific_impulse: float,
    gravity: float = STANDARD_GRAVITY,
) -> float:
    """Calculate total propellant mass flow rate.

    Parameters
    ----------
    thrust:
        Engine thrust in newtons.
    specific_impulse:
        Specific impulse in seconds.
    gravity:
        Reference gravitational acceleration in m/s^2.

    Returns
    -------
    float
        Total mass flow rate in kg/s.
    """
    if thrust <= 0:
        raise ValueError("Thrust must be positive.")
    if specific_impulse <= 0:
        raise ValueError("Specific impulse must be positive.")

    return thrust / (specific_impulse * gravity)


def propellant_mass(
    mass_flow_rate: float,
    burn_time: float,
) -> float:
    """Calculate total propellant mass required."""
    if mass_flow_rate <= 0:
        raise ValueError("Mass flow rate must be positive.")
    if burn_time <= 0:
        raise ValueError("Burn time must be positive.")

    return mass_flow_rate * burn_time


def split_oxidizer_fuel_flow(
    total_mass_flow: float,
    mixture_ratio: float,
) -> tuple[float, float]:
    """Split total mass flow into oxidizer and fuel flow.

    Mixture ratio is defined as:

        O/F = oxidizer mass flow / fuel mass flow

    Returns
    -------
    tuple[float, float]
        Oxidizer mass flow and fuel mass flow in kg/s.
    """
    if total_mass_flow <= 0:
        raise ValueError("Total mass flow must be positive.")
    if mixture_ratio <= 0:
        raise ValueError("Mixture ratio must be positive.")

    fuel_flow = total_mass_flow / (1.0 + mixture_ratio)
    oxidizer_flow = total_mass_flow - fuel_flow

    return oxidizer_flow, fuel_flow
