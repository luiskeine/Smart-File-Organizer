# --- EXTERNAL LIBRARIES ---
import customtkinter as ctk  # Library for the modern "Dark Mode" UI
import threading  # Allows us to run the background "Watchdog" without freezing the UI
import time  # Used to create human-readable timestamps for the log
from watchdog.observers import Observer  # The "Engine" that watches for file system changes
from watchdog.events import FileSystemEventHandler  # A "Listener" that tells us when a file is moved/created

# --- OUR CODE ---
# We import the logic function and the folder path we created in main.py
from main import organize_files, target_dir


class WatcherHandler(FileSystemEventHandler):
    """ 
    This class is like an 'Ear'. It listens for changes in the folder.
    When a file is added or modified, it tells the app to run the organization logic.
    """

    def __init__(self, callback_function):
        self.callback_function = callback_function

    def on_modified(self, event):
        # We check if the change was a file (not a folder)
        if not event.is_directory:
            # We call the 'trigger_logic' function in our main app
            self.callback_function()


class OrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Smart File Organizer - Pro")
        self.geometry("500x480")

        # State variables: Keeps track of whether the monitor is running or not
        self.is_monitoring = False
        self.observer = None

        # --- UI LAYOUT ---
        self.label = ctk.CTkLabel(self, text="Smart File Organizer", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # Status Indicator: Tells the user visually if the app is working or idle
        self.status_indicator = ctk.CTkLabel(self, text="Status: IDLE", text_color="orange", font=("Arial", 14))
        self.status_indicator.pack()

        # Main Button: This toggles the monitoring on and off
        self.toggle_button = ctk.CTkButton(self, text="Start Auto-Monitor",
                                           command=self.toggle_monitoring,
                                           fg_color="green",
                                           hover_color="darkgreen")
        self.toggle_button.pack(pady=20)

        # Activity Log: A scrollable text box to show a history of what happened
        self.log_display = ctk.CTkTextbox(self, width=420, height=180)
        self.log_display.pack(pady=10)
        self.log_display.insert("0.0", "[System] Ready. Click 'Start' to begin monitoring.\n")

    def toggle_monitoring(self):
        """ 
        The 'Brain' of the button. It switches the app between 
        Monitoring mode and Idle mode.
        """
        if not self.is_monitoring:
            self.start_watching()
        else:
            self.stop_watching()

    def start_watching(self):
        """ Turns on the background file monitor """
        self.is_monitoring = True

        # Update the UI visuals
        self.status_indicator.configure(text="Status: MONITORING...", text_color="lightgreen")
        self.toggle_button.configure(text="Stop Monitoring", fg_color="red", hover_color="darkred")
        self.log_display.insert("end", f"[*] Monitoring started in: {target_dir.name}\n")

        # MULTITHREADING: 
        # We start the Watchdog in its own thread. 
        # This is critical so the 'Window' stays responsive while the 'Monitor' waits for files.
        self.observer = Observer()
        event_handler = WatcherHandler(self.trigger_logic)
        self.observer.schedule(event_handler, str(target_dir), recursive=False)
        self.observer.start()

    def stop_watching(self):
        """ Safely shuts down the background monitor """
        self.is_monitoring = False

        # Reset UI visuals
        self.status_indicator.configure(text="Status: IDLE", text_color="orange")
        self.toggle_button.configure(text="Start Auto-Monitor", fg_color="green")

        if self.observer:
            self.observer.stop()  # Tells the watchdog to stop
            self.observer.join()  # Waits for the thread to fully close

        self.log_display.insert("end", "[!] Monitoring Stopped.\n")

    def trigger_logic(self):
        """ 
        This is the bridge between the Watchdog and your main.py logic.
        It runs every time a file change is detected.
        """
        organize_files()  # Calls your function from main.py

        # Update the log in the window with a timestamp
        current_time = time.strftime('%H:%M:%S')
        self.log_display.insert("end", f"[{current_time}] Auto-Organized successful!\n")
        self.log_display.see("end")  # Automatically scrolls to the bottom of the log


# --- START THE APP ---
if __name__ == "__main__":
    app = OrganizerApp()
    app.mainloop()  # This starts the UI loop