import os
import shutil
from pathlib import Path

DOWNLOADS_DIR = Path.home() / "Downloads"

# The specific folders created by the cleaner script
CATEGORIES = ["Images", "PDFs", "InstallationFiles", "Documents", "Archives", "Audio_Video", "Others"]

def undo_clean():
    if not DOWNLOADS_DIR.exists():
        print(f"❌ Error: Could not find the folder at {DOWNLOADS_DIR}")
        return

    print(f"↩️ Reversing organization in: {DOWNLOADS_DIR}\n")
    files_moved_back = 0

    for category in CATEGORIES:
        category_dir = DOWNLOADS_DIR / category
        
        # Check if the subfolder actually exists
        if category_dir.exists() and category_dir.is_dir():
            # Loop through all files inside the subfolder
            for item in category_dir.iterdir():
                if item.is_file():
                    destination = DOWNLOADS_DIR / item.name
                    
                    # Prevent overwriting if a file somehow already exists in Downloads
                    if destination.exists():
                        destination = DOWNLOADS_DIR / f"restored_{item.stem}{item.suffix}"
                    
                    shutil.move(str(item), str(destination))
                    print(f"↩️ Restored: {item.name} ➡️ Downloads")
                    files_moved_back += 1
            
            # Delete the subfolder now that it's empty
            try:
                category_dir.rmdir()
                print(f"🗑️ Removed empty folder: /{category}")
            except OSError:
                print(f"⚠️ Could not remove /{category} (it might still contain folders or files)")

    print(f"\n✨ Undo complete! Restored {files_moved_back} files back to the main folder.")

if __name__ == "__main__":
    undo_clean()