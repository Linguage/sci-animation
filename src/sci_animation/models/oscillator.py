from __future__ import annotations

from dataclasses import dataclass
from math import cos, sqrt

import numpy as np

from sci_animation.schemas import TimeResponse


@dataclass(frozen=True)
class OscillatorConfig:
    mass: float = 1.0
    stiffness: float = 4.0
    amplitude: float = 1.0
    phase: float = 0.0

    def validate(self) -> None:
        if self.mass <= 0:
            raise ValueError("mass must be positive.")
        if self.stiffness <= 0:
            raise ValueError("stiffness must be positive.")
        if self.amplitude < 0:
            raise ValueError("amplitude must be non-negative.")

    @property
    def natural_frequency(self) -> float:
        self.validate()
        return sqrt(self.stiffness / self.mass)


def displacement(config: OscillatorConfig, time: float) -> float:
    omega = config.natural_frequency
    return config.amplitude * cos(omega * time + config.phase)


def acceleration(config: OscillatorConfig, time: float) -> float:
    omega = config.natural_frequency
    return -(omega * omega) * displacement(config, time)


def solve_free_response(
    config: OscillatorConfig,
    duration: float = 8.0,
    dt: float = 0.02,
) -> TimeResponse:
    config.validate()
    if duration <= 0:
        raise ValueError("duration must be positive.")
    if dt <= 0:
        raise ValueError("dt must be positive.")

    time = np.arange(0.0, duration + 0.5 * dt, dt)
    omega = config.natural_frequency
    x = config.amplitude * np.cos(omega * time + config.phase)
    a = -(omega * omega) * x
    return TimeResponse(
        time=time,
        values={"x": x, "a": a},
        units={"x": "m", "a": "m/s^2"},
        labels={"x": "x", "a": "a"},
        metadata={
            "mass": config.mass,
            "stiffness": config.stiffness,
            "amplitude": config.amplitude,
            "phase": config.phase,
            "natural_frequency": omega,
        },
    )

