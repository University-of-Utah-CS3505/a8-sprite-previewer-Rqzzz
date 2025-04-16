#https://github.com/University-of-Utah-CS3505/a8-sprite-previewer-Rqzzz
#Rongquan Zhang

import math

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_sprite(sprite_folder_name, number_of_frames):
    frames = []
    padding = math.ceil(math.log(number_of_frames - 1, 10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding, '0') + ".png"
        frames.append(QPixmap(folder_and_file_name))

    return frames

class SpritePreview(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite Animation Preview")
        self.num_frames = 21
        self.frames = load_sprite('spriteImages',self.num_frames)
        self.current_frame = 0
        self.is_playing = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.setupUI()


    def setupUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.create_menu()

        self.sprite_label = QLabel()
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sprite_label.setPixmap(self.frames[0])
        main_layout.addWidget(self.sprite_label)

        control_panel = QFrame()
        control_layout = QHBoxLayout(control_panel)

        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.clicked.connect(self.toggle_animation)
        control_layout.addWidget(self.start_stop_button)

        fps_control = QFrame()
        fps_layout = QHBoxLayout(fps_control)

        fps_label = QLabel("Frames per second:")
        fps_layout.addWidget(fps_label)

        self.fps_slider = QSlider(Qt.Orientation.Horizontal)
        self.fps_slider.setRange(1, 100)
        self.fps_slider.setValue(30)
        self.fps_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.fps_slider.setTickInterval(10)
        self.fps_slider.valueChanged.connect(self.update_fps_display)
        fps_layout.addWidget(self.fps_slider)

        self.fps_value_label = QLabel("30")
        fps_layout.addWidget(self.fps_value_label)

        control_layout.addWidget(fps_control)
        main_layout.addWidget(control_panel)

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        pause_action = QAction("Pause", self)
        pause_action.triggered.connect(self.pause_animation)
        file_menu.addAction(pause_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def toggle_animation(self):
        if self.is_playing:
            self.stop_animation()
            self.start_stop_button.setText("Start")
        else:
            self.start_animation()
            self.start_stop_button.setText("Stop")

    def start_animation(self):
        if not self.is_playing:
            self.is_playing = True
            fps = self.fps_slider.value()
            delay = int(1000 / fps)
            self.timer.start(delay)

    def stop_animation(self):
        if self.is_playing:
            self.is_playing = False
            self.timer.stop()

    def pause_animation(self):
        self.stop_animation()
        self.start_stop_button.setText("Start")

    def update_frame(self):
        self.current_frame = (self.current_frame + 1) % self.num_frames
        self.sprite_label.setPixmap(self.frames[self.current_frame])

    def update_fps_display(self):
        fps = self.fps_slider.value()
        self.fps_value_label.setText(str(fps))

        if self.is_playing:
            self.timer.stop()
            delay = int(1000 / fps)
            self.timer.start(delay)


def main():
    app = QApplication([])
    # Create our custom application
    window = SpritePreview()
    # And show it
    window.show()
    app.exec()


if __name__ == "__main__":
    main()