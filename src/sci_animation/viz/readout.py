from __future__ import annotations

from manim import DOWN, GREY_B, LEFT, RIGHT, Text, VGroup

from sci_animation.schemas import TimeResponse


class LiveValuePanel(VGroup):
    def __init__(
        self,
        response: TimeResponse,
        tracker,
        rows: list[tuple[str, str, str]],
        colors: dict[str, str],
        font_size: int = 18,
    ):
        self.response = response
        self.tracker = tracker
        self.rows = rows
        self.colors = colors
        self.font_size = font_size
        initial = self._build()
        super().__init__(*initial.submobjects)
        self.add_updater(lambda mob: mob.become(self._build()))

    def _build(self) -> VGroup:
        row_mobjects = VGroup()
        now = self.tracker.get_value()
        for label_text, source, unit in self.rows:
            value = now if source == "time" else self.response.value_at(source, now)
            color = self.colors.get(source, self.colors.get(label_text, "#FFFFFF"))
            label = Text(f"{label_text} =", font_size=self.font_size, color=color)
            number = Text(f"{value:7.3f}", font_size=self.font_size, color=color)
            unit_text = Text(unit, font_size=max(self.font_size - 2, 10), color=GREY_B)
            row_mobjects.add(VGroup(label, number, unit_text).arrange(RIGHT, buff=0.06))
        row_mobjects.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        return row_mobjects
