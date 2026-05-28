from __future__ import annotations

from manim import GREY_A, GREY_B, Line, VGroup, VMobject
import numpy as np


def wall(x: float, y_min: float, y_max: float) -> VGroup:
    line = Line([x, y_min, 0], [x, y_max, 0], color=GREY_A, stroke_width=6)
    hatches = VGroup()
    y = y_min + 0.15
    while y < y_max:
        hatches.add(Line([x - 0.2, y - 0.12, 0], [x, y + 0.08, 0], color=GREY_B))
        y += 0.3
    return VGroup(line, hatches)


def spring(start, end, coils: int = 10, amplitude: float = 0.16, color=GREY_A) -> VMobject:
    start_v = np.array(start, dtype=float)
    end_v = np.array(end, dtype=float)
    axis = end_v - start_v
    length = np.linalg.norm(axis)
    if length == 0:
        return VMobject()

    direction = axis / length
    normal = np.array([-direction[1], direction[0], 0.0])
    lead = min(0.18, length * 0.12)
    points = [start_v, start_v + direction * lead]

    zigzag_count = coils * 2
    usable = max(length - 2 * lead, 0.001)
    for i in range(1, zigzag_count):
        alpha = i / zigzag_count
        sign = 1 if i % 2 else -1
        points.append(start_v + direction * (lead + alpha * usable) + normal * amplitude * sign)

    points.extend([end_v - direction * lead, end_v])
    return VMobject(color=color, stroke_width=4).set_points_as_corners(points)

