# Smart File Organizer (Python Automation)

I built a real-time File Management System in Python to explore high-speed automation and system-level monitoring. My main goal was to transition my knowledge of structured Java development into the "Pythonic" world, focusing on background services and event-driven architecture. I chose Python for this project specifically to demonstrate my ability to build lightweight, high-performance utilities that improve workflow efficiency.

### How it works
* **The "Watchdog" Service:** The core of the app is an event-driven observer that "listens" to the file system. The moment a new file is dropped into the target folder, the system triggers the organization logic.
* **Auto-Categorization:** The app scans file extensions and instantly moves them into dedicated subfolders (e.g., .pdf to "Documents", .jpg to "Images").
* **Universal Folder Selection:** Unlike a basic script, this version includes a "Browse" feature, allowing it to work on any directory.
* **Live Activity Log:** A terminal-style text box with a "Matrix Green" font providing real-time feedback on every file move.
* **Persistent Memory:** Remembers the last folder you worked on using a JSON configuration system.

### Technical Implementation
* **Backend:** Python 3.10+
* **UI Framework:** CustomTkinter (Professional "Deep Midnight Blue" Dark Mode)
* **Monitoring:** Watchdog library (Event-driven file system monitoring)
* **Logic Engine:** Rule-Based Classifier using Dictionaries for O(1) lookup speed.
* **Concurrency:** Used the threading library to keep the UI responsive during background monitoring.
* **Packaging:** Used auto-py-to-exe to bundle the project into a standalone executable.

### Development Notes & Lessons
* **Java to Python Transition:** Replaced complex Java Switch cases with Python Dictionaries and swapped Java’s try-with-resources for Python’s with statements (Context Managers).
* **Concurrency & UX:** Learned how to separate "Worker" threads from "UI" threads to prevent system freezes.
* **Asset Management:** Created a resource_path() function to manage icons and assets inside a compressed EXE.
* **Clean Deployment:** Configured .gitignore to ensure only clean source code is pushed to GitHub.

### Setup

1. Clone the repository to your local machine.

2. Install the required libraries:
pip install customtkinter watchdog

3. Run the application:
python app.py

4. (Optional) A pre-built standalone executable is available in the /output folder.

---
Note: This project serves as a companion to my Java Queue Management System. Together, they demonstrate my versatility in applying different architectural patterns—from enterprise-level Java systems to high-speed Python automation tools.
