from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import numpy as np

from sci_animation.schemas import TimeResponse


def read_time_response_csv(
    path: str | Path,
    units: dict[str, str] | None = None,
    labels: dict[str, str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> TimeResponse:
    csv_path = Path(path)
    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError("CSV must contain a header row.")
        if "time" not in reader.fieldnames:
            raise ValueError('CSV must contain a "time" column.')

        channels = [name for name in reader.fieldnames if name != "time"]
        if not channels:
            raise ValueError("CSV must contain at least one response channel.")

        time: list[float] = []
        values: dict[str, list[float]] = {name: [] for name in channels}
        for row_number, row in enumerate(reader, start=2):
            try:
                time.append(float(row["time"]))
                for name in channels:
                    values[name].append(float(row[name]))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Non-numeric value in CSV row {row_number}.") from exc

    response_units = units or {name: "" for name in channels}
    return TimeResponse(
        time=np.array(time, dtype=float),
        values={name: np.array(data, dtype=float) for name, data in values.items()},
        units=response_units,
        labels=labels,
        metadata=metadata or {"source": str(csv_path)},
    )

