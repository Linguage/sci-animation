from __future__ import annotations

from pathlib import Path
import sys

from manim import *

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from _helpers import require_tex_toolchain
from sci_animation.models import ShearBuildingConfig, solve_earthquake_response, to_time_response
from sci_animation.viz import LiveValuePanel, TimeHistoryPlot, shear_building_mobject


class ThreeStoryEarthquakeScene(Scene):
    def construct(self) -> None:
        require_tex_toolchain()

        config = ShearBuildingConfig(
            masses=(1.0, 1.0, 1.0),
            story_stiffnesses=(90.0, 80.0, 70.0),
            damping_ratio=0.05,
        )
        structural_response = solve_earthquake_response(config, duration=8.0, dt=0.02)
        response = to_time_response(structural_response)
        duration = response.duration()
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
            lambda: VGroup(
                shear_building_mobject(response, tracker, building_origin, story_height, bay_width, disp_scale),
                self._roof_drift(response, tracker, building_origin, story_height, disp_scale),
            )
        )
        ground = always_redraw(
            lambda: self._ground(response, tracker, building_origin, bay_width, ground_scale)
        )
        floor_labels = always_redraw(
            lambda: LiveValuePanel(
                response=response,
                tracker=tracker,
                rows=[
                    ("t", "time", "s"),
                    ("u1", "u1", "m"),
                    ("u2", "u2", "m"),
                    ("u3", "u3", "m"),
                ],
                colors={"time": WHITE, "u1": BLUE_C, "u2": TEAL_C, "u3": ORANGE},
                font_size=18,
            ).to_corner(DL, buff=0.35)
        )

        axes = TimeHistoryPlot(
            response=response,
            channels=["u1", "u2", "u3"],
            tracker=tracker,
            colors=[BLUE_C, TEAL_C, ORANGE],
            title=r"u_i(t)",
            x_length=5.0,
            y_length=2.55,
        )
        axes.move_to(RIGHT * 2.25 + UP * 0.35)
        ground_axes = TimeHistoryPlot(
            response=response,
            channels=["ag"],
            tracker=tracker,
            colors=[RED_C],
            title=r"\ddot{u}_g(t)",
            x_length=5.0,
            y_length=1.25,
        )
        ground_axes.move_to(RIGHT * 2.25 + DOWN * 2.0)

        legend = self._legend()
        legend.next_to(axes, DOWN, buff=0.26).align_to(axes, LEFT)

        self.play(FadeIn(title), FadeIn(equation))
        self.play(Create(ground), Create(building), FadeIn(floor_labels))
        self.play(Create(axes), Create(ground_axes), FadeIn(legend))
        self.play(tracker.animate.set_value(duration), run_time=duration, rate_func=linear)
        self.wait(0.5)

    def _roof_drift(self, response, tracker, origin, story_height, disp_scale):
        roof_y = origin[1] + 3 * story_height
        roof_drift = response.value_at("u3", tracker.get_value()) * disp_scale
        drift_arrow = Arrow(
            [origin[0], roof_y + 0.45, 0],
            [origin[0] + roof_drift, roof_y + 0.45, 0],
            buff=0,
            color=YELLOW,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.28,
        )
        drift_label = MathTex(r"u_3(t)", font_size=24, color=YELLOW)
        drift_label.next_to(drift_arrow, UP, buff=0.06)
        return VGroup(drift_arrow, drift_label)

    def _ground(self, response, tracker, origin, bay_width, ground_scale):
        ag = response.value_at("ag", tracker.get_value())
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
