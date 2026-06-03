import os
import shutil
from pathlib import Path
from datetime import datetime

# 1. SETTINGS & CONFIGURATION
# Path.home() finds the current user's home folder (e.g., C:\Users\Luis)
# We use / to join folders because pathlib handles the backslashes for us automatically.
target_dir = Path.home() / "OneDrive" / "Desktop" / "OrganizeMe"

# A Dictionary acting as a 'Mapping Key'
# Key = File Extension | Value = Name of the destination folder
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


def log_action(message):
    """
    Records every file movement into a text file so the user has a history.
    """
    log_file = target_dir / "organizer_log.txt"
    # Create a human-readable timestamp (Year-Month-Day Hour:Minute:Second)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 'with' ensures the file closes automatically (similar to a try-with-resources in Java)
    # 'a' means Append: it adds to the end of the file instead of overwriting it.
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def organize_files():
    # 2. VALIDATION
    # Check if the folder exists before starting to prevent errors
    if not target_dir.exists():
        print(f"❌ Folder not found.")
        return

    print(f"📂 Scanning: {target_dir}...")
    files_moved = 0

    # 3. SCANNING PHASE
    # .iterdir() is like a 'for-each' loop for every file in the folder
    for file_path in target_dir.iterdir():

        # We only want to move FILES.
        # We skip directories (folders) and our own log file.
        if file_path.is_dir() or file_path.name == "organizer_log.txt":
            continue

        # Get the extension (e.g., '.jpg') and make it lowercase just in case
        ext = file_path.suffix.lower()

        # 4. CLASSIFICATION PHASE
        # Check if the extension exists in our FILE_TYPES dictionary
        if ext in FILE_TYPES:
            folder_name = FILE_TYPES[ext]
        else:
            # If the extension isn't in our list, put it in 'Others'
            folder_name = "Others"

            # Define where the file is going
        dest_folder = target_dir / folder_name

        # Create the subfolder if it doesn't exist yet (mkdir = make directory)
        dest_folder.mkdir(exist_ok=True)

        # 5. EXECUTION PHASE
        try:
            # Move the file from its current path to the new subfolder path
            shutil.move(str(file_path), str(dest_folder / file_path.name))

            # Prepare a success message
            msg = f"Moved: {file_path.name} -> {folder_name}"
            print(f"✅ {msg}")

            # Record this move in our log file
            log_action(msg)
            files_moved += 1

        except Exception as e:
            # If a file is 'In Use' (e.g., a Word doc is open), it will fail.
            # This catch block prevents the whole script from crashing.
            print(f"⚠️ Error moving {file_path.name}: {e}")

    # Final summary for the user
    if files_moved > 0:
        print(f"\n✨ Done! Organized {files_moved} files. Check 'organizer_log.txt' for history.")
    else:
        print("No new files found to organize.")


# The entry point of the script (Like public static void main in Java)
if __name__ == "__main__":
    organize_files()