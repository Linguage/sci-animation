from __future__ import annotations

from pathlib import Path
import sys

from manim import *

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from _helpers import require_tex_toolchain
from sci_animation.models import MonteCarloPiConfig, monte_carlo_to_time_response, simulate_pi
from sci_animation.viz import TimeHistoryPlot


class MonteCarloPiScene(Scene):
    def construct(self) -> None:
        require_tex_toolchain()

        config = MonteCarloPiConfig(samples=800, seed=12)
        result = simulate_pi(config)
        response = monte_carlo_to_time_response(result)
        sample = ValueTracker(1.0)

        title = Text("Monte Carlo estimation of pi", font_size=32)
        title.to_edge(UP, buff=0.3)
        formula = Text("pi_hat = 4 * N_in / N    as N grows", font_size=24, color=GREY_A)
        formula.next_to(title, DOWN, buff=0.12)

        center = LEFT * 3.25 + DOWN * 0.2
        side = 3.25
        radius = side / 2
        square = Square(side_length=side, color=GREY_B).move_to(center)
        circle = Circle(radius=radius, color=BLUE_D).move_to(center)
        quadrant_label = MathTex(r"x^2+y^2\leq 1", font_size=24, color=BLUE_C)
        quadrant_label.next_to(square, DOWN, buff=0.18)

        points = always_redraw(lambda: self._sample_points(result, sample, center, radius))

        plot = TimeHistoryPlot(
            response=response,
            channels=["pi_hat"],
            tracker=sample,
            colors=[BLUE_C],
            title=r"\hat{\pi}(N)",
            x_length=4.8,
            y_length=2.65,
            y_range=(2.4, 4.0, 0.4),
            x_label="N",
        )
        plot.move_to(RIGHT * 2.75 + UP * 0.4)
        pi_reference = DashedLine(
            plot.axes.c2p(0, PI),
            plot.axes.c2p(config.samples, PI),
            color=YELLOW,
            dash_length=0.12,
            stroke_width=2.5,
        )
        pi_label = MathTex(r"\pi", font_size=24, color=YELLOW).next_to(pi_reference, RIGHT, buff=0.08)

        panel = always_redraw(lambda: self._stats_panel(result, response, sample).to_corner(DR, buff=0.55))

        self.play(FadeIn(title), FadeIn(formula))
        self.play(Create(square), Create(circle), FadeIn(quadrant_label), Create(plot), Create(pi_reference), FadeIn(pi_label))
        self.add(points, panel)
        self.play(sample.animate.set_value(config.samples), run_time=8.0, rate_func=linear)
        self.wait(0.5)

    def _sample_points(self, result, tracker, center, scale):
        count = max(1, min(result.samples, int(tracker.get_value())))
        dots = VGroup()
        for x, y, inside in zip(result.x[:count], result.y[:count], result.inside[:count]):
            color = BLUE_C if inside else ORANGE
            dots.add(Dot(center + RIGHT * (x * scale) + UP * (y * scale), radius=0.014, color=color))
        return dots

    def _stats_panel(self, result, response, tracker):
        count = max(1, min(result.samples, int(tracker.get_value())))
        inside_count = int(result.inside[:count].sum())
        pi_hat = response.value_at("pi_hat", count)
        rows = VGroup(
            Text(f"N = {count}", font_size=20, color=WHITE),
            Text(f"inside = {inside_count} / {count}", font_size=20, color=GREY_A),
            Text(f"pi_hat = {pi_hat:.4f}", font_size=20, color=BLUE_C),
        )
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        return rows
