# Smart File Organizer (Python Automation)

A modern, real-time desktop application built to demonstrate high-speed automation, multi-threading, and a transition from Java to Pythonic architecture.

##  The Mission
Transitioning from a structured Java background, I built this tool to explore Python's automation capabilities. Unlike a simple script, this is a functional system service that monitors the file system in real-time and organizes clutter instantly.

##  Key Features
- **Real-Time "Watchdog" Service:** Uses event-driven programming to monitor folders and organize files the second they appear.
- **Universal Folder Selection:** Persistent settings saved via `JSON`, allowing users to pick any directory.
- **Modern Dark Mode UI:** Built with `CustomTkinter` for a professional, responsive user experience.
- **Multi-threaded Architecture:** The organization logic runs in a background thread, ensuring the UI never freezes during heavy file operations.

##  Technical Stack
- **Language:** Python 3.10+
- **Libraries:** `pathlib` (Object-oriented pathing), `shutil` (File ops), `watchdog` (OS events), `CustomTkinter` (GUI).
- **Architecture:** Rule-Based Classifier using Dictionaries for $O(1)$ lookup efficiency.

##  Java vs. Python: Lessons Learned
As a 3rd-year student with a background in Java, this project allowed me to translate enterprise concepts into Pythonic logic:
- **Data Structures:** Replaced complex `Switch` cases with Python `Dictionaries` for cleaner, faster mapping.
- **Memory Management:** Swapped Java's `try-with-resources` for Python’s `with` statements (Context Managers).
- **Concurrency:** Implemented `threading` to separate the "Worker" (Logic) from the "Interface" (UI), similar to Java's `Thread` class.

##  Installation
1. Clone the repo: `git clone https://github.com/luiskeine/Smart-File-Organizer.git`
2. Install requirements: `pip install customtkinter watchdog`
3. Run: `python app.py`
