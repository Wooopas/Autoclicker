


# 🎯 AutoClicker

**A powerful, user-friendly AutoClicker that works everywhere, anytime.**

A modern mouse automation tool built with Python and CustomTkinter, featuring global hotkeys, customizable themes, and precise positioning controls. The concept was not invented by me in any way - I just wanted a small, efficient project for personal use.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/yourusername/autoclicker)

## 📷 Screenshots

### Dark Theme
<img width="393" height="790" alt="image" src="https://github.com/user-attachments/assets/c8dd1f66-3265-4c67-a49a-b3b3fc4b087b" />

### Light Theme  
<img width="393" height="787" alt="image" src="https://github.com/user-attachments/assets/c56a0fa3-309f-4fd2-9516-2dd055b31760" />

### 🎯 **Core Functionality**
1. **Automatic Clicking**:
   - Simulate **single** or **double** clicks with **left** or **right** mouse buttons
   - Precise cursor positioning with **X/Y coordinate** inputs

2. **Adjustable Click Interval**:
   - Set click intervals from **50ms to 5000ms** with real-time slider feedback
   - Live interval display showing current timing

3. **Flexible Repeat Modes**:
   - **Fixed Times**: Click a specific number of times and stop automatically
   - **Until Stopped**: Continuous clicking until manually stopped

### 🌐 **Global Hotkey System**
4. **Dual Hotkey Support**:
   - **Toggle hotkey** (default: F4) - Start/stop clicking from anywhere
   - **Force stop hotkey** (default: F5) - Emergency stop from any application
   - **Customizable keybinds** - Change hotkeys to any key you prefer

5. **System-Wide Operation**:
   - Works even when the application is minimized or in background
   - Global hotkeys function across all applications

### 📍 **Smart Positioning**
6. **Advanced Cursor Position**:
   - **Visual coordinate system** with color-coded X (blue) and Y (green) inputs
   - **Pick location tool** with 3-second countdown for precise positioning
   - **Real-time position display** showing current coordinates
   - Manual coordinate entry with input validation

### 🎨 **Modern User Interface**
7. **Customizable Appearance**:
   - **Dark/Light theme** toggle with optimized contrast
   - **Custom color picker** for 6 different UI elements:
     - Header background, accent colors, success/error colors, coordinate colors
   - **Always on top** option to keep the window visible

8. **Professional Design**:
   - Modern **CustomTkinter** interface with smooth animations
   - **Responsive layout** with clear visual hierarchy
   - **Intuitive controls** with emoji icons and descriptive labels

### ⚡ **Quality of Life Features**
9. **User-Friendly Experience**:
   - **Live feedback** for all settings and status updates
   - **Error handling** with helpful error messages
   - **Session persistence** for custom colors and settings
   - **Compact design** optimized for efficiency without sacrificing functionality

10. **Advanced Controls**:
    - **Info dialog** with hotkey reference
    - **Keybind customization** dialog for easy hotkey changes
    - **Color reset** option to restore default appearance
    - **Status indicators** with color-coded ready/clicking states

## 🚀 Installation

### Option 1: Download Executable (Recommended)
1. Go to [Releases](https://github.com/wooopas/autoclicker/releases)
2. Download the latest `AutoClicker.exe`
3. Run the executable (no installation required)

### Option 2: Run from Source
1. **Clone the repository**:
   ```
   git clone https://github.com/wooopas/autoclicker.git
   cd autoclicker
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```
   python auto.py
   ```

## 📋 Requirements

```
customtkinter>=5.2.0
pynput>=1.7.6
pyautogui>=0.9.54
```

**Python Version**: 3.7 or higher

## 🎮 Quick Start

1. **Set Click Position**:
   - Click "Pick Location" and move your mouse to desired position
   - Or manually enter X/Y coordinates

2. **Configure Settings**:
   - Choose click type (single/double)
   - Select mouse button (left/right)
   - Set click interval and repeat mode

3. **Start Automation**:
   - Press **F4** or click "Start" button
   - Use **F5** for emergency stop
   - Hotkeys work from any application!

## ⚙️ Usage Tips

- **Global Hotkeys**: F4 and F5 work even when the app is minimized
- **Always on Top**: Keep the window visible while working in other applications
- **Theme Switching**: Instantly switch between dark and light modes
- **Custom Colors**: Personalize the interface with your preferred colors
- **Emergency Stop**: F5 will always stop clicking, even if the app seems unresponsive

## 🔧 Building from Source

To create your own executable:

```
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed auto.py
```

## 🛡️ Security Note

Some antivirus software may flag the executable due to global hotkey functionality. This is a false positive - the application is completely safe and doesn't collect any data.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## ⭐ Support

If you find this project helpful, please give it a star! It helps others discover the tool.

---

**Made with ❤️ by Wooopas**
