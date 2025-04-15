import sys
import pyautogui
import time
from threading import Thread
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel, QComboBox, QLineEdit, QCheckBox, QDialog, QShortcut, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeySequence, QPalette, QColor

clicking = False
click_interval = 0.1
click_count = 1
click_button = 'left'
click_type = 'single'
cursor_x = 0
cursor_y = 0
repeat_mode = 'fixed'
hotkey = QKeySequence(Qt.Key_F4)

# Start clicking process in a new thread
def start_thread():
    try:
        print("Starting clicking thread...")
        thread = Thread(target=start_clicking)
        thread.daemon = True  # Ensures thread is stopped when the program exits
        thread.start()
    except Exception as e:
        show_error_message(f"Error starting thread: {e}")

# Clicking process logic using QTimer for non-blocking sleep
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
                print(f"Click count reached: {click_count}")
                break
            elif repeat_mode == 'until_stopped' and not clicking:
                break

            # Use QTimer to schedule the next click, keeping the event loop running
            QTimer.singleShot(int(click_interval * 1000), lambda: None)  # Delay for click_interval
            QApplication.processEvents()  # Ensure GUI is responsive during the sleep

    except Exception as e:
        show_error_message(f"Error during clicking: {e}")
        stop_clicking()

# Stop clicking process
def stop_clicking():
    global clicking
    clicking = False
    print("Autoclicker stopped.")

# Show error message in GUI
def show_error_message(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle("Error")
    msg_box.setText(message)
    msg_box.exec_()

# Main AutoClicker Application
class AutoClickerApp(QWidget):
    def __init__(self):
        super().__init__()
        try:
            self.init_ui()
            self.set_dark_mode()
            self.shortcut = QShortcut(QKeySequence(hotkey), self)
            self.shortcut.activated.connect(self.toggle_clicking)  # Toggle between start/stop
        except Exception as e:
            show_error_message(f"Error initializing GUI: {e}")
            sys.exit(1)

    def init_ui(self):
        try:
            self.setWindowTitle('AutoClicker')
            self.setGeometry(100, 100, 400, 400)

            layout = QVBoxLayout()

            # Click interval section
            self.interval_label = QLabel(f'Click interval: {click_interval * 1000} ms', self)
            layout.addWidget(self.interval_label)

            self.interval_slider = QSlider(Qt.Horizontal, self)
            self.interval_slider.setRange(50, 5000)
            self.interval_slider.setValue(100)
            self.interval_slider.valueChanged.connect(self.set_click_interval)
            layout.addWidget(self.interval_slider)

            # Repeat times section
            self.repeat_label = QLabel('Repeat times (for Fixed option):', self)
            self.repeat_input = QLineEdit(self)
            self.repeat_input.setPlaceholderText("Enter number of times to click")
            layout.addWidget(self.repeat_label)
            layout.addWidget(self.repeat_input)

            # Click type section
            self.type_label = QLabel('Click type', self)
            layout.addWidget(self.type_label)

            self.type_combo = QComboBox(self)
            self.type_combo.addItems(['single', 'double'])
            self.type_combo.currentIndexChanged.connect(self.set_click_type)
            layout.addWidget(self.type_combo)

            # Mouse button section
            self.button_label = QLabel('Mouse Button', self)
            layout.addWidget(self.button_label)

            self.button_combo = QComboBox(self)
            self.button_combo.addItems(['left', 'right'])
            self.button_combo.currentIndexChanged.connect(self.set_click_button)
            layout.addWidget(self.button_combo)

            # Repeat mode checkbox
            self.repeat_checkbox = QCheckBox('Repeat Until Stopped', self)
            self.repeat_checkbox.stateChanged.connect(self.set_repeat_mode)
            layout.addWidget(self.repeat_checkbox)

            self.repeat_count_checkbox = QCheckBox('Repeat Fixed Times', self)
            self.repeat_count_checkbox.stateChanged.connect(self.set_repeat_mode)
            layout.addWidget(self.repeat_count_checkbox)

            # Cursor position section
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

            # Buttons for starting/stopping
            button_layout = QHBoxLayout()

            self.start_button = QPushButton(f'Start ({hotkey.toString()})', self)
            self.start_button.clicked.connect(self.toggle_clicking)
            button_layout.addWidget(self.start_button)

            self.stop_button = QPushButton('Stop', self)
            self.stop_button.clicked.connect(stop_clicking)
            button_layout.addWidget(self.stop_button)

            layout.addLayout(button_layout)

            # Hotkey dialog
            self.hotkey_button = QPushButton('Set Hotkey', self)
            self.hotkey_button.clicked.connect(self.open_hotkey_dialog)
            layout.addWidget(self.hotkey_button)

            # Dark/Light Mode Toggle Button
            self.theme_button = QPushButton("Toggle Dark/Light Mode", self)
            self.theme_button.clicked.connect(self.toggle_theme)
            layout.addWidget(self.theme_button)

            self.setLayout(layout)
        except Exception as e:
            show_error_message(f"Error setting up UI components: {e}")
            sys.exit(1)

    # Set click interval
    def set_click_interval(self):
        global click_interval
        try:
            click_interval = self.interval_slider.value() / 1000  # Convert ms to seconds
            self.interval_label.setText(f'Click interval: {click_interval * 1000} ms')
            print(f"Click interval set to {click_interval * 1000} ms")
        except ValueError as ve:
            show_error_message(f"Invalid value for interval: {ve}")
        except Exception as e:
            show_error_message(f"Unexpected error in setting click interval: {e}")

    # Set click type (single or double)
    def set_click_type(self):
        global click_type
        click_type = self.type_combo.currentText()
        print(f"Click type set to: {click_type}")

    # Set click button (left or right)
    def set_click_button(self):
        global click_button
        click_button = self.button_combo.currentText()
        print(f"Mouse button set to: {click_button}")

    # Set repeat mode (until stopped or fixed times)
    def set_repeat_mode(self):
        global repeat_mode, click_count
        try:
            if self.repeat_checkbox.isChecked():
                repeat_mode = 'until_stopped'
                print("Repeat mode set to 'Until Stopped'")
            elif self.repeat_count_checkbox.isChecked():
                repeat_mode = 'fixed'
                try:
                    click_count = int(self.repeat_input.text())
                    print(f"Fixed repeat mode set to {click_count} clicks")
                except ValueError:
                    show_error_message("Invalid value for repeat count")
            else:
                repeat_mode = 'none'
                print("Repeat mode set to 'None'")
        except Exception as e:
            show_error_message(f"Error setting repeat mode: {e}")

    # Update cursor position from input
    def update_cursor_position(self):
        global cursor_x, cursor_y
        try:
            cursor_x = int(self.x_input.text())
            cursor_y = int(self.y_input.text())
            print(f"Cursor position updated to: ({cursor_x}, {cursor_y})")
        except ValueError:
            pass

    # Pick location based on mouse position
    def pick_location(self):
        try:
            self.pick_button.setText("Picking... (3s)")
            QTimer.singleShot(3000, self.record_cursor_position)  
            print("Picking location...")
        except Exception as e:
            show_error_message(f"Error picking location: {e}")

    # Record cursor position
    def record_cursor_position(self):
        global cursor_x, cursor_y
        try:
            x, y = pyautogui.position()
            self.x_input.setText(str(x))
            self.y_input.setText(str(y))
            self.pick_button.setText("Pick Location")
            print(f"Cursor position recorded: ({x}, {y})")
        except Exception as e:
            show_error_message(f"Error recording cursor position: {e}")

    # Toggle start/stop clicking with hotkey (F4)
    def toggle_clicking(self):
        if clicking:
            stop_clicking()
        else:
            self.start_button.setDisabled(True)  # Disable start button while clicking
            print("Starting autoclicker...")
            start_thread()

    # Set dark mode UI
    def set_dark_mode(self):
        self.setStyleSheet("background-color: #2E2E2E; color: white;")
        QApplication.setStyle("Fusion")
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        QApplication.setPalette(dark_palette)

    # Set light mode UI
    def set_light_mode(self):
        self.setStyleSheet("background-color: white; color: black;")
        QApplication.setStyle("Fusion")
        light_palette = QPalette()
        light_palette.setColor(QPalette.Window, QColor(255, 255, 255))
        light_palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        QApplication.setPalette(light_palette)

    # Toggle dark/light mode
    def toggle_theme(self):
        if QApplication.palette().color(QPalette.Window) == QColor(53, 53, 53):  # Check if dark mode is active
            self.set_light_mode()
            print("Switched to Light Mode")
        else:
            self.set_dark_mode()
            print("Switched to Dark Mode")

    # Open hotkey dialog
    def open_hotkey_dialog(self):
        try:
            dialog = HotkeyDialog(self)
            dialog.exec_()
        except Exception as e:
            show_error_message(f"Error opening hotkey dialog: {e}")

    # Update hotkey in UI and functionality
    def update_hotkey(self, new_hotkey):
        global hotkey
        hotkey = new_hotkey
        print(f"Hotkey updated to: {hotkey.toString()}")
        self.start_button.setText(f"Start ({hotkey.toString()})")
        self.shortcut.setKey(hotkey)  # Update the QShortcut with the new hotkey
        self.start_button.setDisabled(False)  # Re-enable the start button after the hotkey is updated


# Hotkey dialog class
class HotkeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set Hotkey')
        self.setGeometry(200, 200, 250, 100)
        
        layout = QVBoxLayout()
        self.label = QLabel(f'Press a key to set as hotkey (default: {hotkey.toString()})', self)
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
            show_error_message(f"Error handling key press: {e}")


# Main entry point
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = AutoClickerApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        show_error_message(f"Error running the app: {e}")
        sys.exit(1)
