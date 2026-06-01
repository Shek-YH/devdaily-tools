"""File organizer - Sort files by type, date, or size."""

import os
import shutil
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

EXTENSION_MAP = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"},
    "documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv", ".json", ".yaml", ".yml", ".xml"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
    "code": {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".h", ".hpp", ".rs", ".go", ".rb", ".php", ".swift", ".kt", ".cs", ".sh", ".bat", ".ps1"},
    "audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"},
    "video": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"},
    "fonts": {".ttf", ".otf", ".woff", ".woff2", ".eot"},
    "installers": {".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".apk"},
}


def get_category(ext: str) -> str:
    ext = ext.lower()
    for category, extensions in EXTENSION_MAP.items():
        if ext in extensions:
            return category
    return "others"


def organize_files(directory: str, sort_by: str = "type", dry_run: bool = False):
    """Organize files in a directory based on the chosen strategy."""
    dir_path = Path(directory).resolve()
    if not dir_path.is_dir():
        console.print(f"[red]Error:[/] '{directory}' is not a valid directory.")
        return

    files = [f for f in dir_path.iterdir() if f.is_file()]
    if not files:
        console.print("[yellow]No files to organize.[/]")
        return

    table = Table(title=f"Organizing {len(files)} files by {sort_by}")
    table.add_column("File", style="cyan")
    table.add_column("→", style="dim")
    table.add_column("Destination", style="green")

    moves = []

    if sort_by == "type":
        for f in files:
            category = get_category(f.suffix)
            dest_dir = dir_path / category
            dest = dest_dir / f.name
            moves.append((f, dest))
            table.add_row(f.name, "→", str(dest.relative_to(dir_path)))

    elif sort_by == "date":
        for f in files:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            dest_dir = dir_path / mtime.strftime("%Y-%m")
            dest = dest_dir / f.name
            moves.append((f, dest))
            table.add_row(f.name, "→", str(dest.relative_to(dir_path)))

    elif sort_by == "size":
        for f in files:
            size_mb = f.stat().st_size / (1024 * 1024)
            if size_mb < 1:
                bucket = "small"
            elif size_mb < 100:
                bucket = "medium"
            else:
                bucket = "large"
            dest_dir = dir_path / bucket
            dest = dest_dir / f.name
            moves.append((f, dest))
            table.add_row(f.name, "→", str(dest.relative_to(dir_path)))

    console.print(table)

    if dry_run:
        console.print("\n[dim]Dry run — no files moved.[/]")
        return

    for src, dest in moves:
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Handle name conflicts by appending a counter
        if dest.exists():
            stem = dest.stem
            counter = 1
            while dest.exists():
                dest = dest.parent / f"{stem}_{counter}{dest.suffix}"
                counter += 1
        shutil.move(str(src), str(dest))

    console.print(f"\n[green]✓[/] Organized {len(moves)} files.")
