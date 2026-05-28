from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GeometryState:
    points: dict[str, tuple[float, float]]
    metadata: dict[str, Any] | None = None

