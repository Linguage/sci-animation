from __future__ import annotations

from pathlib import Path
import sys

from manim import *

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from _helpers import require_tex_toolchain
from sci_animation.models import OscillatorConfig, solve_free_response
from sci_animation.viz import LiveValuePanel, TimeHistoryPlot, spring, wall


class SpringOscillatorScene(Scene):
    def construct(self) -> None:
        require_tex_toolchain()

        config = OscillatorConfig(mass=1.0, stiffness=4.0, amplitude=1.0)
        duration = 8.0
        response = solve_free_response(config, duration=duration, dt=0.02)
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

        wall_mobject = wall(wall_x, -2.25, 1.6)
        guide = DashedLine(
            [origin[0] + 0.2, origin[1] - 1.05, 0],
            [origin[0] + 3.8, origin[1] - 1.05, 0],
            color=GREY_D,
            dash_length=0.12,
        )

        mass = always_redraw(
            lambda: Square(side_length=0.72, color=BLUE_C, fill_opacity=0.88)
            .set_stroke(WHITE, width=2)
            .move_to(self._mass_center(response, t, mass_center_x, origin[1], motion_scale))
        )
        spring_mobject = always_redraw(
            lambda: spring(
                [wall_x + 0.18, origin[1], 0],
                self._mass_center(response, t, mass_center_x, origin[1], motion_scale)
                + LEFT * 0.36,
                coils=10,
                amplitude=0.16,
                color=GREY_A,
            )
        )
        displacement_arrow = always_redraw(
            lambda: self._displacement_arrow(response, t, mass_center_x, origin[1], motion_scale)
        )

        label_group = always_redraw(
            lambda: LiveValuePanel(
                response=response,
                tracker=t,
                rows=[("t", "time", "s"), ("x", "x", "m"), ("a", "a", "m/s^2")],
                colors={"time": WHITE, "x": BLUE_C, "a": ORANGE},
                font_size=20,
            ).to_corner(DL, buff=0.45)
        )

        plot_x = TimeHistoryPlot(
            response=response,
            tracker=t,
            channels=["x"],
            title=r"x(t)",
            colors=[BLUE_C],
            y_range=(-1.25, 1.25, 1),
            x_length=4.6,
            y_length=1.75,
        )
        plot_x.move_to(RIGHT * 2.25 + UP * 0.65)
        plot_a = TimeHistoryPlot(
            response=response,
            tracker=t,
            channels=["a"],
            title=r"\ddot{x}(t)",
            colors=[ORANGE],
            y_range=(-4.8, 4.8, 4),
            x_length=4.6,
            y_length=1.75,
        )
        plot_a.move_to(RIGHT * 2.25 + DOWN * 1.65)

        self.play(FadeIn(title), FadeIn(formula))
        self.play(Create(wall_mobject), Create(guide), Create(spring_mobject), FadeIn(mass))
        self.play(
            FadeIn(displacement_arrow),
            FadeIn(label_group),
            Create(plot_x),
            Create(plot_a),
        )
        self.play(t.animate.set_value(duration), run_time=duration, rate_func=linear)
        self.wait(0.5)

    def _mass_center(self, response, tracker, base_x, y, scale):
        x = response.value_at("x", tracker.get_value())
        return [base_x + scale * x, y, 0]

    def _displacement_arrow(self, response, tracker, base_x, y, scale):
        x = response.value_at("x", tracker.get_value())
        start = [base_x, y - 0.85, 0]
        end = [base_x + scale * x, y - 0.85, 0]
        arrow = DoubleArrow(start, end, color=BLUE_C, buff=0, stroke_width=4, tip_length=0.14)
        label = MathTex("x", font_size=28, color=BLUE_C).next_to(arrow, DOWN, buff=0.08)
        return VGroup(arrow, label)
