from pypropulsion.mission.orbit import circular_orbit_velocity


def test_circular_orbit_velocity_500km():
    velocity = circular_orbit_velocity(500_000.0)

    assert 7_500.0 < velocity < 7_700.0