# --- EXTERNAL LIBRARIES ---
import customtkinter as ctk  # A modern wrapper for Tkinter (adds Dark Mode and modern widgets)
import threading  # Allows 'Multithreading' so the UI doesn't freeze during monitoring
import json  # Used for Persistent Storage (saving user settings to a file)
import os  # System tasks like checking if the config file exists
from pathlib import Path  # Path manipulation for the config file location
from datetime import datetime  # Timestamps for the UI log display

# Watchdog: An event-driven library that 'listens' to the OS for file changes
from watchdog.observers import Observer  # The background thread that watches the folder
from watchdog.events import FileSystemEventHandler  # The 'Listener' that triggers our code

from main import organize_files  # Import the logic we wrote in main.py


class WatcherHandler(FileSystemEventHandler):
    """ This class acts like an 'Ear'. It waits for a file change and then triggers the logic. """

    def __init__(self, callback_function):
        self.callback_function = callback_function

    def on_modified(self, event):
        # We only trigger if a file was changed/added, not a directory
        if not event.is_directory:
            self.callback_function()


class OrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW SETUP ---
        self.title("Smart File Organizer - Pro")
        self.geometry("600x500")

        # --- PERSISTENT SETTINGS ---
        # We load the last used folder from config.json so the user doesn't have to re-select it
        self.config_file = "config.json"
        self.current_path = self.load_settings()

        # State tracking
        self.is_monitoring = False
        self.observer = None

        # --- UI LAYOUT ---
        ctk.CTkLabel(self, text="Smart File Organizer", font=("Arial", 24, "bold")).pack(pady=20)

        # Folder Selection Frame
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.pack(pady=10, padx=20, fill="x")

        self.path_label = ctk.CTkLabel(self.path_frame, text=f"Folder: {self.current_path}", wraplength=350)
        self.path_label.pack(side="left", padx=10, pady=10)

        # Browse Button: Calls the Windows folder picker
        ctk.CTkButton(self.path_frame, text="Browse", width=80, command=self.browse_folder).pack(side="right", padx=10)

        self.status_indicator = ctk.CTkLabel(self, text="Status: IDLE", text_color="orange", font=("Arial", 14))
        self.status_indicator.pack()

        self.toggle_button = ctk.CTkButton(self, text="Start Auto-Monitor", command=self.toggle_monitoring,
                                           fg_color="green")
        self.toggle_button.pack(pady=20)

        # Scrollable Activity Log
        self.log_display = ctk.CTkTextbox(self, width=500, height=150)
        self.log_display.pack(pady=10)
        self.log_display.insert("0.0", "[System] Ready. Select a folder and click 'Start'.\n")

    # --- SETTINGS MANAGEMENT ---
    def browse_folder(self):
        """ Opens a file dialog and updates the app's target folder """
        new_path = ctk.filedialog.askdirectory()
        if new_path:
            self.current_path = new_path
            self.path_label.configure(text=f"Folder: {new_path}")
            self.save_settings(new_path)

    def save_settings(self, path):
        """ Writes the selected folder to a JSON file (Persistent Storage) """
        with open(self.config_file, "w") as f:
            json.dump({"last_path": path}, f)

    def load_settings(self):
        """ Reads the last used folder from JSON. Returns Home folder if file is missing. """
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f).get("last_path", str(Path.home()))
        return str(Path.home())

    # --- MONITORING CORE ---
    def toggle_monitoring(self):
        """ Switches the app between 'Live' and 'Idle' modes """
        if not self.is_monitoring:
            self.start_watching()
        else:
            self.stop_watching()

    def start_watching(self):
        """ Starts the Watchdog background thread """
        self.is_monitoring = True
        self.status_indicator.configure(text="Status: MONITORING...", text_color="lightgreen")
        self.toggle_button.configure(text="Stop Monitoring", fg_color="red")

        # We initialize the Watchdog observer
        self.observer = Observer()
        event_handler = WatcherHandler(self.trigger_logic)
        self.observer.schedule(event_handler, self.current_path, recursive=False)

        # Start monitoring in its own thread to keep the GUI responsive
        self.observer.start()
        self.log_display.insert("end", f"[*] Started monitoring: {self.current_path}\n")

    def stop_watching(self):
        """ Safely shuts down the background observer """
        self.is_monitoring = False
        self.status_indicator.configure(text="Status: IDLE", text_color="orange")
        self.toggle_button.configure(text="Start Auto-Monitor", fg_color="green")
        if self.observer:
            self.observer.stop()
            self.observer.join()  # Wait for the thread to fully close
        self.log_display.insert("end", "[!] Monitoring Stopped.\n")

    def trigger_logic(self):
        """ This is the bridge between the Watchdog and our main.py logic """
        organize_files(self.current_path)
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_display.insert("end", f"[{timestamp}] Auto-Organized successful!\n")
        self.log_display.see("end")  # Auto-scroll to the bottom of the log


if __name__ == "__main__":
    app = OrganizerApp()
    app.mainloop()