"""Rocket-equation-based staging optimization."""

from dataclasses import dataclass
from math import isfinite, log

from pypropulsion.constants import STANDARD_GRAVITY


@dataclass(frozen=True)
class StageAssumption:
    """Input assumptions for one rocket stage."""

    name: str
    specific_impulse: float  # s
    structural_ratio: float  # dry mass / total stage mass

    def __post_init__(self) -> None:
        if self.specific_impulse <= 0.0:
            raise ValueError("Specific impulse must be positive.")

        if not 0.0 < self.structural_ratio < 1.0:
            raise ValueError("Structural ratio must be between 0 and 1.")


@dataclass(frozen=True)
class OptimizedStagingResult:
    """Optimized multistage vehicle result."""

    required_delta_v: float
    payload_mass: float
    gross_lift_off_mass: float
    payload_fraction: float
    lagrange_multiplier: float
    stage_mass_ratios: tuple[float, ...]
    stage_payload_ratios: tuple[float, ...]
    stage_delta_v: tuple[float, ...]
    stage_masses: tuple[float, ...]
    structural_masses: tuple[float, ...]
    propellant_masses: tuple[float, ...]


def _delta_v_residual(
    lagrange_multiplier: float,
    exhaust_velocities: tuple[float, ...],
    structural_ratios: tuple[float, ...],
    required_delta_v: float,
) -> float:
    """Return difference between required and achieved Delta-V."""
    mass_ratios = tuple(
        (1.0 + lagrange_multiplier * c)
        / (lagrange_multiplier * c * epsilon)
        for c, epsilon in zip(exhaust_velocities, structural_ratios, strict=True)
    )

    achieved_delta_v = sum(
        c * log(mass_ratio)
        for c, mass_ratio in zip(exhaust_velocities, mass_ratios, strict=True)
    )

    return required_delta_v - achieved_delta_v


def _solve_lagrange_multiplier(
    required_delta_v: float,
    exhaust_velocities: tuple[float, ...],
    structural_ratios: tuple[float, ...],
    tolerance: float = 1.0e-6,
    max_iterations: int = 100,
) -> float:
    """Solve staging Lagrange multiplier using Newton-Raphson iteration."""
    initial_guess = -1.0 / min(
        c * (1.0 - epsilon)
        for c, epsilon in zip(exhaust_velocities, structural_ratios, strict=True)
    )

    p = initial_guess

    for _ in range(max_iterations):
        residual = _delta_v_residual(
            p,
            exhaust_velocities,
            structural_ratios,
            required_delta_v,
        )

        if abs(residual) < tolerance:
            return p

        derivative = sum(c / p / (1.0 + p * c) for c in exhaust_velocities)

        if derivative == 0.0:
            raise RuntimeError("Newton-Raphson derivative became zero.")

        p -= residual / derivative

        if not isfinite(p):
            raise RuntimeError("Failed to solve staging optimization.")

    raise RuntimeError("Staging optimization did not converge.")


def optimize_staging(
    required_delta_v: float,
    payload_mass: float,
    stages: tuple[StageAssumption, ...],
) -> OptimizedStagingResult:
    """Optimize multistage rocket masses for a required Delta-V."""
    if required_delta_v <= 0.0:
        raise ValueError("Required Delta-V must be positive.")

    if payload_mass <= 0.0:
        raise ValueError("Payload mass must be positive.")

    if not stages:
        raise ValueError("At least one stage must be provided.")

    exhaust_velocities = tuple(
        stage.specific_impulse * STANDARD_GRAVITY for stage in stages
    )
    structural_ratios = tuple(stage.structural_ratio for stage in stages)

    lagrange_multiplier = _solve_lagrange_multiplier(
        required_delta_v,
        exhaust_velocities,
        structural_ratios,
    )

    stage_mass_ratios = tuple(
        (1.0 + lagrange_multiplier * c)
        / (lagrange_multiplier * c * epsilon)
        for c, epsilon in zip(exhaust_velocities, structural_ratios, strict=True)
    )

    stage_payload_ratios = tuple(
        (mass_ratio * epsilon - 1.0) / (1.0 - mass_ratio)
        for mass_ratio, epsilon in zip(stage_mass_ratios, structural_ratios, strict=True)
    )

    stage_masses_reversed: list[float] = []
    upper_mass = payload_mass

    for payload_ratio in reversed(stage_payload_ratios):
        stage_mass = upper_mass / payload_ratio
        stage_masses_reversed.append(stage_mass)
        upper_mass += stage_mass

    stage_masses = tuple(reversed(stage_masses_reversed))

    structural_masses = tuple(
        epsilon * stage_mass
        for epsilon, stage_mass in zip(structural_ratios, stage_masses, strict=True)
    )

    propellant_masses = tuple(
        stage_mass - structural_mass
        for stage_mass, structural_mass in zip(
            stage_masses, structural_masses, strict=True
        )
    )

    stage_delta_v = tuple(
        c * log(mass_ratio)
        for c, mass_ratio in zip(exhaust_velocities, stage_mass_ratios, strict=True)
    )

    gross_lift_off_mass = payload_mass + sum(stage_masses)
    payload_fraction = payload_mass / gross_lift_off_mass

    return OptimizedStagingResult(
        required_delta_v=required_delta_v,
        payload_mass=payload_mass,
        gross_lift_off_mass=gross_lift_off_mass,
        payload_fraction=payload_fraction,
        lagrange_multiplier=lagrange_multiplier,
        stage_mass_ratios=stage_mass_ratios,
        stage_payload_ratios=stage_payload_ratios,
        stage_delta_v=stage_delta_v,
        stage_masses=stage_masses,
        structural_masses=structural_masses,
        propellant_masses=propellant_masses,
    )