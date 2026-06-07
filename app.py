"""
Smart File Organizer - Professional GUI
Developed by: Luis
Features: Real-time monitoring, Modern Dark Mode UI, Persistent Settings
"""

# --- EXTERNAL LIBRARIES ---
import customtkinter as ctk  # Modern UI components
import threading  # To run monitoring in the background without freezing the UI
import json  # To save and load user settings (persistence)
import os  # Basic system and path operations
import sys  # Required for PyInstaller path handling
from pathlib import Path  # Modern object-oriented path handling
from datetime import datetime  # For timestamps in the activity log

# Watchdog: A library specifically for monitoring file system events
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import the core logic engine from your other file (main.py)
from main import organize_files


# --- PYINSTALLER PATH HELPER ---
def resource_path(relative_path):
    """
    Ensures that external files (like app_icon.ico) can be found
    when the app is bundled into a single .exe file.
    """
    try:
        # PyInstaller creates a temporary folder (_MEIPASS) when running the .exe
        base_path = sys._MEIPASS
    except Exception:
        # If running in a normal editor (PyCharm), use the current folder
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# --- EVENT HANDLER ---
class WatcherHandler(FileSystemEventHandler):
    """ Acts as the 'Ear' for the app, listening for folder changes. """

    def __init__(self, callback_function):
        self.callback_function = callback_function

    def on_modified(self, event):
        # We only trigger the logic if a file (not a folder) is modified/added
        if not event.is_directory:
            self.callback_function()


# --- MAIN APPLICATION CLASS ---
class OrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. WINDOW CONFIGURATION ---
        self.title("Smart File Organizer - Pro")
        self.geometry("600x520")

        # Appearance: Dark Mode with a Deep Midnight Blue background
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color="#001a33")

        # --- 2. ICON HANDLING ---
        # Using resource_path ensures the icon works in the built .exe
        try:
            icon_file = resource_path("app_icon_final.ico")
            self.iconbitmap(icon_file)
        except Exception as e:
            print(f"Icon failed to load: {e}")

        # --- 3. PERSISTENT SETTINGS ---
        # We store the last used path in a JSON file so the user doesn't have to browse every time
        self.config_file = "config.json"
        self.current_path = self.load_settings()
        self.is_monitoring = False
        self.observer = None

        # --- 4. UI LAYOUT ---

        # Main Title Label
        self.title_label = ctk.CTkLabel(self, text="Smart File Organizer",
                                        font=("Arial", 28, "bold"),
                                        text_color="#FFFFFF")
        self.title_label.pack(pady=(25, 10))

        # Folder Selection Box (Frame)
        self.path_frame = ctk.CTkFrame(self, fg_color="#002b53", corner_radius=10)
        self.path_frame.pack(pady=15, padx=30, fill="x")

        self.path_label = ctk.CTkLabel(self.path_frame,
                                       text=f"Folder: {self.current_path}",
                                       wraplength=350,
                                       text_color="#E0E0E0",
                                       font=("Arial", 12))
        self.path_label.pack(side="left", padx=15, pady=15)

        self.browse_btn = ctk.CTkButton(self.path_frame, text="Browse",
                                        width=80,
                                        command=self.browse_folder,
                                        font=("Arial", 12, "bold"))
        self.browse_btn.pack(side="right", padx=15)

        # Status Indicator (Shows Idle or Monitoring)
        self.status_indicator = ctk.CTkLabel(self, text="Status: IDLE",
                                             text_color="#FFA500",
                                             font=("Arial", 14, "bold"))
        self.status_indicator.pack(pady=5)

        # Start/Stop Toggle Button
        self.toggle_button = ctk.CTkButton(self, text="Start Auto-Monitor",
                                           command=self.toggle_monitoring,
                                           fg_color="#28a745",
                                           hover_color="#218838",
                                           font=("Arial", 14, "bold"),
                                           height=40)
        self.toggle_button.pack(pady=15)

        # Activity Log (Terminal-style Textbox)
        self.log_display = ctk.CTkTextbox(self, width=540, height=180,
                                          fg_color="#001226",  # Deep navy
                                          text_color="#00FF41",  # Matrix green
                                          font=("Consolas", 12),
                                          border_width=1,
                                          border_color="#002b53")
        self.log_display.pack(pady=(10, 20), padx=30)

        # Initial Welcome Message
        self.log_display.insert("0.0",
                                "[System] Initialization Complete.\n[System] Select a folder and click 'Start'.\n")

    # --- 5. LOGIC METHODS ---

    def browse_folder(self):
        """ Opens a file dialog for the user to select a folder. """
        new_path = ctk.filedialog.askdirectory()
        if new_path:
            self.current_path = new_path
            self.path_label.configure(text=f"Folder: {new_path}")
            self.save_settings(new_path)
            self.log_display.insert("end", f"[Config] Target changed to: {new_path}\n")
            self.log_display.see("end")

    def save_settings(self, path):
        """ Saves the selected folder path to config.json. """
        with open(self.config_file, "w") as f:
            json.dump({"last_path": path}, f)

    def load_settings(self):
        """ Loads the last used path. Defaults to User Home if not found. """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f).get("last_path", str(Path.home()))
            except:
                return str(Path.home())
        return str(Path.home())

    def toggle_monitoring(self):
        """ Starts or stops the background monitoring service. """
        if not self.is_monitoring:
            self.start_watching()
        else:
            self.stop_watching()

    def start_watching(self):
        """ Initializes and starts the Watchdog Observer. """
        if not os.path.exists(self.current_path):
            self.log_display.insert("end", "[Error] Folder path does not exist!\n")
            return

        self.is_monitoring = True
        self.status_indicator.configure(text="Status: MONITORING...", text_color="#00FF41")
        self.toggle_button.configure(text="Stop Monitoring", fg_color="#dc3545", hover_color="#c82333")

        # Set up the Watchdog observer
        self.observer = Observer()
        event_handler = WatcherHandler(self.trigger_logic)
        self.observer.schedule(event_handler, self.current_path, recursive=False)

        self.observer.start()
        self.log_display.insert("end", f"[*] Started monitoring: {self.current_path}\n")
        self.log_display.see("end")

    def stop_watching(self):
        """ Safely stops the background threads. """
        self.is_monitoring = False
        self.status_indicator.configure(text="Status: IDLE", text_color="#FFA500")
        self.toggle_button.configure(text="Start Auto-Monitor", fg_color="#28a745", hover_color="#218838")

        if self.observer:
            self.observer.stop()
            self.observer.join()  # Wait for thread to fully close

        self.log_display.insert("end", "[!] Monitoring Stopped.\n")
        self.log_display.see("end")

    def trigger_logic(self):
        """ Bridge function: Runs the organization script and logs the result. """
        organize_files(self.current_path)
        timestamp = datetime.now().strftime('%H:%M:%S')
        # We use 'end' to always append to the bottom of the log
        self.log_display.insert("end", f"[{timestamp}] Activity detected: Folder Organized!\n")
        self.log_display.see("end")  # Auto-scroll to the bottom


# --- 6. ENTRY POINT ---
if __name__ == "__main__":
    app = OrganizerApp()
    app.mainloop()