from __future__ import annotations

from pathlib import Path
import sys

from manim import *
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from _helpers import require_tex_toolchain
from mechanisms import ShearBuildingConfig, solve_earthquake_response


class ThreeStoryEarthquakeScene(Scene):
    def construct(self) -> None:
        require_tex_toolchain()

        config = ShearBuildingConfig(
            masses=(1.0, 1.0, 1.0),
            story_stiffnesses=(90.0, 80.0, 70.0),
            damping_ratio=0.05,
        )
        response = solve_earthquake_response(config, duration=8.0, dt=0.02)
        duration = float(response.time[-1])
        tracker = ValueTracker(0.0)

        title = Text("Three-story shear building under earthquake excitation", font_size=29)
        title.to_edge(UP, buff=0.26)
        equation = MathTex(
            r"M\ddot{u}+C\dot{u}+Ku=-M\mathbf{1}\ddot{u}_g(t)",
            font_size=30,
        )
        equation.next_to(title, DOWN, buff=0.12)

        building_origin = LEFT * 4.1 + DOWN * 2.1
        story_height = 1.05
        bay_width = 1.95
        disp_scale = 10.0
        ground_scale = 0.18

        building = always_redraw(
            lambda: self._building(response, tracker, building_origin, story_height, bay_width, disp_scale)
        )
        ground = always_redraw(
            lambda: self._ground(response, tracker, building_origin, bay_width, ground_scale)
        )
        floor_labels = always_redraw(
            lambda: self._floor_values(response, tracker).to_corner(DL, buff=0.35)
        )

        axes, curves, dots = self._response_plot(response, tracker)
        ground_axes, ground_curve, ground_dot = self._ground_plot(response, tracker)

        legend = self._legend()
        legend.next_to(axes, DOWN, buff=0.26).align_to(axes, LEFT)

        self.play(FadeIn(title), FadeIn(equation))
        self.play(Create(ground), Create(building), FadeIn(floor_labels))
        self.play(Create(axes), Create(ground_axes), FadeIn(legend))
        self.add(*curves, *dots, ground_curve, ground_dot)
        self.play(tracker.animate.set_value(duration), run_time=duration, rate_func=linear)
        self.wait(0.5)

    def _building(self, response, tracker, origin, story_height, bay_width, disp_scale):
        now = tracker.get_value()
        xs = [self._floor_disp(response, floor, now) * disp_scale for floor in range(3)]
        floor_y = [origin[1] + story_height * (i + 1) for i in range(3)]
        base_left = np.array([origin[0] - bay_width / 2, origin[1], 0.0])
        base_right = np.array([origin[0] + bay_width / 2, origin[1], 0.0])

        group = VGroup()
        previous_left = base_left
        previous_right = base_right

        for i, y in enumerate(floor_y):
            center_x = origin[0] + xs[i]
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

        roof_drift = xs[-1]
        drift_arrow = Arrow(
            [origin[0], floor_y[-1] + 0.45, 0],
            [origin[0] + roof_drift, floor_y[-1] + 0.45, 0],
            buff=0,
            color=YELLOW,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.28,
        )
        drift_label = MathTex(r"u_3(t)", font_size=24, color=YELLOW)
        drift_label.next_to(drift_arrow, UP, buff=0.06)
        group.add(drift_arrow, drift_label)
        return group

    def _ground(self, response, tracker, origin, bay_width, ground_scale):
        now = tracker.get_value()
        ag = self._ground_acc(response, now)
        shift = ground_scale * ag
        ground_line = Line(
            [origin[0] - bay_width * 0.85 + shift, origin[1] - 0.08, 0],
            [origin[0] + bay_width * 0.85 + shift, origin[1] - 0.08, 0],
            color=GREY_B,
            stroke_width=8,
        )
        arrow = Arrow(
            [origin[0] - 0.75, origin[1] - 0.5, 0],
            [origin[0] - 0.75 + shift, origin[1] - 0.5, 0],
            buff=0,
            color=RED_C,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.35,
        )
        label = MathTex(r"\ddot{u}_g", font_size=24, color=RED_C)
        label.next_to(arrow, DOWN, buff=0.08)
        return VGroup(ground_line, arrow, label)

    def _floor_values(self, response, tracker):
        now = tracker.get_value()
        rows = [self._value_row("t", now, "s", WHITE)]
        colors = [BLUE_C, TEAL_C, ORANGE]
        for floor in range(3):
            rows.append(
                self._value_row(
                    f"u{floor + 1}",
                    self._floor_disp(response, floor, now),
                    "m",
                    colors[floor],
                )
            )
        group = VGroup(*rows)
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        return group

    def _value_row(self, name, value, unit, color):
        label = Text(f"{name} =", font_size=18, color=color)
        number = Text(f"{value:7.3f}", font_size=18, color=color)
        unit_text = Text(unit, font_size=16, color=GREY_B)
        return VGroup(label, number, unit_text).arrange(RIGHT, buff=0.06)

    def _response_plot(self, response, tracker):
        max_u = float(np.max(np.abs(response.displacement))) * 1.15
        max_u = max(max_u, 0.02)
        axes = Axes(
            x_range=(0, response.time[-1], 2),
            y_range=(-max_u, max_u, max_u / 2),
            x_length=5.0,
            y_length=2.55,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        )
        axes.move_to(RIGHT * 2.25 + UP * 0.35)
        title = MathTex(r"u_i(t)", font_size=26)
        title.next_to(axes, UP, buff=0.06)
        x_label = Text("time", font_size=16, color=GREY_B).next_to(axes.x_axis, RIGHT, buff=0.08)
        axes_group = VGroup(axes, title, x_label)

        colors = [BLUE_C, TEAL_C, ORANGE]
        curves = []
        dots = []
        for floor, color in enumerate(colors):
            curves.append(
                always_redraw(
                    lambda floor=floor, color=color: axes.plot(
                        lambda time: self._floor_disp(response, floor, time),
                        x_range=(0, max(tracker.get_value(), 0.001)),
                        color=color,
                        stroke_width=3.5,
                    )
                )
            )
            dots.append(
                always_redraw(
                    lambda floor=floor, color=color: Dot(
                        axes.c2p(
                            tracker.get_value(),
                            self._floor_disp(response, floor, tracker.get_value()),
                        ),
                        radius=0.048,
                        color=color,
                    )
                )
            )

        return axes_group, curves, dots

    def _ground_plot(self, response, tracker):
        max_ag = float(np.max(np.abs(response.ground_acceleration))) * 1.1
        axes = Axes(
            x_range=(0, response.time[-1], 2),
            y_range=(-max_ag, max_ag, max_ag),
            x_length=5.0,
            y_length=1.25,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        )
        axes.move_to(RIGHT * 2.25 + DOWN * 2.0)
        title = MathTex(r"\ddot{u}_g(t)", font_size=24, color=RED_C)
        title.next_to(axes, UP, buff=0.04)

        curve = always_redraw(
            lambda: axes.plot(
                lambda time: self._ground_acc(response, time),
                x_range=(0, max(tracker.get_value(), 0.001)),
                color=RED_C,
                stroke_width=3,
            )
        )
        dot = always_redraw(
            lambda: Dot(
                axes.c2p(tracker.get_value(), self._ground_acc(response, tracker.get_value())),
                radius=0.045,
                color=RED_C,
            )
        )
        return VGroup(axes, title), curve, dot

    def _legend(self):
        items = VGroup(
            self._legend_item(BLUE_C, "floor 1"),
            self._legend_item(TEAL_C, "floor 2"),
            self._legend_item(ORANGE, "floor 3"),
        )
        items.arrange(RIGHT, buff=0.28)
        return items

    def _legend_item(self, color, text):
        swatch = Line(ORIGIN, RIGHT * 0.32, color=color, stroke_width=6)
        label = Text(text, font_size=16, color=GREY_A)
        return VGroup(swatch, label).arrange(RIGHT, buff=0.08)

    def _floor_disp(self, response, floor, time):
        return float(np.interp(time, response.time, response.displacement[floor]))

    def _ground_acc(self, response, time):
        return float(np.interp(time, response.time, response.ground_acceleration))

