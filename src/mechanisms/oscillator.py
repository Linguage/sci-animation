from __future__ import annotations

from dataclasses import dataclass
from math import cos, sqrt


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

