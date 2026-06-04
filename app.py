# --- EXTERNAL LIBRARIES ---
import customtkinter as ctk
import threading
import json
import os
from pathlib import Path
from datetime import datetime

# Watchdog: For real-time file monitoring
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import the logic engine from your other file
from main import organize_files


class WatcherHandler(FileSystemEventHandler):
    """ Acts as the 'Ear' for the app, listening for folder changes. """

    def __init__(self, callback_function):
        self.callback_function = callback_function

    def on_modified(self, event):
        if not event.is_directory:
            self.callback_function()


class OrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        try:
            self.iconbitmap("app_icon.ico")
        except:
            pass  # This keeps the app running even if the icon is missing

        # --- THEME & WINDOW SETUP ---
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Smart File Organizer - Pro")
        self.geometry("600x520")
        self.configure(fg_color="#001a33")  # Deep Midnight Blue Background

        # --- PERSISTENT SETTINGS ---
        self.config_file = "config.json"
        self.current_path = self.load_settings()
        self.is_monitoring = False
        self.observer = None

        # --- UI LAYOUT ---

        # Main Title
        self.title_label = ctk.CTkLabel(self, text="Smart File Organizer",
                                        font=("Arial", 28, "bold"),
                                        text_color="#FFFFFF")
        self.title_label.pack(pady=(25, 10))

        # Folder Selection Frame (The "Selection" Box)
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

        # Status Indicator
        self.status_indicator = ctk.CTkLabel(self, text="Status: IDLE",
                                             text_color="#FFA500",  # Orange for Idle
                                             font=("Arial", 14, "bold"))
        self.status_indicator.pack(pady=5)

        # Start/Stop Button
        self.toggle_button = ctk.CTkButton(self, text="Start Auto-Monitor",
                                           command=self.toggle_monitoring,
                                           fg_color="#28a745",  # Green
                                           hover_color="#218838",
                                           font=("Arial", 14, "bold"),
                                           height=40)
        self.toggle_button.pack(pady=15)

        # Activity Log (The Terminal Style Box)
        self.log_display = ctk.CTkTextbox(self, width=540, height=180,
                                          fg_color="#001226",  # Near Black-Blue
                                          text_color="#00FF41",  # Matrix Green
                                          font=("Consolas", 12),  # Code-style font
                                          border_width=1,
                                          border_color="#002b53")
        self.log_display.pack(pady=(10, 20), padx=30)
        self.log_display.insert("0.0",
                                "[System] Initialization Complete.\n[System] Select a folder and click 'Start'.\n")

    # --- SETTINGS MANAGEMENT ---
    def browse_folder(self):
        new_path = ctk.filedialog.askdirectory()
        if new_path:
            self.current_path = new_path
            self.path_label.configure(text=f"Folder: {new_path}")
            self.save_settings(new_path)
            self.log_display.insert("end", f"[Config] Target changed to: {new_path}\n")
            self.log_display.see("end")

    def save_settings(self, path):
        with open(self.config_file, "w") as f:
            json.dump({"last_path": path}, f)

    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f).get("last_path", str(Path.home()))
            except:
                return str(Path.home())
        return str(Path.home())

    # --- MONITORING CORE ---
    def toggle_monitoring(self):
        if not self.is_monitoring:
            self.start_watching()
        else:
            self.stop_watching()

    def start_watching(self):
        if not os.path.exists(self.current_path):
            self.log_display.insert("end", "[Error] Folder path does not exist!\n")
            return

        self.is_monitoring = True
        self.status_indicator.configure(text="Status: MONITORING...", text_color="#00FF41")
        self.toggle_button.configure(text="Stop Monitoring", fg_color="#dc3545", hover_color="#c82333")

        self.observer = Observer()
        event_handler = WatcherHandler(self.trigger_logic)
        self.observer.schedule(event_handler, self.current_path, recursive=False)

        self.observer.start()
        self.log_display.insert("end", f"[*] Started monitoring: {self.current_path}\n")
        self.log_display.see("end")

    def stop_watching(self):
        self.is_monitoring = False
        self.status_indicator.configure(text="Status: IDLE", text_color="#FFA500")
        self.toggle_button.configure(text="Start Auto-Monitor", fg_color="#28a745", hover_color="#218838")

        if self.observer:
            self.observer.stop()
            self.observer.join()

        self.log_display.insert("end", "[!] Monitoring Stopped.\n")
        self.log_display.see("end")

    def trigger_logic(self):
        """ Runs the organization logic when a change is detected. """
        organize_files(self.current_path)
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_display.insert("end", f"[{timestamp}] Activity detected: Folder Organized!\n")
        self.log_display.see("end")


if __name__ == "__main__":
    app = OrganizerApp()
    app.mainloop()