from manim import (
    BLUE,
    DOWN,
    GREEN,
    LEFT,
    PI,
    PURPLE,
    RED,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Code,
    Create,
    FadeIn,
    FadeOut,
    MathTex,
    Rectangle,
    ReplacementTransform,
    Scene,
    Square,
    SurroundingRectangle,
    Swap,
    Tex,
    Text,
    Transform,
    Triangle,
    VGroup,
)
from manim.mobject.logo import se
from manim.mobject.text.text_mobject import remove_invisible_chars
from user_array import my_array


class BubbleSort(Scene):
    def setup(self):
        super().setup()
        self.global_animation_duration = 0.4

    def create_pointer(self, position, label_text):
        """Creates a pointer with a label below the given position."""
        pointer = Triangle(fill_opacity=1, color=RED).scale(0.2)
        pointer.next_to(position, DOWN)
        label = Text(label_text, font_size=24).next_to(pointer, DOWN * 0.2)
        return VGroup(pointer, label)

    def display_code(self, code_text):
        """Displays code snippet at the bottom."""
        code = Code(
            code=code_text,
            tab_width=4,
            background="window",
            language="Python",
            font_size=18,
            insert_line_no=False,
            line_spacing=0.6,
        ).to_edge(DOWN)
        self.play(Create(code))
        return code

    def build_code_block(self, code_str):
        # build the code block
        m_code = Code(
            code=code_str,
            font_size=18,
            tab_width=4,
            language="Python",
            background="window",
            line_spacing=0.6,
            insert_line_no=False,
        ).to_edge(DOWN)
        self.add(m_code)

        # build sliding windows (SurroundingRectangle)
        m_code.code = remove_invisible_chars(m_code.code)
        self.sliding_wins = VGroup()
        height = m_code.code[0].height
        for line in m_code.code:
            self.sliding_wins.add(
                SurroundingRectangle(line).set_fill(YELLOW).set_opacity(0)
            )

        self.add(self.sliding_wins)
        return m_code

    def highlight(self, prev_line, line):
        self.play(
            self.sliding_wins[prev_line].animate.set_opacity(0.3),
            run_time=self.global_animation_duration,
        )
        self.play(
            ReplacementTransform(
                self.sliding_wins[prev_line], self.sliding_wins[line]
            ),
            run_time=self.global_animation_duration,
        )
        self.play(
            self.sliding_wins[line].animate.set_opacity(0.3),
            run_time=self.global_animation_duration,
        )

    currentlyHighlitedLine = -1  # that means no line is highlighted currently

    def justHighlight(self, line_no):

        if not self.currentlyHighlitedLine == -1:
            self.play(
                self.sliding_wins[
                    self.currentlyHighlitedLine
                ].animate.set_opacity(0.0),
                run_time=self.global_animation_duration,
            )

        self.play(
            self.sliding_wins[line_no].animate.set_opacity(0.3),
            run_time=self.global_animation_duration,
        )
        self.currentlyHighlitedLine = line_no

    def undoHighlight(self, line_no):
        self.currentlyHighlitedLine = -1
        self.play(
            self.sliding_wins[line_no].animate.set_opacity(0.0),
            run_time=self.global_animation_duration,
        )

    def place_slider_window(self, Array: VGroup, at_index=0):
        self.cover_group = VGroup(Array[at_index], Array[at_index + 1])
        self.slider_window = SurroundingRectangle(
            self.cover_group, color=RED, buff=0
        )
        self.slide_amount_1_unit = Array[0].width
        self.slider_current_index = 0
        self.play(
            FadeIn(self.slider_window), run_time=self.global_animation_duration
        )

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
        self.play(
            self.slider_window.animate.shift(dir * net_slide_amount),
            run_time=self.global_animation_duration,
        )
        self.slider_current_index = target_index

    def strobe_bg(self, mobj, color):
        self.play(mobj.animate.set_fill(color, opacity=0.3), run_time=0.4)
        self.play(mobj.animate.set_fill(opacity=0.0), run_time=0.4)

    def construct(self):
        # Title Text
        title = (
            Text("Bubble Sorting Algorithm", gradient=[BLUE, PURPLE])
            .move_to(2.6 * UP)
            .scale(1.2)
        )
        self.add(title)

        # Code snippet at the bottom
        bubble_sort_code = """
        def bubble_sort(arr):
            n = len(arr)
                for i in range(n - 1):
                    for j in range(n - i - 1):
                        if arr[j] > arr[j + 1]:
                            arr[j], arr[j + 1] = arr[j + 1], arr[j]
        """
        code_display = self.build_code_block(bubble_sort_code)
        # self.highlight(0, 1)
        self.justHighlight(0)

        # Array setup
        nums = my_array
        array = (
            VGroup(*[Square().scale(0.4) for _ in range(len(nums))])
            .arrange(RIGHT, buff=0.0)
            .move_to(UP)
        )
        num_tex = (
            VGroup(*[MathTex(str(num)) for num in nums])
            .scale(1.5)
            .arrange(RIGHT)
            .scale(0.8)
        )
        [num_tex[i].move_to(array[i].get_center()) for i in range(len(nums))]

        self.play(Create(array), Create(num_tex))

        self.justHighlight(1)
        n = len(nums)
        i_pointer_created = False
        j_pointer_created = False
        first_comparison = True
        first_swap = True
        # Bubble Sort Animation
        for i in range(n - 1):
            # i Pointer
            if not i_pointer_created:
                position = num_tex[i].get_center()
                label_text = f"i={i}"
                i_pointer = Triangle(fill_opacity=1, color=RED).scale(0.2)
                i_pointer.next_to(position, DOWN)
                i_ptr_label = Text(label_text, font_size=24).next_to(
                    i_pointer, DOWN * 0.2
                )
                i_ptr_vg = VGroup(i_pointer, i_ptr_label)

                i_pointer_created = True
                # self.highlight(1, 2)
                self.justHighlight(2)
                self.play(
                    Create(i_ptr_vg), run_time=self.global_animation_duration
                )
            else:
                position = num_tex[i].get_center()
                label_text = f"i={i}"
                updated_i_ptr_label = Text(label_text, font_size=24).next_to(
                    position, DOWN * 2.3
                )
                # self.highlight(3, 2)
                self.justHighlight(2)
                self.play(
                    i_ptr_vg.animate.next_to(position, DOWN),
                    Transform(i_ptr_label, updated_i_ptr_label),
                    run_time=self.global_animation_duration,
                )

            first_comparison = True
            for j in range(n - i - 1):
                # j Pointer
                if not j_pointer_created:

                    position = num_tex[j].get_center()
                    label_text = f"j={j}"
                    j_pointer = Triangle(fill_opacity=1, color=RED).scale(0.2)
                    j_pointer.rotate(PI)
                    j_pointer.next_to(position, UP)
                    j_ptr_label = Text(label_text, font_size=24).next_to(
                        j_pointer, UP * 0.2
                    )
                    j_ptr_vg = VGroup(j_pointer, j_ptr_label)

                    j_pointer_created = True
                    # self.highlight(2, 3)
                    self.justHighlight(3)
                    self.play(
                        Create(j_ptr_vg),
                        run_time=self.global_animation_duration,
                    )
                else:
                    position = num_tex[j].get_center()
                    label_text = f"j={j}"
                    updated_j_ptr_label = Text(
                        label_text, font_size=24
                    ).next_to(position, UP * 2.3)
                    # self.highlight(5, 2)
                    self.justHighlight(3)
                    self.play(
                        j_ptr_vg.animate.next_to(position, UP),
                        Transform(j_ptr_label, updated_j_ptr_label),
                        run_time=self.global_animation_duration,
                    )

                self.justHighlight(4)
                if first_comparison:
                    self.place_slider_window(array, at_index=0)
                    first_comparison = False
                else:
                    self.slide_window_to(j)

                self.play(
                    num_tex[j].animate.set_color(YELLOW),
                    num_tex[j + 1].animate.set_color(YELLOW),
                    run_time=self.global_animation_duration,
                )

                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
                    self.strobe_bg(self.slider_window, GREEN)

                    self.justHighlight(5)
                    self.play(
                        Swap(num_tex[j], num_tex[j + 1]),
                        run_time=self.global_animation_duration,
                    )
                    num_tex[j], num_tex[j + 1] = num_tex[j + 1], num_tex[j]
                else:
                    self.strobe_bg(self.slider_window, RED)

                # Reset colors and remove the j pointer
                self.play(
                    num_tex[j].animate.set_color(WHITE),
                    num_tex[j + 1].animate.set_color(WHITE),
                    run_time=self.global_animation_duration,
                )
                # self.play(FadeOut(j_pointer))

            # Finalize the sorted element and remove the i pointer
            self.play(
                FadeOut(self.slider_window),
                run_time=self.global_animation_duration,
            )
            self.play(
                num_tex[n - i - 1].animate.shift(RIGHT),
                array[n - i - 1].animate.shift(RIGHT),
                run_time=self.global_animation_duration,
            )

            self.play(
                num_tex[n - i - 1].animate.set_color(GREEN),
                array[n - i - 1].animate.set_color(GREEN),
                run_time=self.global_animation_duration,
            )

        self.play(
            num_tex[0].animate.shift(RIGHT),
            array[0].animate.shift(RIGHT),
            run_time=self.global_animation_duration,
        )
        self.play(
            num_tex[0].animate.set_color(GREEN),
            array[0].animate.set_color(GREEN),
            run_time=self.global_animation_duration,
        )

        self.play(
            array.animate.shift(LEFT),
            num_tex.animate.shift(LEFT),
            run_time=self.global_animation_duration,
        )
        # Final wait before ending the scene
        self.undoHighlight(5)
        self.play(FadeOut(code_display))
        self.wait(1)
