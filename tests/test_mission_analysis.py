from pypropulsion.mission import MissionRequirement, analyze_mission


def test_analyze_500km_sso_like_mission():
    mission = MissionRequirement(
        payload_mass=300.0,
        target_orbit_altitude=500_000.0,
        target_inclination=97.0,
        launch_site="Europe",
        mission_type="SSO",
    )

    result = analyze_mission(mission)

    assert 7_500.0 < result.orbital_velocity < 7_700.0
    assert 9_300.0 < result.estimated_delta_v < 9_500.0
    assert result.staging_result.payload_mass == 300.0
    assert result.staging_result.gross_lift_off_mass > result.staging_result.payload_mass
    assert len(result.staging_result.stage_delta_v) == 2
    assert abs(sum(result.staging_result.stage_delta_v) - result.estimated_delta_v) < 1.0e-3