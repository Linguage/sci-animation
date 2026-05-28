from __future__ import annotations

from manim import RIGHT, UP, Axes, Dot, GREY_B, MathTex, Text, VGroup, always_redraw

from sci_animation.schemas import TimeResponse


class TimeHistoryPlot(VGroup):
    def __init__(
        self,
        response: TimeResponse,
        channels: list[str],
        tracker,
        colors: list[str],
        title: str,
        x_length: float,
        y_length: float,
        y_range: tuple[float, float, float] | None = None,
    ):
        if len(channels) != len(colors):
            raise ValueError("channels and colors must have the same length.")

        self.response = response
        self.channels = channels
        self.tracker = tracker
        self.colors = colors

        if y_range is None:
            max_value = max(response.max_abs(channels) * 1.15, 1.0e-6)
            y_range = (-max_value, max_value, max_value)

        self.axes = Axes(
            x_range=(0, response.duration(), 2),
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        )
        title_mob = MathTex(title, font_size=24)
        title_mob.next_to(self.axes, UP, buff=0.06)
        x_label = Text("time", font_size=16, color=GREY_B).next_to(self.axes.x_axis, RIGHT, buff=0.08)

        curves = [
            always_redraw(
                lambda channel=channel, color=color: self.axes.plot(
                    lambda time: response.value_at(channel, time),
                    x_range=(0, max(tracker.get_value(), 0.001)),
                    color=color,
                    stroke_width=3.5,
                )
            )
            for channel, color in zip(channels, colors)
        ]
        dots = [
            always_redraw(
                lambda channel=channel, color=color: Dot(
                    self.axes.c2p(tracker.get_value(), response.value_at(channel, tracker.get_value())),
                    radius=0.048,
                    color=color,
                )
            )
            for channel, color in zip(channels, colors)
        ]

        self.curves = VGroup(*curves)
        self.dots = VGroup(*dots)
        super().__init__(self.axes, title_mob, x_label, self.curves, self.dots)
