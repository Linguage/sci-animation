from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import numpy as np


@dataclass(frozen=True)
class TimeResponse:
    time: np.ndarray
    values: dict[str, np.ndarray]
    units: dict[str, str]
    labels: dict[str, str] | None = None
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        time = np.asarray(self.time, dtype=float)
        if time.ndim != 1:
            raise ValueError("time must be a one-dimensional array.")
        if len(time) == 0:
            raise ValueError("time must not be empty.")
        if np.any(np.diff(time) <= 0):
            raise ValueError("time must be strictly increasing.")

        values: dict[str, np.ndarray] = {}
        for name, data in self.values.items():
            array = np.asarray(data, dtype=float)
            if array.ndim != 1:
                raise ValueError(f'values["{name}"] must be one-dimensional.')
            if len(array) != len(time):
                raise ValueError(f'values["{name}"] must have the same length as time.')
            values[name] = array

        missing_units = set(values) - set(self.units)
        if missing_units:
            missing = ", ".join(sorted(missing_units))
            raise ValueError(f"units missing for channel(s): {missing}")

        object.__setattr__(self, "time", time)
        object.__setattr__(self, "values", values)
        object.__setattr__(self, "labels", self.labels or {})
        object.__setattr__(self, "metadata", self.metadata or {})

    def channel(self, name: str) -> np.ndarray:
        try:
            return self.values[name]
        except KeyError as exc:
            raise KeyError(f'Unknown response channel "{name}".') from exc

    def value_at(self, name: str, time: float) -> float:
        return float(np.interp(time, self.time, self.channel(name)))

    def duration(self) -> float:
        return float(self.time[-1])

    def max_abs(self, names: Sequence[str] | None = None) -> float:
        selected = list(names) if names is not None else list(self.values)
        if not selected:
            return 0.0
        return max(float(np.max(np.abs(self.channel(name)))) for name in selected)

