import pytest

from pypropulsion.mission.delta_v import estimate_leo_delta_v

def test_estimated_delta_v_500_km():
    delta_v = estimate_leo_delta_v(500_000.0)

    assert 9_300.0 < delta_v < 9_500.0

def test_negative_orbit_altitude_raise_error():
    with pytest.raises(ValueError):
        estimate_leo_delta_v(-500_000.0)

def test_negative_loss_raises_error():
    with pytest.raises(ValueError):
        estimate_leo_delta_v(
            orbit_altitude=500_000.0,
            gravity_loss=-1.0,
        )
    