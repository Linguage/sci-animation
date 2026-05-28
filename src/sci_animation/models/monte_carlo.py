from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from sci_animation.schemas import TimeResponse


@dataclass(frozen=True)
class MonteCarloPiConfig:
    samples: int = 800
    seed: int = 42

    def validate(self) -> None:
        if self.samples <= 0:
            raise ValueError("samples must be positive.")


@dataclass(frozen=True)
class MonteCarloPiResult:
    x: np.ndarray
    y: np.ndarray
    inside: np.ndarray
    estimate: np.ndarray

    @property
    def samples(self) -> int:
        return len(self.estimate)


def simulate_pi(config: MonteCarloPiConfig) -> MonteCarloPiResult:
    config.validate()
    rng = np.random.default_rng(config.seed)
    x = rng.uniform(-1.0, 1.0, config.samples)
    y = rng.uniform(-1.0, 1.0, config.samples)
    inside = x * x + y * y <= 1.0
    counts = np.cumsum(inside)
    sample_numbers = np.arange(1, config.samples + 1)
    estimate = 4.0 * counts / sample_numbers
    return MonteCarloPiResult(x=x, y=y, inside=inside, estimate=estimate)


def to_time_response(result: MonteCarloPiResult) -> TimeResponse:
    sample_numbers = np.arange(1, result.samples + 1, dtype=float)
    return TimeResponse(
        time=sample_numbers,
        values={"pi_hat": result.estimate},
        units={"pi_hat": ""},
        labels={"pi_hat": "pi estimate"},
        metadata={"samples": result.samples},
    )

