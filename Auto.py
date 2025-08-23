import sys
import pyautogui
import time
import threading
from pynput import keyboard
from pynput.keyboard import Listener
import customtkinter as ctk
from tkinter import messagebox, colorchooser
import tkinter as tk

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Global variables
clicking = False
click_interval = 0.1
click_count = 1
click_button = 'left'
click_type = 'single'
cursor_x = None
cursor_y = None
repeat_mode = 'fixed'
hotkey_start = 'f4'
hotkey_stop = 'f5'
app_instance = None
hotkey_listener = None

# Custom color variables
custom_colors = {
    "header_bg": None,
    "accent_color": None,
    "success_color": None,
    "error_color": None,
    "coordinate_x_color": None,
    "coordinate_y_color": None
}

def start_thread():
    try:
        if cursor_x is None or cursor_y is None:
            messagebox.showerror("Error", "Please set a click position first!")
            return False
        
        thread = threading.Thread(target=start_clicking, daemon=True)
        thread.start()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error starting thread: {e}")
        return False

def start_clicking():
    global clicking
    try:
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

            start_time = time.time()
            while time.time() - start_time < click_interval and clicking:
                time.sleep(0.01)
                
            if not clicking:
                break

    except Exception as e:
        print(f"Error during clicking: {e}")
    finally:
        stop_clicking()

def stop_clicking():
    global clicking
    clicking = False

def on_key_press(key):
    global clicking
    try:
        key_str = None
        if hasattr(key, 'name'):
            key_str = key.name.lower()
        elif hasattr(key, 'char') and key.char:
            key_str = key.char.lower()
        
        if key_str == hotkey_start:
            if clicking:
                stop_clicking()
            else:
                start_thread()
        elif key_str == hotkey_stop:
            stop_clicking()
            
    except Exception as e:
        print(f"Error in hotkey handler: {e}")

def setup_global_hotkeys():
    global hotkey_listener
    try:
        if hotkey_listener and hotkey_listener.running:
            hotkey_listener.stop()
        hotkey_listener = Listener(on_press=on_key_press)
        hotkey_listener.daemon = True
        hotkey_listener.start()
        return True
    except Exception as e:
        print(f"Error setting up global hotkeys: {e}")
        return False

def stop_global_hotkeys():
    global hotkey_listener
    try:
        if hotkey_listener and hotkey_listener.running:
            hotkey_listener.stop()
    except Exception as e:
        print(f"Error stopping global hotkeys: {e}")

class CompactAutoClicker(ctk.CTk):
    def __init__(self):
        super().__init__()
        global app_instance
        app_instance = self
        
        # Configure window
        self.title("🎯 AutoClicker by Wooopas")
        self.geometry("400x765")
        self.resizable(False, False)
        
        # Variables
        self.always_on_top_var = tk.BooleanVar(value=False)
        self.interval_var = tk.DoubleVar(value=100)
        self.repeat_count_var = tk.StringVar(value="1")
        self.click_type_var = tk.StringVar(value="single")
        self.mouse_button_var = tk.StringVar(value="left")
        self.repeat_mode_var = tk.StringVar(value="fixed")
        self.x_pos_var = tk.StringVar()
        self.y_pos_var = tk.StringVar()
        
        # Keep references to widgets that need color updates
        self.color_dependent_widgets = {}
        
        self.create_widgets()
        setup_global_hotkeys()
        self.update_ui_state()
        
    def get_colors(self):
        """Get colors based on current theme and custom colors"""
        is_dark = ctk.get_appearance_mode() == "Dark"
        
        # Default colors
        if is_dark:
            defaults = {
                "header_bg": ("#3B82F6", "#1E40AF"),
                "text_color": "white",
                "accent_color": ("#1f538d", "#14b8a6"),
                "success_color": ("#16a34a", "#22c55e"),
                "error_color": ("#dc2626", "#ef4444"),
                "success_hover": ("#15803d", "#16a34a"),
                "error_hover": ("#b91c1c", "#dc2626"),
                "primary_text": "white",
                "secondary_text": "gray",
                "coordinate_x_color": ("#3B82F6", "#2563EB"),
                "coordinate_y_color": ("#059669", "#047857")
            }
        else:
            defaults = {
                "header_bg": ("#2563EB", "#1D4ED8"),
                "text_color": "white",
                "accent_color": ("#1E40AF", "#0F172A"),
                "success_color": ("#059669", "#047857"),
                "error_color": ("#DC2626", "#B91C1C"),
                "success_hover": ("#047857", "#064E3B"),
                "error_hover": ("#B91C1C", "#991B1B"),
                "primary_text": ("#111827", "#000000"),
                "secondary_text": ("#374151", "#1F2937"),
                "coordinate_x_color": ("#2563EB", "#1D4ED8"),
                "coordinate_y_color": ("#059669", "#047857")
            }
        
        # Apply custom colors if set
        for key, custom_color in custom_colors.items():
            if custom_color:
                defaults[key] = custom_color
                
        return defaults
        
    def create_widgets(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Main frame with good padding
        main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=12, pady=12)
        
        colors = self.get_colors()
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, height=65, fg_color=colors["header_bg"])
        header_frame.pack(fill="x", pady=(0, 12))
        header_frame.pack_propagate(False)
        self.color_dependent_widgets['header_frame'] = header_frame
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🎯 AutoClicker", 
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=colors["text_color"]
        )
        title_label.pack(pady=(6, 0))
        self.color_dependent_widgets['title_label'] = title_label
        
        self.hotkey_label = ctk.CTkLabel(
            header_frame,
            text=f"Global: {hotkey_start.upper()} (Toggle) • {hotkey_stop.upper()} (Stop)",
            font=ctk.CTkFont(size=10),
            text_color=colors["text_color"]
        )
        self.hotkey_label.pack(pady=(0, 6))
        self.color_dependent_widgets['hotkey_label'] = self.hotkey_label
        
        # Always on top switch
        self.always_on_top_switch = ctk.CTkSwitch(
            main_frame,
            text="📌 Always on Top",
            command=self.toggle_always_on_top,
            variable=self.always_on_top_var,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=colors["primary_text"]
        )
        self.always_on_top_switch.pack(pady=(0, 12))
        self.color_dependent_widgets['always_on_top_switch'] = self.always_on_top_switch
        
        # Settings frame
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(fill="x", pady=(0, 12))
        
        # Interval section
        interval_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        interval_frame.pack(fill="x", padx=15, pady=(15, 8))
        
        interval_label = ctk.CTkLabel(
            interval_frame, 
            text="Interval:", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=colors["primary_text"]
        )
        interval_label.pack(side="left")
        self.color_dependent_widgets['interval_label'] = interval_label
        
        self.interval_display = ctk.CTkLabel(
            interval_frame, 
            text="100 ms", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=colors["accent_color"]
        )
        self.interval_display.pack(side="right")
        self.color_dependent_widgets['interval_display'] = self.interval_display
        
        self.interval_slider = ctk.CTkSlider(
            settings_frame,
            from_=50,
            to=5000,
            variable=self.interval_var,
            command=self.update_interval_display,
            height=18
        )
        self.interval_slider.pack(fill="x", padx=15, pady=(0, 12))
        
        # Controls row 1
        controls1_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        controls1_frame.pack(fill="x", padx=15, pady=(0, 8))
        
        self.click_type_menu = ctk.CTkOptionMenu(
            controls1_frame,
            values=["single", "double"],
            variable=self.click_type_var,
            command=self.update_click_type,
            width=140,
            height=32,
            font=ctk.CTkFont(size=12)
        )
        self.click_type_menu.pack(side="left", padx=(0, 15))
        
        self.mouse_button_menu = ctk.CTkOptionMenu(
            controls1_frame,
            values=["left", "right"],
            variable=self.mouse_button_var,
            command=self.update_mouse_button,
            width=140,
            height=32,
            font=ctk.CTkFont(size=12)
        )
        self.mouse_button_menu.pack(side="right")
        
        # Repeat mode row
        repeat_mode_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        repeat_mode_frame.pack(fill="x", padx=15, pady=(8, 8))
        
        repeat_mode_label = ctk.CTkLabel(
            repeat_mode_frame, 
            text="Repeat Mode:", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=colors["primary_text"]
        )
        repeat_mode_label.pack(side="left")
        self.color_dependent_widgets['repeat_mode_label'] = repeat_mode_label
        
        self.repeat_mode_menu = ctk.CTkOptionMenu(
            repeat_mode_frame,
            values=["fixed", "until_stopped"],
            variable=self.repeat_mode_var,
            command=self.update_repeat_mode,
            width=160,
            height=32,
            font=ctk.CTkFont(size=12)
        )
        self.repeat_mode_menu.pack(side="right")
        
        # Repeat count row
        repeat_count_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        repeat_count_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        repeat_count_label = ctk.CTkLabel(
            repeat_count_frame, 
            text="Repeat Count:", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=colors["primary_text"]
        )
        repeat_count_label.pack(side="left")
        self.color_dependent_widgets['repeat_count_label'] = repeat_count_label
        
        self.repeat_count_entry = ctk.CTkEntry(
            repeat_count_frame,
            textvariable=self.repeat_count_var,
            placeholder_text="Number",
            width=100,
            height=32,
            font=ctk.CTkFont(size=12)
        )
        self.repeat_count_entry.pack(side="right")
        self.repeat_count_entry.bind("<KeyRelease>", self.update_repeat_count)
        
        # Position frame
        position_frame = ctk.CTkFrame(main_frame)
        position_frame.pack(fill="x", pady=(0, 12))
        
        pos_title = ctk.CTkLabel(
            position_frame, 
            text="📍 Click Position", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=colors["primary_text"]
        )
        pos_title.pack(pady=(12, 10))
        self.color_dependent_widgets['pos_title'] = pos_title
        
        # Coordinate sections
        coordinates_container = ctk.CTkFrame(position_frame, fg_color="transparent")
        coordinates_container.pack(fill="x", padx=15, pady=(0, 10))
        
        # X Coordinate Section
        x_section = ctk.CTkFrame(coordinates_container, fg_color="transparent")
        x_section.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        x_label = ctk.CTkLabel(
            x_section,
            text="✖️ X (Horizontal)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=colors["coordinate_x_color"]
        )
        x_label.pack(anchor="w")
        self.color_dependent_widgets['x_label'] = x_label
        
        self.x_entry = ctk.CTkEntry(
            x_section,
            textvariable=self.x_pos_var,
            placeholder_text="X coordinate",
            height=32,
            font=ctk.CTkFont(size=12),
            border_color=colors["coordinate_x_color"]
        )
        self.x_entry.pack(fill="x", pady=(4, 0))
        self.x_entry.bind("<KeyRelease>", self.update_cursor_position)
        self.color_dependent_widgets['x_entry'] = self.x_entry
        
        # Y Coordinate Section  
        y_section = ctk.CTkFrame(coordinates_container, fg_color="transparent")
        y_section.pack(side="right", fill="x", expand=True, padx=(8, 0))
        
        y_label = ctk.CTkLabel(
            y_section,
            text="✖️ Y (Vertical)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=colors["coordinate_y_color"]
        )
        y_label.pack(anchor="w")
        self.color_dependent_widgets['y_label'] = y_label
        
        self.y_entry = ctk.CTkEntry(
            y_section,
            textvariable=self.y_pos_var,
            placeholder_text="Y coordinate",
            height=32,
            font=ctk.CTkFont(size=12),
            border_color=colors["coordinate_y_color"]
        )
        self.y_entry.pack(fill="x", pady=(4, 0))
        self.y_entry.bind("<KeyRelease>", self.update_cursor_position)
        self.color_dependent_widgets['y_entry'] = self.y_entry
        
        # Pick button
        self.pick_button = ctk.CTkButton(
            position_frame,
            text="📍 Pick Location (Move mouse & wait 3s)",
            command=self.pick_location,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36,
            fg_color=colors["accent_color"]
        )
        self.pick_button.pack(fill="x", padx=15, pady=(0, 10))
        self.color_dependent_widgets['pick_button'] = self.pick_button
        
        # Current position display
        self.position_display = ctk.CTkLabel(
            position_frame,
            text="Current: Not Set",
            font=ctk.CTkFont(size=11),
            text_color=colors["secondary_text"]
        )
        self.position_display.pack(pady=(0, 8))
        self.color_dependent_widgets['position_display'] = self.position_display
        
        # Status
        self.status_label = ctk.CTkLabel(
            position_frame,
            text="🟢 Ready",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=colors["success_color"]
        )
        self.status_label.pack(pady=(0, 12))
        self.color_dependent_widgets['status_label'] = self.status_label
        
        # Control buttons
        control_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        control_frame.pack(fill="x", pady=(0, 15))
        
        self.start_button = ctk.CTkButton(
            control_frame,
            text=f"▶️ Start ({hotkey_start.upper()})",
            command=self.toggle_clicking,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=45,
            fg_color=colors["success_color"],
            hover_color=colors["success_hover"],
            text_color="white"
        )
        self.start_button.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.color_dependent_widgets['start_button'] = self.start_button
        
        self.stop_button = ctk.CTkButton(
            control_frame,
            text=f"⏹️ Stop ({hotkey_stop.upper()})",
            command=stop_clicking,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=45,
            fg_color=colors["error_color"],
            hover_color=colors["error_hover"],
            text_color="white"
        )
        self.stop_button.pack(side="right", fill="x", expand=True, padx=(6, 0))
        self.color_dependent_widgets['stop_button'] = self.stop_button
        
        # Bottom options
        options_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        options_frame.pack(fill="x", pady=(0, 15))
        
        # Create two rows for buttons
        top_buttons = ctk.CTkFrame(options_frame, fg_color="transparent")
        top_buttons.pack(fill="x", pady=(0, 5))
        
        bottom_buttons = ctk.CTkFrame(options_frame, fg_color="transparent")
        bottom_buttons.pack(fill="x")
        
        # Top row: Info and Keybinds
        self.info_button = ctk.CTkButton(
            top_buttons,
            text="ℹ️ Info",
            command=self.show_hotkey_info,
            font=ctk.CTkFont(size=11, weight="bold"),
            height=32,
            width=120,
            fg_color="transparent",
            border_width=2,
            text_color=colors["primary_text"],
            border_color=colors["accent_color"]
        )
        self.info_button.pack(side="left", padx=(0, 6))
        self.color_dependent_widgets['info_button'] = self.info_button
        
        self.keybind_button = ctk.CTkButton(
            top_buttons,
            text="⌨️ Keybinds",
            command=self.open_keybind_dialog,
            font=ctk.CTkFont(size=11, weight="bold"),
            height=32,
            width=120,
            fg_color="transparent",
            border_width=2,
            text_color=colors["primary_text"],
            border_color=colors["accent_color"]
        )
        self.keybind_button.pack(side="right")
        self.color_dependent_widgets['keybind_button'] = self.keybind_button
        
        # Bottom row: Theme and Colors
        self.theme_button = ctk.CTkButton(
            bottom_buttons,
            text="🌓 Theme",
            command=self.toggle_theme,
            font=ctk.CTkFont(size=11, weight="bold"),
            height=32,
            width=120,
            fg_color="transparent",
            border_width=2,
            text_color=colors["primary_text"],
            border_color=colors["accent_color"]
        )
        self.theme_button.pack(side="left", padx=(0, 6))
        self.color_dependent_widgets['theme_button'] = self.theme_button
        
        # Color selector button
        self.color_button = ctk.CTkButton(
            bottom_buttons,
            text="🎨 Colors",
            command=self.open_color_selector,
            font=ctk.CTkFont(size=11, weight="bold"),
            height=32,
            width=120,
            fg_color="transparent",
            border_width=2,
            text_color=colors["primary_text"],
            border_color=colors["accent_color"]
        )
        self.color_button.pack(side="right")
        self.color_dependent_widgets['color_button'] = self.color_button
        
        # Start UI update timer
        self.after(100, self.update_ui_state)
    
    def open_color_selector(self):
        """Open color customization dialog"""
        color_window = ctk.CTkToplevel(self)
        color_window.title("🎨 Customize Colors")
        color_window.geometry("380x420")
        color_window.resizable(False, False)
        color_window.transient(self)
        color_window.grab_set()
        
        colors = self.get_colors()
        
        frame = ctk.CTkFrame(color_window)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        title = ctk.CTkLabel(
            frame, 
            text="🎨 Customize Colors", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=colors["primary_text"]
        )
        title.pack(pady=(15, 20))
        
        # Create color selection buttons
        color_options = [
            ("Header Background", "header_bg", "🔵"),
            ("Accent Color", "accent_color", "🔷"),
            ("Success Color", "success_color", "🟢"),
            ("Error Color", "error_color", "🔴"),
            ("X Coordinate Color", "coordinate_x_color", "🟦"),
            ("Y Coordinate Color", "coordinate_y_color", "🟩")
        ]
        
        def create_color_button(name, key, emoji):
            btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
            btn_frame.pack(fill="x", pady=5)
            
            label = ctk.CTkLabel(
                btn_frame, 
                text=f"{emoji} {name}:", 
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=colors["primary_text"]
            )
            label.pack(side="left")
            
            def pick_color():
                color = colorchooser.askcolor(title=f"Choose {name} Color")
                if color[1]:  # color[1] is the hex value
                    custom_colors[key] = color[1]
                    color_btn.configure(text=f"✓ {color[1]}")
                    print(f"Set {name} to {color[1]}")
            
            current_color = custom_colors[key] if custom_colors[key] else "Default"
            color_btn = ctk.CTkButton(
                btn_frame,
                text=f"Pick Color" if current_color == "Default" else f"✓ {current_color}",
                command=pick_color,
                width=120,
                height=28,
                font=ctk.CTkFont(size=10)
            )
            color_btn.pack(side="right")
        
        # Create all color selection buttons
        for name, key, emoji in color_options:
            create_color_button(name, key, emoji)
        
        # Buttons frame
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 10))
        
        def apply_colors():
            try:
                # Refresh the UI with new colors
                self.refresh_colors()
                messagebox.showinfo("Success", "Colors applied successfully!")
                color_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error applying colors: {e}")
        
        def reset_colors():
            global custom_colors
            custom_colors = {key: None for key in custom_colors}
            self.refresh_colors()
            messagebox.showinfo("Reset", "Colors reset to default!")
            color_window.destroy()
        
        apply_btn = ctk.CTkButton(
            button_frame, 
            text="Apply", 
            command=apply_colors, 
            width=80, 
            height=32,
            fg_color=colors["success_color"]
        )
        apply_btn.pack(side="left", padx=(0, 10))
        
        reset_btn = ctk.CTkButton(
            button_frame, 
            text="Reset", 
            command=reset_colors, 
            width=80, 
            height=32,
            fg_color=colors["error_color"]
        )
        reset_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            button_frame, 
            text="Cancel", 
            command=color_window.destroy, 
            width=80, 
            height=32,
            fg_color=colors["secondary_text"]
        )
        cancel_btn.pack(side="right")
    
    def update_interval_display(self, value):
        global click_interval
        click_interval = value / 1000
        colors = self.get_colors()
        self.interval_display.configure(text=f"{value:.0f} ms", text_color=colors["accent_color"])
    
    def update_click_type(self, value):
        global click_type
        click_type = value
    
    def update_mouse_button(self, value):
        global click_button
        click_button = value
    
    def update_repeat_mode(self, value):
        global repeat_mode
        repeat_mode = value
        if value == "until_stopped":
            self.repeat_count_entry.configure(state="disabled")
        else:
            self.repeat_count_entry.configure(state="normal")
    
    def update_repeat_count(self, event):
        global click_count
        try:
            click_count = int(self.repeat_count_var.get()) if self.repeat_count_var.get() else 1
        except ValueError:
            click_count = 1
    
    def update_cursor_position(self, event):
        global cursor_x, cursor_y
        try:
            x_text = self.x_pos_var.get()
            y_text = self.y_pos_var.get()
            
            if x_text and y_text:
                cursor_x = int(x_text)
                cursor_y = int(y_text)
                colors = self.get_colors()
                self.position_display.configure(text=f"Current: X={cursor_x}, Y={cursor_y}", text_color=colors["secondary_text"])
            elif x_text or y_text:
                x_val = x_text if x_text else "?"
                y_val = y_text if y_text else "?"
                colors = self.get_colors()
                self.position_display.configure(text=f"Current: X={x_val}, Y={y_val}", text_color=colors["secondary_text"])
            else:
                colors = self.get_colors()
                self.position_display.configure(text="Current: Not Set", text_color=colors["secondary_text"])
                cursor_x, cursor_y = None, None
        except ValueError:
            colors = self.get_colors()
            self.position_display.configure(text="Current: Invalid Input", text_color=colors["secondary_text"])
            pass
    
    def pick_location(self):
        colors = self.get_colors()
        self.pick_button.configure(text="📍 Picking in 3 seconds...", state="disabled", fg_color=colors["accent_color"])
        self.after(3000, self.record_cursor_position)
    
    def record_cursor_position(self):
        global cursor_x, cursor_y
        try:
            x, y = pyautogui.position()
            self.x_pos_var.set(str(x))
            self.y_pos_var.set(str(y))
            cursor_x, cursor_y = x, y
            colors = self.get_colors()
            self.position_display.configure(text=f"Current: X={x}, Y={y}", text_color=colors["secondary_text"])
            self.pick_button.configure(text="📍 Pick Location (Move mouse & wait 3s)", state="normal", fg_color=colors["accent_color"])
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
            colors = self.get_colors()
            self.pick_button.configure(text="📍 Pick Location (Move mouse & wait 3s)", state="normal", fg_color=colors["accent_color"])
    
    def toggle_clicking(self):
        global clicking
        if clicking:
            stop_clicking()
        else:
            start_thread()
    
    def toggle_always_on_top(self):
        if self.always_on_top_var.get():
            self.attributes("-topmost", True)
        else:
            self.attributes("-topmost", False)
    
    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
        
        self.after(100, self.refresh_colors)
    
    def refresh_colors(self):
        """Properly refresh all colors after theme/color change"""
        colors = self.get_colors()
        
        # Update all stored widget colors
        widget_color_map = {
            'header_frame': {'fg_color': colors["header_bg"]},
            'title_label': {'text_color': colors["text_color"]},
            'hotkey_label': {'text_color': colors["text_color"]},
            'always_on_top_switch': {'text_color': colors["primary_text"]},
            'interval_label': {'text_color': colors["primary_text"]},
            'interval_display': {'text_color': colors["accent_color"]},
            'repeat_mode_label': {'text_color': colors["primary_text"]},
            'repeat_count_label': {'text_color': colors["primary_text"]},
            'pos_title': {'text_color': colors["primary_text"]},
            'x_label': {'text_color': colors["coordinate_x_color"]},
            'y_label': {'text_color': colors["coordinate_y_color"]},
            'x_entry': {'border_color': colors["coordinate_x_color"]},
            'y_entry': {'border_color': colors["coordinate_y_color"]},
            'pick_button': {'fg_color': colors["accent_color"]},
            'position_display': {'text_color': colors["secondary_text"]},
            'status_label': {'text_color': colors["success_color"]},
            'start_button': {'fg_color': colors["success_color"], 'hover_color': colors["success_hover"]},
            'stop_button': {'fg_color': colors["error_color"], 'hover_color': colors["error_hover"]},
            'info_button': {'text_color': colors["primary_text"], 'border_color': colors["accent_color"]},
            'keybind_button': {'text_color': colors["primary_text"], 'border_color': colors["accent_color"]},
            'theme_button': {'text_color': colors["primary_text"], 'border_color': colors["accent_color"]},
            'color_button': {'text_color': colors["primary_text"], 'border_color': colors["accent_color"]}
        }
        
        # Apply colors to all widgets
        for widget_name, color_config in widget_color_map.items():
            if widget_name in self.color_dependent_widgets:
                widget = self.color_dependent_widgets[widget_name]
                try:
                    widget.configure(**color_config)
                except Exception as e:
                    print(f"Error updating {widget_name}: {e}")
    
    def show_hotkey_info(self):
        info_window = ctk.CTkToplevel(self)
        info_window.title("Hotkeys")
        info_window.geometry("300x210")
        info_window.resizable(False, False)
        info_window.transient(self)
        info_window.grab_set()
        
        colors = self.get_colors()
        
        frame = ctk.CTkFrame(info_window)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        title = ctk.CTkLabel(
            frame, 
            text="🌐 Global Hotkeys", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=colors["primary_text"]
        )
        title.pack(pady=(10, 15))
        
        info_text = f"""🔹 {hotkey_start.upper()}: Toggle Start/Stop
🔹 {hotkey_stop.upper()}: Force Stop

✨ Work from anywhere!"""
        
        info_label = ctk.CTkLabel(
            frame, 
            text=info_text, 
            font=ctk.CTkFont(size=11),
            text_color=colors["secondary_text"]
        )
        info_label.pack(pady=5)
        
        ctk.CTkButton(
            frame, 
            text="Close", 
            command=info_window.destroy, 
            width=80, 
            height=30,
            fg_color=colors["accent_color"]
        ).pack(pady=(10, 15))
    
    def open_keybind_dialog(self):
        keybind_window = ctk.CTkToplevel(self)
        keybind_window.title("Change Keybinds")
        keybind_window.geometry("320x280")
        keybind_window.resizable(False, False)
        keybind_window.transient(self)
        keybind_window.grab_set()
        
        colors = self.get_colors()
        
        frame = ctk.CTkFrame(keybind_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            frame, 
            text="⌨️ Change Keybinds", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=colors["primary_text"]
        )
        title.pack(pady=(15, 20))
        
        # Start hotkey
        start_frame = ctk.CTkFrame(frame, fg_color="transparent")
        start_frame.pack(fill="x", pady=(0, 10))
        
        start_label = ctk.CTkLabel(
            start_frame, 
            text="Start/Stop Key:", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=colors["primary_text"]
        )
        start_label.pack(side="left")
        
        start_var = tk.StringVar(value=hotkey_start.upper())
        start_entry = ctk.CTkEntry(start_frame, textvariable=start_var, width=60, height=28)
        start_entry.pack(side="right")
        
        # Stop hotkey
        stop_frame = ctk.CTkFrame(frame, fg_color="transparent")
        stop_frame.pack(fill="x", pady=(0, 15))
        
        stop_label = ctk.CTkLabel(
            stop_frame, 
            text="Force Stop Key:", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=colors["primary_text"]
        )
        stop_label.pack(side="left")
        
        stop_var = tk.StringVar(value=hotkey_stop.upper())
        stop_entry = ctk.CTkEntry(stop_frame, textvariable=stop_var, width=60, height=28)
        stop_entry.pack(side="right")
        
        # Info text
        info_label = ctk.CTkLabel(
            frame, 
            text="Enter single keys like: F4, F5, Q, E, etc.\n(Function keys and letters work best)", 
            font=ctk.CTkFont(size=10),
            text_color=colors["secondary_text"]
        )
        info_label.pack(pady=(0, 15))
        
        # Buttons
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        def apply_keybinds():
            global hotkey_start, hotkey_stop
            try:
                new_start = start_var.get().lower()
                new_stop = stop_var.get().lower()
                
                if new_start and new_stop:
                    hotkey_start = new_start
                    hotkey_stop = new_stop
                    
                    self.hotkey_label.configure(text=f"Global: {hotkey_start.upper()} (Toggle) • {hotkey_stop.upper()} (Stop)")
                    self.start_button.configure(text=f"▶️ Start ({hotkey_start.upper()})")
                    self.stop_button.configure(text=f"⏹️ Stop ({hotkey_stop.upper()})")
                    
                    setup_global_hotkeys()
                    
                    messagebox.showinfo("Success", f"Keybinds updated!\n{hotkey_start.upper()}: Start/Stop\n{hotkey_stop.upper()}: Force Stop")
                    keybind_window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter valid keys!")
            except Exception as e:
                messagebox.showerror("Error", f"Error updating keybinds: {e}")
        
        apply_btn = ctk.CTkButton(
            button_frame, 
            text="Apply", 
            command=apply_keybinds, 
            width=80, 
            height=30,
            fg_color=colors["success_color"],
            hover_color=colors["success_hover"]
        )
        apply_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            button_frame, 
            text="Cancel", 
            command=keybind_window.destroy, 
            width=80, 
            height=30, 
            fg_color=colors["secondary_text"]
        )
        cancel_btn.pack(side="right")
    
    def update_ui_state(self):
        global clicking
        colors = self.get_colors()
        
        if clicking:
            self.start_button.configure(
                text="⏸️ Stop",
                fg_color=colors["error_color"],
                hover_color=colors["error_hover"]
            )
            self.status_label.configure(
                text="🔴 Clicking...", 
                text_color=colors["error_color"]
            )
        else:
            self.start_button.configure(
                text=f"▶️ Start ({hotkey_start.upper()})",
                fg_color=colors["success_color"],
                hover_color=colors["success_hover"]
            )
            self.status_label.configure(
                text="🟢 Ready", 
                text_color=colors["success_color"]
            )
        
        self.after(100, self.update_ui_state)
    
    def on_closing(self):
        global clicking
        clicking = False
        stop_global_hotkeys()
        self.destroy()

if __name__ == "__main__":
    try:
        app = CompactAutoClicker()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except Exception as e:
        print(f"Error: {e}")
