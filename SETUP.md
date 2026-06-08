# How to run this project on your computer

I wrote this guide to help anyone who wants to test this project but might be new to setting up a Python environment or using PyCharm. This was the exact process I used to get everything working on my machine.

## 1. Things you need to install
You can't run the code without these. I used the latest versions:
* **Python 3.10 (or higher):** The engine that runs the code. (During installation, make sure to check the box that says "Add Python to PATH").
* **PyCharm Community Edition:** The IDE I used to write and run the code.
* **Git:** To clone the repository from GitHub.

## 2. Setting up the Project
Since Python projects use external libraries, you need to set up a virtual environment so the installation stays contained within this project.

1. Download this project as a ZIP from GitHub and extract it.
2. Open **PyCharm** and select **Open**.
3. Browse to the extracted folder and click **OK**.
4. If PyCharm asks to create a **Virtual Environment (venv)**, click **OK**.

## 3. Installing the Libraries
This project relies on two main tools: `customtkinter` for the modern UI and `watchdog` for the real-time folder monitoring.

1. At the bottom of PyCharm, click the **Terminal** tab.
2. Copy and paste the command below and hit **Enter**:

pip install customtkinter watchdog

3. Wait for the terminal to say "Successfully installed."

## 4. Understanding the Folder Structure
To see the app in action, you need a folder for the app to monitor.
1. Once the app is running, you will use the **Browse** button to select a directory.
2. **Tip:** I recommend creating a new folder on your Desktop named `OrganizeMe` and putting some random `.pdf`, `.jpg`, and `.docx` files in there to see them get sorted instantly!

## 5. Persistent Settings (JSON)
The app is designed to be user-friendly. Once you select a folder, it creates a `config.json` file.
1. You don't need to touch this file.
2. The app uses it to "remember" your last selected folder so you don't have to re-browse every time you open the program.

## 6. Launching
1. In the project file explorer on the left, find **app.py**.
2. Right-click it and select **Run 'app'**.
3. The "Deep Midnight Blue" Dark Mode window should appear!
4. Click **Browse** to pick your target folder, then click **Start Auto-Monitor**.

**Alternative:** If you just want to run the app without looking at the code, you can go to the `/output` folder and double-click **Smart File Organizer.exe** to launch the standalone version!
