from pypropulsion.mission import MissionRequirement, analyze_mission


mission = MissionRequirement(
    payload_mass=2000.0,
    target_orbit_altitude=500_000.0,
    target_inclination=97.0,
    launch_site="Europe",
    mission_type="SSO",
)

result = analyze_mission(mission)

print("\n========== MISSION ANALYSIS ==========")

print(f"Mission type: {mission.mission_type}")
print(f"Payload mass: {mission.payload_mass:.1f} kg")
print(f"Orbit altitude: {mission.target_orbit_altitude / 1000:.1f} km")
print(f"Inclination: {mission.target_inclination:.1f} deg")

print("\n========== ORBIT ==========")

print(f"Orbital velocity: {result.orbital_velocity:.2f} m/s")
print(f"Estimated mission Delta-V: {result.estimated_delta_v:.2f} m/s")

print("\n========== STAGING ==========")

print(
    f"Gross lift-off mass: "
    f"{result.staging_result.gross_lift_off_mass:.2f} kg"
)

print(
    f"Payload fraction: "
    f"{100 * result.staging_result.payload_fraction:.3f} %"
)

for index, delta_v in enumerate(result.staging_result.stage_delta_v, start=1):
    print(f"\nStage {index}")

    print(f"  Delta-V: {delta_v:.2f} m/s")

    print(
        f"  Stage mass: "
        f"{result.staging_result.stage_masses[index - 1]:.2f} kg"
    )

    print(
        f"  Structural mass: "
        f"{result.staging_result.structural_masses[index - 1]:.2f} kg"
    )

    print(
        f"  Propellant mass: "
        f"{result.staging_result.propellant_masses[index - 1]:.2f} kg"
    )

print("\n======================================")