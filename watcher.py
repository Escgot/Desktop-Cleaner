import time
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from cleaner import DOWNLOADS_DIR, FILE_CATEGORIES, DRY_RUN, file_hash

from datetime import datetime
import shutil


class DownloadHandler(FileSystemEventHandler):
    """Handles new files appearing in the watched directory."""

    def on_created(self, event):
        # Ignore directories and temporary/partial download files
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Skip common temporary download extensions
        temp_extensions = {".crdownload", ".part", ".tmp", ".download"}
        if file_path.suffix.lower() in temp_extensions:
            return

        # Brief delay to let the file finish writing
        time.sleep(1)

        # Make sure the file still exists (it may have been renamed by the browser)
        if not file_path.exists():
            return

        self._sort_file(file_path)

    def on_moved(self, event):
        """Browsers often download to a .tmp then rename; catch the final name."""
        if event.is_directory:
            return

        file_path = Path(event.dest_path)

        # Only process files landing directly in the watched directory
        if file_path.parent != DOWNLOADS_DIR:
            return

        time.sleep(0.5)
        if file_path.exists():
            self._sort_file(file_path)

    def _sort_file(self, item):
        """Sort a single file using the same logic as cleaner.py."""
        # Only process files sitting directly in the watched directory
        if item.parent != DOWNLOADS_DIR:
            return

        file_ext = item.suffix.lower()
        if file_ext == "":
            return

        moved = False

        for category, extensions in FILE_CATEGORIES.items():
            if file_ext in extensions:
                # Date-based subfolders
                timestamp = item.stat().st_mtime
                file_date = datetime.fromtimestamp(timestamp)
                year_month = file_date.strftime("%Y/%B")

                target_dir = DOWNLOADS_DIR / category / year_month
                target_dir.mkdir(parents=True, exist_ok=True)

                # Duplicate check via MD5 hash
                item_hash = file_hash(item)
                for existing in target_dir.iterdir():
                    if existing.is_file() and file_hash(existing) == item_hash:
                        if DRY_RUN:
                            print(f"[DRY RUN] Would delete duplicate: {item.name} (matches {existing.name})")
                        else:
                            item.unlink()
                            print(f"🗑️  Deleted duplicate: {item.name} (matches {existing.name})")
                        return

                destination = target_dir / item.name
                if destination.exists():
                    destination = target_dir / f"{item.stem}_copy{file_ext}"

                if DRY_RUN:
                    print(f"[DRY RUN] Would move: {item.name} ➡️ /{category}/{year_month}")
                else:
                    shutil.move(str(item), str(destination))
                    print(f"📁 Moved: {item.name} ➡️ /{category}/{year_month}")
                moved = True
                break

        # Catch-all for unrecognized extensions
        if not moved:
            timestamp = item.stat().st_mtime
            file_date = datetime.fromtimestamp(timestamp)
            year_month = file_date.strftime("%Y/%B")

            others_dir = DOWNLOADS_DIR / "Others" / year_month
            others_dir.mkdir(parents=True, exist_ok=True)
            destination = others_dir / item.name

            if not destination.exists():
                if DRY_RUN:
                    print(f"[DRY RUN] Would move: {item.name} ➡️ /Others/{year_month}")
                else:
                    shutil.move(str(item), str(destination))
                    print(f"📁 Moved: {item.name} ➡️ /Others/{year_month}")


def main():
    if not DOWNLOADS_DIR.exists():
        print(f"❌ Error: Could not find the folder at {DOWNLOADS_DIR}")
        sys.exit(1)

    mode = "DRY RUN" if DRY_RUN else "LIVE"
    print(f"👁️  [{mode}] Watching for new files in: {DOWNLOADS_DIR}")
    print("Press Ctrl+C to stop.\n")

    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, str(DOWNLOADS_DIR), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Watcher stopped.")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
