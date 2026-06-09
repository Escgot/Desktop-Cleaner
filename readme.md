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
- **Dry Run Mode:** Preview every move before it happens. The script defaults to a safe test mode that prints what *would* happen without touching any files.
- **Date-Based Subfolders:** Files are automatically sorted into `Year/Month` subfolders within each category (e.g., `/Images/2026/June/`), keeping things tidy long-term.
- **Automatic Duplicate Cleanup:** Uses MD5 hashing to detect files with identical content. Exact duplicates are deleted instead of being moved, saving disk space.
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

### 1. Dry Run Mode
By default, `DRY_RUN` is set to `True` at the top of `cleaner.py`. In this mode the script will only **print** what it would do:

```
🧹 [DRY RUN] Scanning and organizing: /Users/you/Downloads

[DRY RUN] Would move: photo.png ➡️ /Images/2026/June
[DRY RUN] Would move: report.pdf ➡️ /PDFs/2026/June
```

Once you're happy with the preview, open `cleaner.py` and flip the flag:

```python
DRY_RUN = False  # Now files will actually be moved
```

### 2. Date-Based Subfolders
Files are automatically organized into `Year/Month` subfolders based on their last-modified date. For example:

```
Downloads/
├── Images/
│   └── 2026/
│       └── June/
│           └── photo.png
├── Documents/
│   └── 2025/
│       └── December/
│           └── report.docx
└── Others/
    └── 2026/
        └── June/
            └── random.dat
```

This prevents individual category folders from becoming cluttered over time.

### 3. Automatic Duplicate Cleanup
Before moving a file, the script calculates its MD5 hash (a digital fingerprint of the file's contents) and compares it against every file already in the destination folder. If an exact match is found — even if the filenames differ — the duplicate is deleted instead of moved.

```
🗑️  Deleted duplicate: installer_copy.exe (matches installer.exe)
```

This runs automatically and respects **Dry Run** mode, so you can preview which duplicates would be removed before anything is deleted.

### 4. Change the Folder Path
By default, the script scans your default system Downloads folder using `Path.home() / "Downloads"`. If you want to clean your Desktop instead, open `cleaner.py` and `undo_cleaner.py` in a text editor and change that line to:

```python
DOWNLOADS_DIR = Path.home() / "Desktop"
```

### 5. Run Automatically on a Schedule

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