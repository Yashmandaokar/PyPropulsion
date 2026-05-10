import pytest

from pypropulsion.mission import MissionRequirement


def test_valid_mission_requirement():
    mission = MissionRequirement(
        payload_mass=300.0,
        target_orbit_altitude=500_000.0,
        target_inclination=97.0,
        launch_site="Europe",
        mission_type="SSO",
    )

    assert mission.payload_mass == 300.0
    assert mission.target_orbit_altitude == 500_000.0
    assert mission.target_inclination == 97.0
    assert mission.launch_site == "Europe"
    assert mission.mission_type == "SSO"


def test_invalid_payload_mass():
    with pytest.raises(ValueError):
        MissionRequirement(
            payload_mass=-10.0,
            target_orbit_altitude=500_000.0,
            target_inclination=97.0,
            launch_site="Europe",
        )