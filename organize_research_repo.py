import os
import shutil
from pathlib import Path

ROOT = Path.cwd()

# folders to create
folders = [
    "data/raw",
    "data/processed",
    "data/features",
    "src/models",
    "src/statistical_tests",
    "src/visualization",
    "src/data_processing",
    "results/figures",
    "results/tables",
    "results/metrics",
    "paper/figures",
    "paper/sections",
    "docs",
    "scripts",
    "notebooks",
    "experiments/xgboost_nds",
    "experiments/rule_based_model",
    "experiments/temporal_split_validation"
]

for f in folders:
    os.makedirs(ROOT / f, exist_ok=True)

# folders to skip (already structured)
skip_dirs = {
    "data","src","results","paper","docs","scripts","experiments",".git",".venv","__pycache__", "notebooks"
}

def move_file(file_path):
    ext = file_path.suffix.lower()
    name = file_path.name.lower()
    target = None

    if ext == ".csv":
        if "normalized" in name:
            target = ROOT / "data/processed"
        elif "brain_activation" in name:
            target = ROOT / "data/features"
        elif "comparison" in name or "tests" in name or "summary" in name:
            target = ROOT / "results/metrics"
        else:
            target = ROOT / "data/raw"

    elif ext in [".png",".jpg",".jpeg",".pdf"]:
        target = ROOT / "results/figures"

    elif ext == ".py":
        if "stat" in name or "test" in name or "validate" in name or "check" in name or "calculate" in name:
            target = ROOT / "src/statistical_tests"
        elif "plot" in name or "graph" in name or "visual" in name or "create_" in name or "combine" in name:
            target = ROOT / "src/visualization"
        elif "model" in name or "xgboost" in name or "generate" in name or "risk" in name:
            target = ROOT / "src/models"
        elif "split" in name or "leakage" in name or "data" in name:
            target = ROOT / "src/data_processing"
        else:
            target = ROOT / "scripts"

    elif ext == ".tex":
        if "figure" in name:
            target = ROOT / "paper/figures"
        else:
            target = ROOT / "paper"
            
    elif ext == ".txt":
        if "scaler" in name:
            target = ROOT / "data/processed"
        else:
            target = ROOT / "docs"

    elif ext == ".md":
        # Keep the main README in the root
        if name == "readme.md":
            return
        target = ROOT / "docs"

    if target:
        destination = target / file_path.name
        try:
            # Don't overwrite if it already exists, or if destination is the source
            if not destination.exists() and file_path != destination:
                shutil.move(str(file_path), str(destination))
                print(f"Moved {file_path.name} → {target.relative_to(ROOT)}")
        except Exception as e:
            print(f"Failed to move {file_path.name}: {e}")

for path in ROOT.rglob("*"):
    # Skip organization script itself
    if path.name == "organize_research_repo.py" or path.name == "reorganize_repo.py":
         continue

    if path.is_file():
        # Check if file is inside a directory we should skip
        should_skip = False
        # Calculate path relative to root to correctly check parent folders
        try:
            rel_path = path.relative_to(ROOT)
            for part in rel_path.parts[:-1]: # exclude the filename itself
                if part in skip_dirs:
                    should_skip = True
                    break
        except ValueError:
            pass # path not relative to ROOT (shouldn't happen with Path.cwd)

        if not should_skip:
            move_file(path)

print("\nRepository reorganized successfully into ML Research Structure.")
print("Empty legacy directories can now be deleted manually.")
