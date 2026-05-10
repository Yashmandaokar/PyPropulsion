"""Mission requirement definitions for PyPropulsion."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MissionRequirement:
    """High-level mission requirements.

    This class stores the basic mission-level inputs before converting them
    into propulsion or engine-level requirements.

    Parameters
    ----------
    payload_mass:
        Payload mass in kg.
    target_orbit_altitude:
        Target circular orbit altitude in meters.
    target_inclination:
        Target orbital inclination in degrees.
    launch_site:
        Name or description of the launch site.
    mission_type:
        Type of mission, for example "LEO", "SSO", or "GTO".
    """

    payload_mass: float
    target_orbit_altitude: float
    target_inclination: float
    launch_site: str
    mission_type: str = "LEO"

    def __post_init__(self) -> None:
        if self.payload_mass <= 0:
            raise ValueError("Payload mass must be positive.")

        if self.target_orbit_altitude <= 0:
            raise ValueError("Target orbit altitude must be positive.")

        if not 0 <= self.target_inclination <= 180:
            raise ValueError("Target inclination must be between 0 and 180 degrees.")

        if not self.launch_site:
            raise ValueError("Launch site must be provided.")
        
mission = MissionRequirement(
    payload_mass=300.0,
    target_orbit_altitude=500_000.0,
    target_inclination=97.0,
    launch_site="Europe",
    mission_type="SSO",
)