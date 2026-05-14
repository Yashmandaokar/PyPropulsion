"""Top-level mission analysis workflow."""

from dataclasses import dataclass

from pypropulsion.mission.delta_v import estimate_leo_delta_v
from pypropulsion.mission.mission_requirements import MissionRequirement
from pypropulsion.mission.orbit import circular_orbit_velocity
from pypropulsion.mission.staging import (
    OptimizedStagingResult,
    StageAssumption,
    optimize_staging,
)

@dataclass(frozen=True)
class MissionAnalysisResult:
    """Summary of mission-level analysis."""

    orbital_velocity: float
    estimated_delta_v: float
    staging_result: OptimizedStagingResult

def analyze_mission(mission: MissionRequirement) -> MissionAnalysisResult:
    """Analyze a mission requirement and return first-order mission outputs."""
    orbital_velocity = circular_orbit_velocity(mission.target_orbit_altitude)

    estimated_delta_v = estimate_leo_delta_v(
        orbit_altitude=mission.target_orbit_altitude
    )

    stages = (
        StageAssumption("Stage 1", specific_impulse=305.0, structural_ratio=0.15),
        StageAssumption("Stage 2", specific_impulse=325.0, structural_ratio=0.14),
    )

    staging_result = optimize_staging(
        required_delta_v=estimated_delta_v,
        payload_mass=mission.payload_mass,
        stages=stages,
    )

    return MissionAnalysisResult(
        orbital_velocity=orbital_velocity,
        estimated_delta_v=estimated_delta_v,
        staging_result=staging_result,
    )