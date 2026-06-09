import os
import shutil
from pathlib import Path
from datetime import datetime

# Set to True to preview changes without moving files, False to actually move them
DRY_RUN = True

# Automatically detects your user profile's Downloads folder
DOWNLOADS_DIR = Path.home() / "Downloads"

# Define mappings of subfolders to their respective file extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"],
    "PDFs": [".pdf"],
    "InstallationFiles": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
    "Documents": [".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".csv", ".md"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Audio_Video": [".mp3", ".wav", ".mp4", ".mov", ".mkv", ".avi", ".flac"]
}

def clean_downloads():
    if not DOWNLOADS_DIR.exists():
        print(f"❌ Error: Could not find the folder at {DOWNLOADS_DIR}")
        return

    mode = "DRY RUN" if DRY_RUN else "LIVE"
    print(f"🧹 [{mode}] Scanning and organizing: {DOWNLOADS_DIR}\n")
    files_moved = 0

    # Iterate through every item in the Downloads folder
    for item in DOWNLOADS_DIR.iterdir():
        # Skip directories (we only want to sort loose files)
        if item.is_dir():
            continue

        # Get the file extension in lowercase
        file_ext = item.suffix.lower()
        
        # Track if the file found a home
        moved = False
        
        for category, extensions in FILE_CATEGORIES.items():
            if file_ext in extensions:
                # Sort into date-based subfolders: /Category/2026/June
                timestamp = item.stat().st_mtime
                file_date = datetime.fromtimestamp(timestamp)
                year_month = file_date.strftime("%Y/%B")  # e.g., "2026/June"

                target_dir = DOWNLOADS_DIR / category / year_month
                target_dir.mkdir(parents=True, exist_ok=True)
                
                destination = target_dir / item.name
                
                # Prevent overwriting if a file with the same name already exists
                if destination.exists():
                    destination = target_dir / f"{item.stem}_copy{file_ext}"

                if DRY_RUN:
                    print(f"[DRY RUN] Would move: {item.name} ➡️ /{category}")
                else:
                    shutil.move(str(item), str(destination))
                    print(f"📁 Moved: {item.name} ➡️ /{category}")
                files_moved += 1
                moved = True
                break
        
        # Optional: Catch-all for miscellaneous files not defined in FILE_CATEGORIES
        if not moved and file_ext != "":
            # Sort "Others" into date-based subfolders too
            timestamp = item.stat().st_mtime
            file_date = datetime.fromtimestamp(timestamp)
            year_month = file_date.strftime("%Y/%B")

            others_dir = DOWNLOADS_DIR / "Others" / year_month
            others_dir.mkdir(parents=True, exist_ok=True)
            destination = others_dir / item.name
            
            if not destination.exists():
                if DRY_RUN:
                    print(f"[DRY RUN] Would move: {item.name} ➡️ /Others")
                else:
                    shutil.move(str(item), str(destination))
                    print(f"📁 Moved unknown file: {item.name} ➡️ /Others")
                files_moved += 1

    print(f"\n✨ Clean-up complete! Organized {files_moved} files.")

if __name__ == "__main__":
    clean_downloads()