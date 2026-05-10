from pypropulsion.phase1.performance import (
    effective_exhaust_velocity,
    propellant_mass,
    split_oxidizer_fuel_flow,
    total_mass_flow_rate,
)


def test_effective_exhaust_velocity():
    result = effective_exhaust_velocity(280.0)
    assert abs(result - 2745.862) < 1e-3


def test_total_mass_flow_rate():
    result = total_mass_flow_rate(400_000.0, 280.0)
    assert abs(result - 145.674) < 1e-3


def test_propellant_mass():
    result = propellant_mass(145.674, 150.0)
    assert abs(result - 21851.1) < 1e-1


def test_split_oxidizer_fuel_flow():
    oxidizer, fuel = split_oxidizer_fuel_flow(145.674, 2.6)

    assert abs(oxidizer - 105.209) < 1e-3
    assert abs(fuel - 40.465) < 1e-3
