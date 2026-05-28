from __future__ import annotations

from pathlib import Path
import sys

from manim import *

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from _helpers import require_tex_toolchain
from sci_animation.replay import read_time_response_csv
from sci_animation.viz import LiveValuePanel, TimeHistoryPlot


class ReplayTimeResponseScene(Scene):
    def construct(self) -> None:
        require_tex_toolchain()

        response = read_time_response_csv(
            ROOT / "examples" / "replay" / "three_story_sample.csv",
            units={"u1": "m", "u2": "m", "u3": "m"},
            labels={"u1": "u1", "u2": "u2", "u3": "u3"},
            metadata={"source": "examples/replay/three_story_sample.csv"},
        )
        tracker = ValueTracker(0.0)

        title = Text("Replay CSV time response", font_size=32)
        title.to_edge(UP, buff=0.35)
        subtitle = Text("external data -> TimeResponse -> reusable plot", font_size=20, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.12)

        plot = TimeHistoryPlot(
            response=response,
            channels=["u1", "u2", "u3"],
            tracker=tracker,
            colors=[BLUE_C, TEAL_C, ORANGE],
            title=r"u_i(t)",
            x_length=7.4,
            y_length=3.2,
        )
        plot.move_to(UP * 0.1)

        panel = always_redraw(
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
            ).to_corner(DL, buff=0.45)
        )

        self.play(FadeIn(title), FadeIn(subtitle))
        self.play(Create(plot), FadeIn(panel))
        self.play(tracker.animate.set_value(response.duration()), run_time=4, rate_func=linear)
        self.wait(0.5)

