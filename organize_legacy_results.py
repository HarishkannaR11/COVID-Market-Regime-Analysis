import os
import shutil
from pathlib import Path

ROOT = Path.cwd()
SOURCE = ROOT / "Neurofinance" / "NeuroFininace" / "NDS-ImprovedModels" / "results"

def move_legacy_results():
    if not SOURCE.exists():
        print(f"Source folder not found: {SOURCE}")
        return

    for path in SOURCE.rglob("*"):
        if not path.is_file():
            continue
            
        ext = path.suffix.lower()
        name = path.name.lower()
        parent_name = path.parent.name
        
        # Determine target directory based on the new ML structure
        if ext == ".csv":
            target = ROOT / "results/metrics"
        elif ext in [".md", ".txt"]:
            target = ROOT / "docs"
        elif ext == ".py":
            if "create" in name or "chart" in name or "plot" in name:
                target = ROOT / "src/visualization"
            else:
                target = ROOT / "src/statistical_tests"
        else:
            target = ROOT / "results"

        target.mkdir(parents=True, exist_ok=True)
        
        # Check for filename collisions and prefix with parent context if a duplicate exists
        dest_file = target / path.name
        if dest_file.exists():
            new_name = f"{parent_name}_{path.name}"
            dest_file = target / new_name
            
        # Move to destination
        try:
            shutil.move(str(path), str(dest_file))
            print(f"Moved: {parent_name}/{path.name} -> {target.relative_to(ROOT)}/{dest_file.name}")
        except Exception as e:
            print(f"Error moving {path.name}: {e}")

if __name__ == "__main__":
    print("Organizing legacy results folder...")
    move_legacy_results()
    print("Done!")
