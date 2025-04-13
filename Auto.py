import sys
import pyautogui
import time
from threading import Thread
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel, QComboBox, QLineEdit, QCheckBox, QDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeySequence, QPalette, QColor, QKeyEvent

clicking = False
click_interval = 0.1
click_count = 1
click_button = 'left'
click_type = 'single'
cursor_x = 0
cursor_y = 0
repeat_mode = 'fixed'
hotkey = QKeySequence(Qt.Key_F4)  


def start_thread():
    try:
        thread = Thread(target=start_clicking)
        thread.daemon = True
        thread.start()
    except Exception as e:
        print(f"Error starting thread: {e}")


def start_clicking():
    global clicking
    try:
        print("Autoclicker started!")
        clicking = True
        count = 0
        while clicking:
            if click_type == 'single':
                pyautogui.click(x=cursor_x, y=cursor_y, button=click_button)
            elif click_type == 'double':
                pyautogui.doubleClick(x=cursor_x, y=cursor_y, button=click_button)

            count += 1
            if repeat_mode == 'fixed' and count >= click_count:
                break
            elif repeat_mode == 'until_stopped' and not clicking:
                break
            time.sleep(click_interval)
    except Exception as e:
        print(f"Error during clicking: {e}")
        stop_clicking() 

def stop_clicking():
    global clicking
    clicking = False


class AutoClickerApp(QWidget):
    def set_dark_mode(self):
        self.setStyleSheet("background-color: #2E2E2E; color: white;")
        QApplication.setStyle("Fusion")
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(42, 42, 42))
        dark_palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        QApplication.setPalette(dark_palette)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.set_dark_mode()

    def __init__(self):
        super().__init__()
        try:
            self.init_ui()
            self.set_dark_mode()
        except Exception as e:
            print(f"Error initializing GUI: {e}")
            sys.exit(1) 

    def init_ui(self):
        try:
            self.setWindowTitle('AutoClicker')
            self.setGeometry(100, 100, 400, 400)

            layout = QVBoxLayout()

            self.interval_label = QLabel(f'Click interval: {click_interval * 1000} ms', self)
            layout.addWidget(self.interval_label)

            self.interval_slider = QSlider(Qt.Horizontal, self)
            self.interval_slider.setRange(50, 5000)  
            self.interval_slider.setValue(100)
            self.interval_slider.valueChanged.connect(self.set_click_interval)
            layout.addWidget(self.interval_slider)

            self.repeat_label = QLabel('Repeat times (for Fixed option):', self)
            self.repeat_input = QLineEdit(self)
            self.repeat_input.setPlaceholderText("Enter number of times to click")
            layout.addWidget(self.repeat_label)
            layout.addWidget(self.repeat_input)

            self.type_label = QLabel('Click type', self)
            layout.addWidget(self.type_label)

            self.type_combo = QComboBox(self)
            self.type_combo.addItems(['single', 'double'])
            self.type_combo.currentIndexChanged.connect(self.set_click_type)
            layout.addWidget(self.type_combo)

            self.button_label = QLabel('Mouse Button', self)
            layout.addWidget(self.button_label)

            self.button_combo = QComboBox(self)
            self.button_combo.addItems(['left', 'right'])
            self.button_combo.currentIndexChanged.connect(self.set_click_button)
            layout.addWidget(self.button_combo)

            self.repeat_checkbox = QCheckBox('Repeat Until Stopped', self)
            self.repeat_checkbox.stateChanged.connect(self.set_repeat_mode)
            layout.addWidget(self.repeat_checkbox)

            self.repeat_count_checkbox = QCheckBox('Repeat Fixed Times', self)
            self.repeat_count_checkbox.stateChanged.connect(self.set_repeat_mode)
            layout.addWidget(self.repeat_count_checkbox)

            self.location_label = QLabel('Cursor Position (X,Y)', self)
            layout.addWidget(self.location_label)

            self.x_input = QLineEdit(self)
            self.x_input.setPlaceholderText("X Position")
            self.y_input = QLineEdit(self)
            self.y_input.setPlaceholderText("Y Position")
            self.x_input.textChanged.connect(self.update_cursor_position)
            self.y_input.textChanged.connect(self.update_cursor_position)

            self.pick_button = QPushButton("Pick Location", self)
            self.pick_button.clicked.connect(self.pick_location)
            layout.addWidget(self.x_input)
            layout.addWidget(self.y_input)
            layout.addWidget(self.pick_button)

            button_layout = QHBoxLayout()

            self.start_button = QPushButton('Start (F4)', self)
            self.start_button.clicked.connect(self.start_thread)
            button_layout.addWidget(self.start_button)

            self.stop_button = QPushButton('Stop', self)
            self.stop_button.clicked.connect(stop_clicking)
            button_layout.addWidget(self.stop_button)

            layout.addLayout(button_layout)

            self.hotkey_button = QPushButton('Set Hotkey', self)
            self.hotkey_button.clicked.connect(self.open_hotkey_dialog)
            layout.addWidget(self.hotkey_button)

            self.record_button = QPushButton('Start Recording', self)
            self.record_button.clicked.connect(self.open_recording_dialog)
            layout.addWidget(self.record_button)

            self.setLayout(layout)
        except Exception as e:
            print(f"Error setting up UI components: {e}")
            sys.exit(1)

    def set_click_interval(self):
        global click_interval
        try:
            click_interval = self.interval_slider.value() / 1000  # Convert ms to seconds
            self.interval_label.setText(f'Click interval: {click_interval * 1000} ms')
        except Exception as e:
            print(f"Error setting click interval: {e}")

    def set_click_type(self):
        global click_type
        click_type = self.type_combo.currentText()

    def set_click_button(self):
        global click_button
        click_button = self.button_combo.currentText()

    def set_repeat_mode(self):
        global repeat_mode
        try:
            if self.repeat_checkbox.isChecked():
                repeat_mode = 'until_stopped'
            elif self.repeat_count_checkbox.isChecked():
                repeat_mode = 'fixed'
                try:
                    global click_count
                    click_count = int(self.repeat_input.text())
                except ValueError:
                    pass
            else:
                repeat_mode = 'none'
        except Exception as e:
            print(f"Error setting repeat mode: {e}")

    def update_cursor_position(self):
        global cursor_x, cursor_y
        try:
            cursor_x = int(self.x_input.text())
            cursor_y = int(self.y_input.text())
        except ValueError:
            pass

    def pick_location(self):
        try:
            self.pick_button.setText("Picking... (3s)")
            QTimer.singleShot(3000, self.record_cursor_position)  
        except Exception as e:
            print(f"Error picking location: {e}")

    def record_cursor_position(self):
        global cursor_x, cursor_y
        try:
            x, y = pyautogui.position()
            self.x_input.setText(str(x))
            self.y_input.setText(str(y))
            self.pick_button.setText("Pick Location")
        except Exception as e:
            print(f"Error recording cursor position: {e}")

    def start_thread(self):
        try:
            thread = Thread(target=start_clicking)
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Error starting thread: {e}")

    def open_hotkey_dialog(self):
        try:
            dialog = HotkeyDialog(self)
            dialog.exec_()
        except Exception as e:
            print(f"Error opening hotkey dialog: {e}")

    def open_recording_dialog(self):
        try:
            dialog = RecordingDialog(self)
            dialog.exec_()
        except Exception as e:
            print(f"Error opening recording dialog: {e}")

class HotkeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set Hotkey')
        self.setGeometry(200, 200, 250, 100)
        
        layout = QVBoxLayout()
        self.label = QLabel('Press a key to set as hotkey (default: F4)', self)
        layout.addWidget(self.label)
        
        self.setHotkeyButton = QPushButton("Press to Log Key", self)
        self.setHotkeyButton.clicked.connect(self.start_key_listening)
        layout.addWidget(self.setHotkeyButton)
        
        self.setLayout(layout)

    def start_key_listening(self):
        self.setHotkeyButton.setText("Press any key to set as hotkey...")
        self.setHotkeyButton.setEnabled(False)
        self.setFocusPolicy(Qt.StrongFocus) 

    def keyPressEvent(self, event):
        try:
            if event.key() != Qt.Key_Shift and event.key() != Qt.Key_Control and event.key() != Qt.Key_Alt:
                global hotkey
                hotkey = QKeySequence(event.key()) 
                self.label.setText(f"Hotkey set to: {event.text()}")
                self.setHotkeyButton.setText("Press to Log Key")
                self.setHotkeyButton.setEnabled(True)
                self.setFocusPolicy(Qt.NoFocus)

                self.accept()


                self.parent().update_hotkey(hotkey)
        except Exception as e:
            print(f"Error handling key press: {e}")


class RecordingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Recording')
        self.setGeometry(200, 200, 250, 150)
        layout = QVBoxLayout()

        self.record_button = QPushButton('Start Recording', self)
        self.record_button.clicked.connect(self.start_recording)
        layout.addWidget(self.record_button)

        self.pause_button = QPushButton('Pause Recording', self)
        self.pause_button.clicked.connect(self.pause_recording)
        layout.addWidget(self.pause_button)

        self.cancel_button = QPushButton('Cancel Recording', self)
        self.cancel_button.clicked.connect(self.cancel_recording)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def start_recording(self):
        try:
            time.sleep(0.2)
        except Exception as e:
            print(f"Error starting recording: {e}")

    def pause_recording(self):
        try:
            pass
        except Exception as e:
            print(f"Error pausing recording: {e}")

    def cancel_recording(self):
        try:
            pass
        except Exception as e:
            print(f"Error canceling recording: {e}")
            
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = AutoClickerApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error running the app: {e}")
        sys.exit(1)
