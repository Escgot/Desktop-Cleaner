# 🧹 Automated Desktop & Downloads Cleaner

A production-ready, cross-platform Python automation system that monitors and cleans up your messy `Downloads` or `Desktop` directories. It intelligently categorizes files by extension, handles naming collisions safely, can group items by date, and includes a full **Undo** script to completely reverse changes.

---

## ✨ Features

- **Cross-Platform Compatibility:** Runs seamlessly on Windows, macOS, and Linux without any hardcoded paths.
- **Collision Protection:** Prevents file loss. If `document.pdf` already exists in the destination, subsequent files are automatically renamed to `document_copy.pdf`.
- **Smart Categorization:** Automatically groups files into clean, logical subfolders:
  - `/Images` (jpg, png, webp, heic...)
  - `/PDFs` (pdf)
  - `/InstallationFiles` (exe, msi, dmg, pkg...)
  - `/Documents` (docx, csv, txt, md...)
  - `/Archives` (zip, rar, 7z...)
  - `/Audio_Video` (mp3, mp4, mkv...)
  - `/Others` (Catch-all folder for unspecified types)
- **Safe Execution:** Skips active directories to preserve existing folder structures.
- **Reversible:** Accidentally ran it? Run the companion `undo_cleaner.py` script to seamlessly return all files to the main folder and delete the generated subfolders.

---

## 🚀 Quick Start Guide

### Step 1: Install Python
Ensure Python 3.x is installed on your computer. 
* **Windows Users:** Ensure you check the box that says **"Add python.exe to PATH"** during installation.

### Step 2: Download the Scripts
Save both scripts into a folder on your system (e.g., `C:\Users\YourName\Scripts\` or `~/Scripts/`):
1. **`cleaner.py`** — The primary sorting script.
2. **`undo_cleaner.py`** — The emergency reversal script.

### Step 3: Run the Script Manually
Open your terminal (macOS/Linux) or Command Prompt (Windows), navigate to your scripts directory, and execute:

**Windows:**
```bash
cd Documents\Scripts
python cleaner.py
```

**macOS / Linux:**
```bash
cd ~/Documents/Scripts
python3 cleaner.py
```

## ↩️ How to Undo Everything
If you need to return your folder to its original state, run the built-in undo mechanism:

**Windows:**

```bash
python undo_cleaner.py
```

**macOS / Linux:**

```bash
python3 undo_cleaner.py
```

## 🛠️ Advanced Customization & Autopilot

### 1. Change the Folder Path
By default, the script scans your default system Downloads folder using `Path.home() / "Downloads"`. If you want to clean your Desktop instead, open `cleaner.py` and `undo_cleaner.py` in a text editor and change that line to:

```python
DOWNLOADS_DIR = Path.home() / "Desktop"
```

### 2. Run Automatically on a Schedule

**Windows (Task Scheduler)**

Open Task Scheduler and select Create Basic Task.

Set the Trigger to Daily or When I log on.

Choose Start a Program as the action.

Set Program/script to python and add the full path to your script in the Add arguments box (e.g., `C:\Scripts\cleaner.py`).

**macOS & Linux (Cron Job)**

Open terminal and edit your crontab configuration: `crontab -e`.

To run the cleanup automatically every day at midnight, append this line:

```bash
0 0 * * * /usr/bin/python3 /Users/YourUsername/Scripts/cleaner.py
```

## 📝 License
This project is open-source and free to use or modify for personal and commercial purposes.