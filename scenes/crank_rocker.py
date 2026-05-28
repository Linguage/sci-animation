from __future__ import annotations

from math import pi
from pathlib import Path
import sys

from manim import *

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mechanisms import FourBarConfig, solve_four_bar
from _helpers import require_tex_toolchain


class CrankRockerScene(Scene):
    def construct(self) -> None:
        require_tex_toolchain()

        config = FourBarConfig(
            ground=4.8,
            crank=1.25,
            coupler=3.8,
            rocker=3.0,
            assembly="open",
        )

        scale = 1.15
        origin = LEFT * 2.6 + DOWN * 1.0
        angle = ValueTracker(25 * DEGREES)

        title = Text("Crank-rocker linkage", font_size=34)
        title.to_edge(UP, buff=0.35)

        subtitle = Text("input crank drives an oscillating rocker", font_size=20)
        subtitle.next_to(title, DOWN, buff=0.12)
        subtitle.set_color(GREY_B)

        ground_line = self._line(
            lambda: self._p(solve_four_bar(config, angle.get_value()).a, origin, scale),
            lambda: self._p(solve_four_bar(config, angle.get_value()).d, origin, scale),
            GREY_B,
            8,
        )

        crank = self._link(lambda: self._state_point(config, angle, "a", origin, scale),
                           lambda: self._state_point(config, angle, "b", origin, scale),
                           BLUE_C, 10)
        coupler = self._link(lambda: self._state_point(config, angle, "b", origin, scale),
                             lambda: self._state_point(config, angle, "c", origin, scale),
                             TEAL_C, 10)
        rocker = self._link(lambda: self._state_point(config, angle, "d", origin, scale),
                            lambda: self._state_point(config, angle, "c", origin, scale),
                            ORANGE, 10)

        joints = VGroup(
            self._joint(lambda: self._state_point(config, angle, "a", origin, scale), "A"),
            self._joint(lambda: self._state_point(config, angle, "b", origin, scale), "B"),
            self._joint(lambda: self._state_point(config, angle, "c", origin, scale), "C"),
            self._joint(lambda: self._state_point(config, angle, "d", origin, scale), "D"),
        )

        trace = TracedPath(
            lambda: self._state_point(config, angle, "c", origin, scale),
            stroke_color=YELLOW,
            stroke_width=3,
            dissipating_time=0,
        )

        input_arrow = always_redraw(
            lambda: CurvedArrow(
                self._state_point(config, angle, "a", origin, scale) + RIGHT * 0.9,
                self._state_point(config, angle, "a", origin, scale) + UP * 0.9,
                radius=-0.65,
                color=BLUE_B,
                stroke_width=4,
            )
        )

        rocker_angle_label = always_redraw(
            lambda: self._rocker_label(config, angle, origin, scale)
        )

        legend = VGroup(
            self._legend_item(BLUE_C, "crank"),
            self._legend_item(TEAL_C, "coupler"),
            self._legend_item(ORANGE, "rocker"),
            self._legend_item(YELLOW, "point C path"),
        )
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        legend.to_corner(DR, buff=0.45)

        self.play(FadeIn(title), FadeIn(subtitle), Create(ground_line))
        self.play(Create(crank), Create(coupler), Create(rocker), FadeIn(joints))
        self.add(trace, input_arrow, rocker_angle_label, legend)
        self.play(angle.animate.set_value(385 * DEGREES), run_time=8, rate_func=linear)
        self.wait(0.5)

    def _state_point(self, config, angle, name: str, origin, scale):
        state = solve_four_bar(config, angle.get_value())
        return self._p(getattr(state, name), origin, scale)

    def _p(self, point, origin, scale):
        x, y = point
        return origin + RIGHT * (x * scale) + UP * (y * scale)

    def _link(self, start_getter, end_getter, color, width):
        return always_redraw(
            lambda: Line(
                start_getter(),
                end_getter(),
                color=color,
                stroke_width=width,
            )
        )

    def _line(self, start_getter, end_getter, color, width):
        return always_redraw(
            lambda: Line(
                start_getter(),
                end_getter(),
                color=color,
                stroke_width=width,
            )
        )

    def _joint(self, point_getter, label: str):
        dot = always_redraw(lambda: Dot(point_getter(), radius=0.08, color=WHITE))
        text = always_redraw(
            lambda: Text(label, font_size=18)
            .next_to(dot, DOWN if label in {"A", "D"} else UP, buff=0.08)
        )
        return VGroup(dot, text)

    def _rocker_label(self, config, angle, origin, scale):
        state = solve_four_bar(config, angle.get_value())
        pivot = self._p(state.d, origin, scale)
        label = MathTex(r"\theta_{out}", font_size=28, color=ORANGE)
        label.next_to(pivot + UP * 0.55 + LEFT * 0.25, RIGHT, buff=0.08)
        value = DecimalNumber(state.rocker_angle / pi * 180, num_decimal_places=1)
        value.set_color(ORANGE).scale(0.45)
        degree = Text("deg", font_size=16, color=ORANGE)
        group = VGroup(label, value, degree).arrange(RIGHT, buff=0.08)
        group.move_to(pivot + UP * 0.95 + LEFT * 0.1)
        return group

    def _legend_item(self, color, text):
        swatch = Line(ORIGIN, RIGHT * 0.45, color=color, stroke_width=7)
        label = Text(text, font_size=18, color=GREY_A)
        return VGroup(swatch, label).arrange(RIGHT, buff=0.16)
