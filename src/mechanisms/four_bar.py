from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, sin, sqrt


Point = tuple[float, float]


@dataclass(frozen=True)
class FourBarConfig:
    """Lengths and assembly mode for a planar four-bar linkage.

    The ground link is placed from A=(0, 0) to D=(ground, 0).
    The crank rotates around A. The rocker rotates around D.
    """

    ground: float
    crank: float
    coupler: float
    rocker: float
    assembly: str = "open"

    def validate(self) -> None:
        if min(self.ground, self.crank, self.coupler, self.rocker) <= 0:
            raise ValueError("All link lengths must be positive.")
        if self.assembly not in {"open", "crossed"}:
            raise ValueError('assembly must be either "open" or "crossed".')


@dataclass(frozen=True)
class FourBarState:
    input_angle: float
    rocker_angle: float
    transmission_angle: float
    a: Point
    b: Point
    c: Point
    d: Point


def solve_four_bar(config: FourBarConfig, input_angle: float) -> FourBarState:
    """Solve joint positions for a four-bar linkage at a given crank angle."""

    config.validate()

    a = (0.0, 0.0)
    d = (config.ground, 0.0)
    b = (
        config.crank * cos(input_angle),
        config.crank * sin(input_angle),
    )

    c = _circle_intersection(
        center_0=b,
        radius_0=config.coupler,
        center_1=d,
        radius_1=config.rocker,
        assembly=config.assembly,
    )

    rocker_angle = atan2(c[1] - d[1], c[0] - d[0])
    coupler_angle = atan2(c[1] - b[1], c[0] - b[0])
    transmission_angle = _wrapped_angle(coupler_angle - rocker_angle)

    return FourBarState(
        input_angle=input_angle,
        rocker_angle=rocker_angle,
        transmission_angle=transmission_angle,
        a=a,
        b=b,
        c=c,
        d=d,
    )


def _circle_intersection(
    center_0: Point,
    radius_0: float,
    center_1: Point,
    radius_1: float,
    assembly: str,
) -> Point:
    x0, y0 = center_0
    x1, y1 = center_1
    dx = x1 - x0
    dy = y1 - y0
    distance = sqrt(dx * dx + dy * dy)

    if distance == 0:
        raise ValueError("Circle centers coincide; linkage state is singular.")
    if distance > radius_0 + radius_1 or distance < abs(radius_0 - radius_1):
        raise ValueError("No real four-bar solution for this angle and lengths.")

    along = (radius_0 * radius_0 - radius_1 * radius_1 + distance * distance) / (
        2 * distance
    )
    height_squared = max(radius_0 * radius_0 - along * along, 0.0)
    height = sqrt(height_squared)

    base_x = x0 + along * dx / distance
    base_y = y0 + along * dy / distance

    offset_x = -dy * height / distance
    offset_y = dx * height / distance

    if assembly == "open":
        return (base_x + offset_x, base_y + offset_y)
    return (base_x - offset_x, base_y - offset_y)


def _wrapped_angle(angle: float) -> float:
    while angle <= -3.141592653589793:
        angle += 6.283185307179586
    while angle > 3.141592653589793:
        angle -= 6.283185307179586
    return angle

