from __future__ import annotations

from dataclasses import dataclass
from math import comb

import numpy as np

from sci_animation.schemas import TimeResponse


@dataclass(frozen=True)
class GaltonBoardConfig:
    rows: int = 10
    balls: int = 160
    p: float = 0.5
    seed: int = 7

    def validate(self) -> None:
        if self.rows <= 0:
            raise ValueError("rows must be positive.")
        if self.balls <= 0:
            raise ValueError("balls must be positive.")
        if not 0.0 <= self.p <= 1.0:
            raise ValueError("p must be between 0 and 1.")


@dataclass(frozen=True)
class GaltonBoardResult:
    paths: np.ndarray
    bins: np.ndarray
    cumulative_counts: np.ndarray
    probabilities: np.ndarray
    p: float

    @property
    def rows(self) -> int:
        return self.paths.shape[1]

    @property
    def balls(self) -> int:
        return self.paths.shape[0]


def simulate_galton_board(config: GaltonBoardConfig) -> GaltonBoardResult:
    config.validate()
    rng = np.random.default_rng(config.seed)
    paths = rng.random((config.balls, config.rows)) < config.p
    final_slots = paths.sum(axis=1).astype(int)
    bins = np.bincount(final_slots, minlength=config.rows + 1)

    cumulative_counts = np.zeros((config.balls, config.rows + 1), dtype=float)
    running = np.zeros(config.rows + 1, dtype=float)
    for index, slot in enumerate(final_slots):
        running[slot] += 1.0
        cumulative_counts[index] = running

    probabilities = np.array(
        [
            comb(config.rows, slot)
            * (config.p**slot)
            * ((1.0 - config.p) ** (config.rows - slot))
            for slot in range(config.rows + 1)
        ],
        dtype=float,
    )

    return GaltonBoardResult(
        paths=paths,
        bins=bins.astype(float),
        cumulative_counts=cumulative_counts,
        probabilities=probabilities,
        p=config.p,
    )


def to_time_response(result: GaltonBoardResult) -> TimeResponse:
    sample_numbers = np.arange(1, result.balls + 1, dtype=float)
    values = {
        f"bin_{slot:02d}": result.cumulative_counts[:, slot]
        for slot in range(result.rows + 1)
    }
    units = {name: "balls" for name in values}
    labels = {f"bin_{slot:02d}": f"slot {slot}" for slot in range(result.rows + 1)}
    return TimeResponse(
        time=sample_numbers,
        values=values,
        units=units,
        labels=labels,
        metadata={"rows": result.rows, "balls": result.balls, "p": result.p},
    )
