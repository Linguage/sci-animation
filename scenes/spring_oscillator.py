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
from mechanisms import OscillatorConfig, acceleration, displacement


class SpringOscillatorScene(Scene):
    def construct(self) -> None:
        require_tex_toolchain()

        config = OscillatorConfig(mass=1.0, stiffness=4.0, amplitude=1.0)
        duration = 8.0
        t = ValueTracker(0.0)

        title = Text("Single-degree-of-freedom oscillator", font_size=32)
        title.to_edge(UP, buff=0.32)

        formula = MathTex(
            r"x(t)=A\cos(\omega_n t)",
            r"\quad",
            r"\ddot{x}(t)=-\omega_n^2x(t)",
            font_size=28,
        )
        formula.next_to(title, DOWN, buff=0.14)
        formula.set_color_by_tex(r"x(t)", BLUE_C)
        formula.set_color_by_tex(r"\ddot{x}", ORANGE)

        origin = LEFT * 4.3 + DOWN * 0.35
        wall_x = origin[0] - 0.45
        mass_center_x = origin[0] + 2.0
        motion_scale = 0.82
        spring_length = 2.0

        wall = self._wall(wall_x)
        guide = DashedLine(
            [origin[0] + 0.2, origin[1] - 1.05, 0],
            [origin[0] + 3.8, origin[1] - 1.05, 0],
            color=GREY_D,
            dash_length=0.12,
        )

        mass = always_redraw(
            lambda: Square(side_length=0.72, color=BLUE_C, fill_opacity=0.88)
            .set_stroke(WHITE, width=2)
            .move_to(self._mass_center(config, t, mass_center_x, origin[1], motion_scale))
        )
        spring = always_redraw(
            lambda: self._spring(
                [wall_x + 0.18, origin[1], 0],
                self._mass_center(config, t, mass_center_x, origin[1], motion_scale)
                + LEFT * 0.36,
                coils=10,
                amplitude=0.16,
                color=GREY_A,
            )
        )
        displacement_arrow = always_redraw(
            lambda: self._displacement_arrow(config, t, mass_center_x, origin[1], motion_scale)
        )

        label_group = always_redraw(
            lambda: self._live_values(config, t).to_corner(DL, buff=0.45)
        )

        axes_x, x_curve, x_dot = self._time_plot(
            config=config,
            tracker=t,
            value_func=displacement,
            title=r"x(t)",
            color=BLUE_C,
            y_range=(-1.25, 1.25, 1),
            center=RIGHT * 2.25 + UP * 0.65,
            duration=duration,
        )
        axes_a, a_curve, a_dot = self._time_plot(
            config=config,
            tracker=t,
            value_func=acceleration,
            title=r"\ddot{x}(t)",
            color=ORANGE,
            y_range=(-4.8, 4.8, 4),
            center=RIGHT * 2.25 + DOWN * 1.65,
            duration=duration,
        )

        self.play(FadeIn(title), FadeIn(formula))
        self.play(Create(wall), Create(guide), Create(spring), FadeIn(mass))
        self.play(
            FadeIn(displacement_arrow),
            FadeIn(label_group),
            Create(axes_x),
            Create(axes_a),
        )
        self.add(x_curve, a_curve, x_dot, a_dot)
        self.play(t.animate.set_value(duration), run_time=duration, rate_func=linear)
        self.wait(0.5)

    def _mass_center(self, config, tracker, base_x, y, scale):
        x = displacement(config, tracker.get_value())
        return [base_x + scale * x, y, 0]

    def _wall(self, x):
        line = Line([x, -2.25, 0], [x, 1.6, 0], color=GREY_A, stroke_width=6)
        hatches = VGroup()
        for y in [v / 10 for v in range(-21, 16, 3)]:
            hatches.add(Line([x - 0.2, y - 0.12, 0], [x, y + 0.08, 0], color=GREY_B))
        return VGroup(line, hatches)

    def _spring(self, start, end, coils, amplitude, color):
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

    def _displacement_arrow(self, config, tracker, base_x, y, scale):
        x = displacement(config, tracker.get_value())
        start = [base_x, y - 0.85, 0]
        end = [base_x + scale * x, y - 0.85, 0]
        arrow = DoubleArrow(start, end, color=BLUE_C, buff=0, stroke_width=4, tip_length=0.14)
        label = MathTex("x", font_size=28, color=BLUE_C).next_to(arrow, DOWN, buff=0.08)
        return VGroup(arrow, label)

    def _live_values(self, config, tracker):
        now = tracker.get_value()
        rows = VGroup(
            self._value_row("t", now, "s", WHITE),
            self._value_row("x", displacement(config, now), "m", BLUE_C),
            self._value_row("a", acceleration(config, now), "m/s^2", ORANGE),
        )
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        return rows

    def _value_row(self, name, value, unit, color):
        label = Text(f"{name} =", font_size=20, color=color)
        number = Text(f"{value:6.2f}", font_size=20, color=color)
        unit_text = Text(unit, font_size=18, color=GREY_B)
        return VGroup(label, number, unit_text).arrange(RIGHT, buff=0.08)

    def _time_plot(self, config, tracker, value_func, title, color, y_range, center, duration):
        axes = Axes(
            x_range=(0, duration, 2),
            y_range=y_range,
            x_length=4.6,
            y_length=1.75,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        )
        axes.move_to(center)

        title_mob = MathTex(title, font_size=24, color=color)
        title_mob.next_to(axes, UP, buff=0.08)
        x_label = Text("time", font_size=16, color=GREY_B).next_to(axes.x_axis, RIGHT, buff=0.08)

        curve = always_redraw(
            lambda: axes.plot(
                lambda time: value_func(config, time),
                x_range=(0, max(tracker.get_value(), 0.001)),
                color=color,
                stroke_width=4,
            )
        )
        dot = always_redraw(
            lambda: Dot(
                axes.c2p(tracker.get_value(), value_func(config, tracker.get_value())),
                radius=0.055,
                color=color,
            )
        )

        return VGroup(axes, title_mob, x_label), curve, dot
