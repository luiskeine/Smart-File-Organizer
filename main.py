# --- EXTERNAL LIBRARIES ---
import os  # Basic system operations (like checking file paths)
import shutil  # High-level file operations (Specifically used for moving files)
from pathlib import Path  # Modern, object-oriented way to handle file paths (replaces old os.path)
from datetime import datetime  # Used to create timestamps for our activity log

# A Dictionary acting as a 'Mapping Key'
# In Java, this would be a HashMap. Using a dictionary gives us O(1) lookup speed.
FILE_TYPES = {
    ".pdf": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".zip": "Archives",
    ".mp4": "Videos",
}


def log_action(target_dir, message):
    """ Records movement history into a text file within the organized folder """
    log_file = Path(target_dir) / "organizer_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 'with' acts like Java's try-with-resources. It ensures the file closes automatically.
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def organize_files(target_path):
    """ Scans the folder and moves files based on their extension """
    target_dir = Path(target_path)

    # Safety Check: Ensure the folder exists before running
    if not target_dir.exists():
        return "Folder not found."

    files_moved = 0
    # .iterdir() is like a 'for-each' loop for every file in the directory
    for file_path in target_dir.iterdir():
        # Skip folders and our own log file to avoid infinite loops or errors
        if file_path.is_dir() or file_path.name == "organizer_log.txt":
            continue

        # Get the file extension (e.g., .jpg) and make it lowercase
        ext = file_path.suffix.lower()

        # Decide destination: use the map if known, otherwise put in 'Others'
        folder_name = FILE_TYPES.get(ext, "Others")

        dest_folder = target_dir / folder_name

        # Create the subfolder if it doesn't exist yet (mkdir = make directory)
        dest_folder.mkdir(exist_ok=True)

        try:
            # Atomic move operation: moves the file from current path to the new subfolder
            shutil.move(str(file_path), str(dest_folder / file_path.name))
            log_action(target_dir, f"Moved: {file_path.name} -> {folder_name}")
            files_moved += 1
        except Exception as e:
            # Catch block prevents a single 'File in Use' error from crashing the whole script
            print(f"Error moving {file_path.name}: {e}")

    return files_moved