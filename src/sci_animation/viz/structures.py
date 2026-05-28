from __future__ import annotations

from manim import BLUE_C, GREY_A, Line, Rectangle, VGroup
import numpy as np

from sci_animation.schemas import TimeResponse


def shear_building_mobject(
    response: TimeResponse,
    tracker,
    origin,
    story_height: float,
    bay_width: float,
    disp_scale: float,
) -> VGroup:
    floor_channels = sorted(
        [name for name in response.values if name.startswith("u") and name[1:].isdigit()],
        key=lambda name: int(name[1:]),
    )
    now = tracker.get_value()
    xs = [response.value_at(channel, now) * disp_scale for channel in floor_channels]
    floor_y = [origin[1] + story_height * (i + 1) for i in range(len(floor_channels))]
    base_left = np.array([origin[0] - bay_width / 2, origin[1], 0.0])
    base_right = np.array([origin[0] + bay_width / 2, origin[1], 0.0])

    group = VGroup()
    previous_left = base_left
    previous_right = base_right
    for x_shift, y in zip(xs, floor_y):
        center_x = origin[0] + x_shift
        left = np.array([center_x - bay_width / 2, y, 0.0])
        right = np.array([center_x + bay_width / 2, y, 0.0])
        slab = Rectangle(width=bay_width + 0.26, height=0.16, color=BLUE_C, fill_opacity=0.85)
        slab.move_to([center_x, y, 0.0])
        columns = VGroup(
            Line(previous_left, left, color=GREY_A, stroke_width=5),
            Line(previous_right, right, color=GREY_A, stroke_width=5),
        )
        group.add(columns, slab)
        previous_left = left
        previous_right = right

    return group

