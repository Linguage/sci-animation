from __future__ import annotations

from math import exp, pi, sqrt
from pathlib import Path
import sys

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from _helpers import require_tex_toolchain
from sci_animation.models import GaltonBoardConfig, simulate_galton_board


class GaltonBoardScene(Scene):
    def construct(self) -> None:
        require_tex_toolchain()

        config = GaltonBoardConfig(rows=10, balls=160, p=0.5, seed=13)
        result = simulate_galton_board(config)
        dropped = ValueTracker(0)

        title = Text("Galton board: random choices build a bell curve", font_size=30)
        title.to_edge(UP, buff=0.28)
        formula = Text("X ~ Binomial(n, p),   p = 0.5", font_size=23, color=GREY_A)
        formula.next_to(title, DOWN, buff=0.1)

        center = LEFT * 1.25 + DOWN * 0.05
        spacing_x = 0.44
        spacing_y = 0.34
        top_y = 2.0
        base_y = -1.62
        bar_scale = 0.06

        pegs = self._pegs(config.rows, center, spacing_x, spacing_y, top_y)
        frame = self._frame(config.rows, center, spacing_x, top_y, base_y)
        slots = self._slots(config.rows, center, spacing_x, base_y)
        bars = always_redraw(
            lambda: self._bars(result, dropped, center, spacing_x, base_y, bar_scale)
        )
        theory = self._theory_curves(result, center, spacing_x, base_y, bar_scale)
        stats = always_redraw(lambda: self._stats_panel(result, dropped).to_corner(DR, buff=0.42))

        self.play(FadeIn(title), FadeIn(formula))
        self.play(Create(frame), FadeIn(pegs), FadeIn(slots), FadeIn(theory))
        self.add(bars, stats)

        batch_size = 10
        for start in range(0, config.balls, batch_size):
            end = min(start + batch_size, config.balls)
            balls = VGroup()
            animations = []
            for index in range(start, end):
                dot = Dot(
                    self._start_point(center, top_y),
                    radius=0.046,
                    color=BLUE_C if index % 2 == 0 else TEAL_C,
                )
                path = self._ball_path(result.paths[index], center, spacing_x, spacing_y, top_y, base_y)
                balls.add(dot)
                animations.append(MoveAlongPath(dot, path))
            self.add(balls)
            self.play(*animations, run_time=0.66, rate_func=smooth)
            self.remove(balls)
            self.play(dropped.animate.set_value(end), run_time=0.08, rate_func=linear)

        self.wait(0.6)

    def _pegs(self, rows, center, spacing_x, spacing_y, top_y):
        pegs = VGroup()
        for row in range(rows):
            for col in range(row + 1):
                x = center[0] + (col - row / 2) * spacing_x
                y = top_y - row * spacing_y
                pegs.add(Dot([x, y, 0], radius=0.028, color=GREY_B))
        return pegs

    def _frame(self, rows, center, spacing_x, top_y, base_y):
        width = (rows + 1) * spacing_x
        left = center[0] - width / 2 - 0.18
        right = center[0] + width / 2 + 0.18
        top = top_y + 0.42
        line_left = Line([center[0], top, 0], [left, base_y + 0.25, 0], color=GREY_D)
        line_right = Line([center[0], top, 0], [right, base_y + 0.25, 0], color=GREY_D)
        base = Line([left, base_y, 0], [right, base_y, 0], color=GREY_B)
        return VGroup(line_left, line_right, base)

    def _slots(self, rows, center, spacing_x, base_y):
        slots = VGroup()
        for slot in range(rows + 2):
            x = center[0] + (slot - 0.5 - rows / 2) * spacing_x
            slots.add(Line([x, base_y, 0], [x, base_y + 0.34, 0], color=GREY_D, stroke_width=2))
        return slots

    def _bars(self, result, tracker, center, spacing_x, base_y, bar_scale):
        count = int(tracker.get_value())
        counts = np.zeros(result.rows + 1) if count <= 0 else result.cumulative_counts[count - 1]
        bars = VGroup()
        for slot, value in enumerate(counts):
            height = max(0.001, float(value) * bar_scale)
            x = center[0] + (slot - result.rows / 2) * spacing_x
            bar = Rectangle(
                width=spacing_x * 0.72,
                height=height,
                stroke_width=1.4,
                stroke_color=BLUE_E,
                fill_color=BLUE_E,
                fill_opacity=0.62,
            )
            bar.move_to([x, base_y + height / 2, 0])
            bars.add(bar)
        return bars

    def _theory_curves(self, result, center, spacing_x, base_y, bar_scale):
        binomial_points = []
        normal_points = []
        mean = result.rows * result.p
        sigma = sqrt(result.rows * result.p * (1.0 - result.p))
        for slot, probability in enumerate(result.probabilities):
            x = center[0] + (slot - result.rows / 2) * spacing_x
            binomial_points.append([x, base_y + result.balls * probability * bar_scale, 0])
            normal_probability = self._normal_density(slot, mean, sigma)
            normal_points.append([x, base_y + result.balls * normal_probability * bar_scale, 0])

        binomial = VMobject(color=YELLOW, stroke_width=3.2).set_points_smoothly(binomial_points)
        normal = VMobject(color=GREY_A, stroke_width=2.2).set_points_smoothly(normal_points)
        normal.set_opacity(0.75)
        legend = VGroup(
            self._legend_row("binomial", YELLOW),
            self._legend_row("normal", GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend.next_to(binomial, RIGHT, buff=0.3).shift(UP * 0.25)
        return VGroup(binomial, normal, legend)

    def _legend_row(self, label, color):
        line = Line(LEFT * 0.18, RIGHT * 0.18, color=color, stroke_width=3)
        text = Text(label, font_size=18, color=color)
        return VGroup(line, text).arrange(RIGHT, buff=0.08)

    def _normal_density(self, x, mean, sigma):
        if sigma <= 0:
            return 0.0
        return exp(-0.5 * ((x - mean) / sigma) ** 2) / (sigma * sqrt(2.0 * pi))

    def _stats_panel(self, result, tracker):
        count = int(tracker.get_value())
        counts = np.zeros(result.rows + 1) if count <= 0 else result.cumulative_counts[count - 1]
        slots = np.arange(result.rows + 1, dtype=float)
        total = max(float(counts.sum()), 1.0)
        mean = float(np.dot(slots, counts) / total)
        variance = float(np.dot((slots - mean) ** 2, counts) / total)
        peak = int(counts.max()) if count > 0 else 0
        panel = VGroup(
            Text(f"balls = {count}", font_size=20, color=WHITE),
            Text(f"mean slot = {mean:.2f}", font_size=20, color=GREY_A),
            Text(f"std = {sqrt(variance):.2f}", font_size=20, color=GREY_A),
            Text(f"peak = {peak}", font_size=20, color=BLUE_C),
        )
        panel.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        return panel

    def _start_point(self, center, top_y):
        return [center[0], top_y + 0.58, 0]

    def _ball_path(self, choices, center, spacing_x, spacing_y, top_y, base_y):
        points = [self._start_point(center, top_y)]
        rights = 0
        for row, goes_right in enumerate(choices):
            rights += int(goes_right)
            x = center[0] + (rights - (row + 1) / 2) * spacing_x
            y = top_y - row * spacing_y - spacing_y * 0.58
            points.append([x, y, 0])
        slot = int(np.sum(choices))
        points.append([center[0] + (slot - len(choices) / 2) * spacing_x, base_y + 0.18, 0])
        return VMobject().set_points_smoothly(points)
