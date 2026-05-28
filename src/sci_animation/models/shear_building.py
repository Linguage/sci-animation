from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from sci_animation.schemas import TimeResponse
from sci_animation.solvers import newmark_average_acceleration


@dataclass(frozen=True)
class ShearBuildingConfig:
    masses: tuple[float, ...] = (1.0, 1.0, 1.0)
    story_stiffnesses: tuple[float, ...] = (90.0, 80.0, 70.0)
    damping_ratio: float = 0.05

    def validate(self) -> None:
        if len(self.masses) == 0:
            raise ValueError("At least one floor is required.")
        if len(self.masses) != len(self.story_stiffnesses):
            raise ValueError("masses and story_stiffnesses must have the same length.")
        if min(self.masses) <= 0:
            raise ValueError("All masses must be positive.")
        if min(self.story_stiffnesses) <= 0:
            raise ValueError("All story stiffnesses must be positive.")
        if self.damping_ratio < 0:
            raise ValueError("damping_ratio must be non-negative.")


@dataclass(frozen=True)
class ShearBuildingResponse:
    time: np.ndarray
    ground_acceleration: np.ndarray
    displacement: np.ndarray
    velocity: np.ndarray
    acceleration: np.ndarray
    frequencies: np.ndarray


def mass_matrix(config: ShearBuildingConfig) -> np.ndarray:
    config.validate()
    return np.diag(np.array(config.masses, dtype=float))


def stiffness_matrix(config: ShearBuildingConfig) -> np.ndarray:
    config.validate()
    stiffnesses = np.array(config.story_stiffnesses, dtype=float)
    n = len(stiffnesses)
    matrix = np.zeros((n, n), dtype=float)

    for i in range(n):
        matrix[i, i] += stiffnesses[i]
        if i + 1 < n:
            matrix[i, i] += stiffnesses[i + 1]
            matrix[i, i + 1] -= stiffnesses[i + 1]
            matrix[i + 1, i] -= stiffnesses[i + 1]

    return matrix


def damping_matrix(config: ShearBuildingConfig, mass: np.ndarray, stiffness: np.ndarray) -> np.ndarray:
    frequencies = natural_frequencies(mass, stiffness)
    if config.damping_ratio == 0 or len(frequencies) == 0:
        return np.zeros_like(stiffness)

    if len(frequencies) == 1:
        alpha = 2 * config.damping_ratio * frequencies[0]
        beta = 0.0
    else:
        w1, w2 = frequencies[0], frequencies[1]
        beta = 2 * config.damping_ratio / (w1 + w2)
        alpha = beta * w1 * w2

    return alpha * mass + beta * stiffness


def natural_frequencies(mass: np.ndarray, stiffness: np.ndarray) -> np.ndarray:
    inv_sqrt_mass = np.diag(1.0 / np.sqrt(np.diag(mass)))
    dynamic_matrix = inv_sqrt_mass @ stiffness @ inv_sqrt_mass
    eigenvalues = np.linalg.eigvalsh(dynamic_matrix)
    return np.sqrt(np.maximum(eigenvalues, 0.0))


def synthetic_ground_acceleration(time: np.ndarray) -> np.ndarray:
    envelope = np.exp(-0.38 * time) * (1 - np.exp(-3.0 * time))
    waves = (
        3.2 * np.sin(2 * np.pi * 1.15 * time)
        + 1.6 * np.sin(2 * np.pi * 2.35 * time + 0.8)
        + 0.7 * np.sin(2 * np.pi * 4.10 * time + 1.4)
    )
    return envelope * waves


def solve_earthquake_response(
    config: ShearBuildingConfig,
    duration: float = 8.0,
    dt: float = 0.02,
) -> ShearBuildingResponse:
    config.validate()
    if duration <= 0:
        raise ValueError("duration must be positive.")
    if dt <= 0:
        raise ValueError("dt must be positive.")

    time = np.arange(0.0, duration + 0.5 * dt, dt)
    ground_acc = synthetic_ground_acceleration(time)

    mass = mass_matrix(config)
    stiffness = stiffness_matrix(config)
    damping = damping_matrix(config, mass, stiffness)
    frequencies = natural_frequencies(mass, stiffness)

    influence = np.ones(len(config.masses))
    force = -mass @ influence[:, None] * ground_acc[None, :]

    displacement, velocity, acceleration = newmark_average_acceleration(
        mass=mass,
        damping=damping,
        stiffness=stiffness,
        force=force,
        dt=dt,
    )

    return ShearBuildingResponse(
        time=time,
        ground_acceleration=ground_acc,
        displacement=displacement,
        velocity=velocity,
        acceleration=acceleration,
        frequencies=frequencies,
    )


def to_time_response(response: ShearBuildingResponse) -> TimeResponse:
    floor_count = response.displacement.shape[0]
    values = {f"u{i + 1}": response.displacement[i] for i in range(floor_count)}
    values["ag"] = response.ground_acceleration
    units = {f"u{i + 1}": "m" for i in range(floor_count)}
    units["ag"] = "m/s^2"
    labels = {f"u{i + 1}": f"u{i + 1}" for i in range(floor_count)}
    labels["ag"] = "ag"
    return TimeResponse(
        time=response.time,
        values=values,
        units=units,
        labels=labels,
        metadata={"frequencies": response.frequencies},
    )

