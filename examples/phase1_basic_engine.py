from pypropulsion.phase1.performance import (
    effective_exhaust_velocity,
    propellant_mass,
    split_oxidizer_fuel_flow,
    total_mass_flow_rate,
)


thrust = 400_000.0  # N
specific_impulse = 280.0  # s
burn_time = 150.0  # s
mixture_ratio = 2.6  # O/F


exhaust_velocity = effective_exhaust_velocity(specific_impulse)
mass_flow = total_mass_flow_rate(thrust, specific_impulse)
oxidizer_flow, fuel_flow = split_oxidizer_fuel_flow(mass_flow, mixture_ratio)
total_propellant = propellant_mass(mass_flow, burn_time)


print("Phase 1 Basic Engine Sizing")
print("---------------------------")
print(f"Thrust: {thrust:.1f} N")
print(f"Specific impulse: {specific_impulse:.1f} s")
print(f"Effective exhaust velocity: {exhaust_velocity:.2f} m/s")
print(f"Total mass flow rate: {mass_flow:.3f} kg/s")
print(f"Oxidizer mass flow rate: {oxidizer_flow:.3f} kg/s")
print(f"Fuel mass flow rate: {fuel_flow:.3f} kg/s")
print(f"Total propellant mass: {total_propellant:.2f} kg")