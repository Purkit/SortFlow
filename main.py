import ast
import subprocess
import sys
import time

from PySide6.QtCore import QProcess, QUrl, Signal, Slot
from PySide6.QtGui import QIcon, Qt
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# import time


class MainPage(QWidget):
    start_clicked = Signal()  # Signal to switch to algorithm selection

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SortFlow")
        self.setWindowIcon(QIcon("icon.png"))

        title_label = QLabel("SortFlow")
        title_label.setStyleSheet(
            "font-size: 80px; font-weight: bold; text-align: center; margin-bottom: 30px"
        )

        start_button = QPushButton("Start")
        start_button.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 15px 60px;
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                border: none;
                outline: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #387c3a;
            }
        """
        )
        start_button.clicked.connect(
            self.start_clicked.emit
        )  # Emit the signal when clicked

        v_layout = QVBoxLayout()

        v_layout.addWidget(title_label)
        v_layout.setAlignment(
            title_label,
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
        )

        v_layout.addWidget(start_button)
        v_layout.setAlignment(
            start_button,
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
        )

        self.setLayout(v_layout)


class AlgorithmPage(QWidget):
    algorithm_selected = Signal(str)  # Signal to pass the selected algorithm

    def __init__(self):
        super().__init__()

        request_test = QLabel("Select a sorting algorithm...")

        self.algorithm_list = QComboBox()
        self.algorithm_list.addItems(
            ["Bubble Sort", "Selection Sort", "Insertion Sort"]
        )

        select_button = QPushButton("Select Algorithm")
        select_button.clicked.connect(self.select_algorithm)

        style = """
            QLabel {
                font-size: 40px;
                font-weight: bold;
                color: #ffffff;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                border: none;
                outline: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #387c3a;
            }
            QComboBox {
                font-size: 14px;
                padding: 5px 90px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QComboBox:hover {
                border-color: #4CAF50;
            }
            QComboBox:focus {
                border-color: #4CAF50;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                selection-background-color: #4CAF50;
                selection-color: white;
            }
        """
        self.setStyleSheet(style)

        v_layout = QVBoxLayout()

        v_layout.addWidget(request_test)
        v_layout.setAlignment(request_test, Qt.AlignmentFlag.AlignCenter)

        v_layout.addWidget(self.algorithm_list)
        v_layout.setAlignment(
            self.algorithm_list,
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
        )

        v_layout.addWidget(select_button)
        v_layout.setAlignment(
            select_button,
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
        )

        self.setLayout(v_layout)

    def select_algorithm(self):
        selected_algorithm = self.algorithm_list.currentText()
        self.algorithm_selected.emit(
            selected_algorithm
        )  # Emit the selected algorithm


class InputPage(QWidget):
    input_done = Signal()

    def __init__(self):
        super().__init__()

        request_text_label = QLabel("Enter List of Numbers to Sort")

        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText(
            "Enter a list of numbers (comma separated)"
        )

        go_button = QPushButton("Generate Animation")
        go_button.clicked.connect(self.write_array_to_module)
        style = """
            QLabel {
                font-size: 25px;
                color: #ffffff;
                margin-right: 20px;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                border: none;
                outline: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #387c3a;
            }
            QLineEdit {
                font-size: 14px;
                padding: 8px 200px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """
        self.setStyleSheet(style)

        h_layout = QHBoxLayout()
        v_layout = QVBoxLayout()

        h_layout.addWidget(request_text_label)
        h_layout.setAlignment(request_text_label, Qt.AlignmentFlag.AlignLeft)

        h_layout.addWidget(self.number_input)
        h_layout.setAlignment(self.number_input, Qt.AlignmentFlag.AlignRight)

        v_layout.addLayout(h_layout)
        v_layout.setAlignment(h_layout, Qt.AlignmentFlag.AlignCenter)

        v_layout.addWidget(go_button)
        v_layout.setAlignment(go_button, Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("")
        v_layout.addWidget(self.status_label)
        v_layout.setAlignment(self.status_label, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(v_layout)

    def wrap_string_with_square_bracket(self, input_str):
        input_str = input_str.strip()

        if not input_str:
            return "[]"

        output_str = "[" + input_str + "]"
        return output_str

    def write_array_to_module(self):
        # Retrieve the user input from the text box
        user_input = self.number_input.text().strip()
        wrapped_list = self.wrap_string_with_square_bracket(user_input)

        try:
            # Convert the input string to an actual Python list using ast.literal_eval
            array = ast.literal_eval(wrapped_list)

            if not isinstance(array, list):
                raise ValueError("Input is not a valid list.")

            # Write the array to the module
            file_path = "./animations/user_array.py"
            with open(file_path, "w") as f:
                # Write the array to the Python file as a list
                f.write(f"my_array = {array}\n")
            print(f"Array written to {file_path}")

            # Update status
            self.status_label.setText(
                "Array successfully saved. Generating animation..."
            )
            self.status_label.setStyleSheet("color: green;")

            # ! Trigger ManimStdoutCapturePage page from here
            self.input_done.emit()

        except Exception as e:
            # In case of error, show error message
            self.status_label.setText(f"Error: {str(e)}")
            self.status_label.setStyleSheet("color: red;")


class ManimStdoutCapturePage(QWidget):
    manim_process_success = Signal()

    def __init__(self):
        super().__init__()

        style = """
            QLabel {
                font-size: 40px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            QProgressBar {
                height: 30px;
                width: 500px;
                border-radius: 10px;
                margin-top: 0px;
                margin-bottom: 10px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 10px;
            }
            QTextEdit {
                font-size: 14px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 10px;
            }
        """
        self.setStyleSheet(style)

        request_text_label = QLabel("Generating Animation. Please Wait...")

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Make it infinite (endless)
        self.progress_bar.setTextVisible(False)  # Hide text in progress bar

        self.stdout_display = QTextEdit()
        self.stdout_display.setReadOnly(True)

        h_layout_1 = QHBoxLayout()
        v_layout = QVBoxLayout()

        v_layout.addWidget(request_text_label)
        v_layout.setAlignment(
            request_text_label,
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
        )

        v_layout.addWidget(self.progress_bar)
        v_layout.setAlignment(
            self.progress_bar,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter,
        )

        h_layout_1.addWidget(self.stdout_display)
        h_layout_1.setAlignment(
            self.stdout_display,
            Qt.AlignmentFlag.AlignAbsolute,
        )

        v_layout.addLayout(h_layout_1)
        v_layout.setAlignment(h_layout_1, Qt.AlignmentFlag.AlignAbsolute)

        self.setLayout(v_layout)

        # Initialize QProcess
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout_output)
        self.process.readyReadStandardError.connect(self.handle_stderr_output)

        self.process.finished.connect(self.on_process_finish)

    def run_manim_process(self, algo):
        command_test = ["ping", "-c", "4", "archlinux.org"]
        command_1 = [
            "docker",
            "run",
            "--rm",
            "-v",
            "/home/deepy/DEV/SortFlow:/AnimDir",
            "manimce:latest",
            "/bin/bash",
            "-c",
            "cd /AnimDir/animations/ && manim bubble.py",
        ]
        command_2 = [
            "docker",
            "run",
            "--rm",
            "-v",
            "/home/deepy/DEV/SortFlow:/AnimDir",
            "manimce:latest",
            "/bin/bash",
            "-c",
            "cd /AnimDir/animations/ && manim selection.py",
        ]
        command_3 = [
            "docker",
            "run",
            "--rm",
            "-v",
            "/home/deepy/DEV/SortFlow:/AnimDir",
            "manimce:latest",
            "/bin/bash",
            "-c",
            "cd /AnimDir/animations/ && manim insertion.py",
        ]

        # Start the process
        if algo == "Bubble Sort":
            self.process.start(command_1[0], command_1[1:])
        elif algo == "Selection Sort":
            self.process.start(command_2[0], command_2[1:])
        elif algo == "Insertion Sort":
            self.process.start(command_3[0], command_3[1:])

        # Start progress animation (endless)
        self.progress_bar.setValue(0)
        self.progress_bar.setRange(0, 0)  # Endless mode

    def handle_stdout_output(self):
        stdout_output = bytes(self.process.readAllStandardOutput()).decode(
            "utf-8"
        )
        self.stdout_display.append(stdout_output)

    def handle_stderr_output(self):
        stderr_output = bytes(self.process.readAllStandardError()).decode(
            "utf-8"
        )
        self.stdout_display.append(stderr_output)

    def on_process_finish(self, exit_code, exit_status):
        if exit_status == QProcess.ExitStatus.NormalExit:
            self.stdout_display.append(
                f"Process finished successfully with exit code: {exit_code}."
            )
            time.sleep(5)
            # Run this: ffmpeg -i input_video.mp4 -c:v libx264 -crf 23 -preset fast output_video.mp4
            # Trigger FinalPage from here
            self.manim_process_success.emit()
        else:
            self.stdout_display.append(
                f"Process crashed with exit code: {exit_code}."
            )

    # // ! Continue from here
    @Slot()
    def start_process(self, algo):
        print(
            f"algorithm_selected string recieved by slot start_process: {algo}"
        )
        self.run_manim_process(algo)


class FinalPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.setLayout(layout)

        # Setting up the video player
        self.video_widget = QVideoWidget()
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.video_widget)

        layout.addWidget(self.video_widget)
        self.video_widget.show()

        # Load a placeholder video file
        self.player.setSource(
            QUrl(
                "animations/media/videos/array_visual/1080p60/ProceduralArrayVisual.mp4"
            )
        )

    @Slot()
    def startPlaying(self):
        self.player.play()


class SortFlowApp(QWidget):
    start_video_signal = Signal()
    start_manim_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SortFlow")
        self.setGeometry(100, 100, 1400, 800)

        # Create stacked widget to hold different pages
        self.stacked_widget = QStackedWidget()

        # Initialize the pages
        self.main_page = MainPage()
        self.algorithm_page = AlgorithmPage()
        self.input_page = InputPage()
        self.manim_process_page = ManimStdoutCapturePage()
        self.final_page = FinalPage()

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.algorithm_page)
        self.stacked_widget.addWidget(self.input_page)
        self.stacked_widget.addWidget(self.manim_process_page)
        self.stacked_widget.addWidget(self.final_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # Connect signals
        self.main_page.start_clicked.connect(self.show_algorithm_page)
        self.algorithm_page.algorithm_selected.connect(self.show_input_page)
        self.input_page.input_done.connect(self.show_manim_progress_page)
        # self.manim_process_page.manim_process_success.connect(
        #     self.show_final_page
        # )
        self.manim_process_page.manim_process_success.connect(self.fire_mpv)

        self.start_manim_signal.connect(self.manim_process_page.start_process)
        self.start_video_signal.connect(self.final_page.startPlaying)

    def show_algorithm_page(self):
        self.stacked_widget.setCurrentWidget(self.algorithm_page)

    def show_input_page(self, selected_algorithm):
        self.selected_algorithm = selected_algorithm
        self.stacked_widget.setCurrentWidget(self.input_page)

    def show_manim_progress_page(self):
        self.stacked_widget.setCurrentWidget(self.manim_process_page)
        self.start_manim_signal.emit(self.selected_algorithm)

    def show_final_page(self):

        self.stacked_widget.setCurrentWidget(self.final_page)
        self.start_video_signal.emit()

    def fire_mpv(self):
        if self.selected_algorithm == "Bubble Sort":
            subprocess.run(
                [
                    "mpv",
                    "animations/media/videos/bubble/1080p60/BubbleSort.mp4",
                ]
            )
        elif self.selected_algorithm == "Selection Sort":
            subprocess.run(
                [
                    "mpv",
                    "animations/media/videos/selection/1080p60/SelectionSort.mp4",
                ]
            )
        elif self.selected_algorithm == "Insertion Sort":
            subprocess.run(
                [
                    "mpv",
                    "animations/media/videos/insertion/1080p60/InsertionSort.mp4",
                ]
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SortFlowApp()
    window.show()
    sys.exit(app.exec())
