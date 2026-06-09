import os
import shutil
from pathlib import Path

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

    print(f"🧹 Scanning and organizing: {DOWNLOADS_DIR}\n")
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
                target_dir = DOWNLOADS_DIR / category
                target_dir.mkdir(exist_ok=True)  # Create folder if it doesn't exist
                
                destination = target_dir / item.name
                
                # Prevent overwriting if a file with the same name already exists
                if destination.exists():
                    destination = target_dir / f"{item.stem}_copy{file_ext}"

                shutil.move(str(item), str(destination))
                print(f"📁 Moved: {item.name} ➡️ /{category}")
                files_moved += 1
                moved = True
                break
        
        # Optional: Catch-all for miscellaneous files not defined in FILE_CATEGORIES
        if not moved and file_ext != "":
            others_dir = DOWNLOADS_DIR / "Others"
            others_dir.mkdir(exist_ok=True)
            destination = others_dir / item.name
            
            if not destination.exists():
                shutil.move(str(item), str(destination))
                print(f"📁 Moved unknown file: {item.name} ➡️ /Others")
                files_moved += 1

    print(f"\n✨ Clean-up complete! Organized {files_moved} files.")

if __name__ == "__main__":
    clean_downloads()