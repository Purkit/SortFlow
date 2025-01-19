from manim import (
    GREEN,
    LEFT,
    RED,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    FadeIn,
    GrowFromCenter,
    ManimColor,
    Rectangle,
    Scene,
    SurroundingRectangle,
    Text,
    VGroup,
    Write,
)
from numpy import array

from user_array import my_array


def GenerateArrayVisual(
    array_literal,
    start_pos,
    cell_width=1.1,
    cell_height=0.9,
    inbetween_gap=0,
    cell_color=WHITE,
    text_color=YELLOW,
    text_scale=1,
):
    array_cells = VGroup(
        *[
            Rectangle(height=cell_height, width=cell_width).set_color(
                cell_color
            )
            for _ in range(len(array_literal))
        ]
    )
    array_cells[0].move_to(start_pos)
    for i in range(1, len(array_cells)):
        array_cells[i].next_to(array_cells[i - 1], RIGHT, buff=inbetween_gap)

    array_content = VGroup()
    for i, individual_cell in enumerate(array_cells):
        text = Text(str(array_literal[i]))
        text.set_color(text_color)
        text.scale(text_scale)
        text.move_to(individual_cell.get_center())
        array_content.add(text)

    array_package = VGroup(array_cells, array_content)
    return array_package


class ProceduralArrayVisual(Scene):
    def place_slider_window(self, Array: VGroup, at_index=0):
        self.cover_group = VGroup(Array[at_index], Array[at_index + 1])
        self.slider_window = SurroundingRectangle(
            self.cover_group, color=RED, buff=0
        )
        self.slide_amount_1_unit = Array[0].width
        self.slider_current_index = 0
        self.play(FadeIn(self.slider_window))

    def slide_window_to(self, target_index):
        if self.slider_current_index < target_index:
            dir = RIGHT
        elif self.slider_current_index > target_index:
            dir = LEFT
        else:
            return

        net_slide_amount = self.slide_amount_1_unit * abs(
            self.slider_current_index - target_index
        )
        self.play(self.slider_window.animate.shift(dir * net_slide_amount))
        self.slider_current_index = target_index

    def strobe_bg(self, mobj, color):
        self.play(mobj.animate.set_fill(color, opacity=0.3), run_time=0.4)
        self.play(mobj.animate.set_fill(opacity=0.0), run_time=0.4)

    def construct(self):
        # some_array = [55, 86, 98, 72, 21, 13, 64]
        some_array = my_array
        array_vr = GenerateArrayVisual(some_array, LEFT * 6)
        self.play(Write(array_vr), run_time=4)
        self.play(array_vr.animate.center())

        array_cells = array_vr[0]
        self.place_slider_window(array_cells)
        self.strobe_bg(self.slider_window, GREEN)
        self.slide_window_to(1)
        self.strobe_bg(self.slider_window, RED)
        self.slide_window_to(5)
        self.strobe_bg(self.slider_window, GREEN)
        self.slide_window_to(2)
        self.strobe_bg(self.slider_window, RED)
        self.slide_window_to(4)
        self.strobe_bg(self.slider_window, GREEN)
        self.slide_window_to(3)
        self.strobe_bg(self.slider_window, RED)

        self.wait(3)
