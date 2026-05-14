import pytest

from pypropulsion.mission.staging import StageAssumption, optimize_staging


def test_two_stage_optimized_staging():
    stages = (
        StageAssumption("Stage 1", specific_impulse=305.0, structural_ratio=0.15),
        StageAssumption("Stage 2", specific_impulse=325.0, structural_ratio=0.14),
    )

    result = optimize_staging(
        required_delta_v=9_500.0,
        payload_mass=300.0,
        stages=stages,
    )

    assert result.gross_lift_off_mass > result.payload_mass
    assert result.payload_fraction > 0.0
    assert len(result.stage_delta_v) == 2
    assert abs(sum(result.stage_delta_v) - 9_500.0) < 1.0e-3


def test_invalid_structural_ratio_raises_error():
    with pytest.raises(ValueError):
        StageAssumption(
            name="Bad stage",
            specific_impulse=300.0,
            structural_ratio=1.2,
        )


def test_invalid_payload_mass_raises_error():
    stages = (
        StageAssumption("Stage 1", specific_impulse=305.0, structural_ratio=0.15),
    )

    with pytest.raises(ValueError):
        optimize_staging(
            required_delta_v=9_500.0,
            payload_mass=-1.0,
            stages=stages,
        )


def test_no_stages_raises_error():
    with pytest.raises(ValueError):
        optimize_staging(
            required_delta_v=9_500.0,
            payload_mass=300.0,
            stages=(),
        )