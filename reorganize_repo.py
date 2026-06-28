import os
import shutil
from pathlib import Path

# Define the root of your project
ROOT_DIR = Path(".")
SOURCE_DIR = ROOT_DIR / "Neurofinance" / "NeuroFininace" / "NDS-ImprovedModels"

# Desired structure
STRUCTURE = {
    "data/raw": ["nifty_bank_pre_covid.csv", "nifty_bank_post_covid.csv"],
    "data/processed": ["*normalized.csv", "*scaler_info.txt"],
    "data/features": ["brain_activation*.csv"],
    "src/data_processing": ["fix_data_leakage.py", "analyze_splitting_impact.py", "compare_split_methods.py"],
    "src/models": ["generate_ml_based_nds.py", "compare_rule_vs_ml_nds.py", "risk_system_observations.py", "check_dominance_claim.py", "check_risk_dominance.py"],
    "src/statistical_tests": ["run_statistical_tests.py", "run_statistical_tests_CORRECTED.py", "comprehensive_statistical_validation.py", "calculate_activation_frequencies.py"],
    "src/visualization": ["create_*.py", "combine_images_side_by_side.py"],
    "results/metrics": ["random_vs_chronological_comparison.csv", "rule_vs_ml_comparison_*.csv", "statistical_tests_*.csv"],
    "paper": ["*RESEARCH_PAPER*.tex", "*.tex"], # We'll handle specifics below
    "docs": ["*.md", "text.txt"]
}

def create_structure():
    print("Creating directories...")
    for folder in STRUCTURE.keys():
        (ROOT_DIR / folder).mkdir(parents=True, exist_ok=True)
    
    # Extra folders
    for extra in ["experiments", "results/figures", "results/tables", "paper/figures", "paper/sections", "scripts"]:
        (ROOT_DIR / extra).mkdir(parents=True, exist_ok=True)

def move_files():
    print("Moving files...")
    if not SOURCE_DIR.exists():
        print(f"Source directory {SOURCE_DIR} not found. Please run this script from the workspace root.")
        return

    # Move files from NDS-ImprovedModels
    for dest_folder, patterns in STRUCTURE.items():
        dest_path = ROOT_DIR / dest_folder
        for pattern in patterns:
            for file_path in SOURCE_DIR.glob(pattern):
                # Don't move README if it accidentally gets caught in docs
                if file_path.name == "README.md":
                    continue
                
                # Special routing for LaTeX figures
                if "figure" in file_path.name.lower() and file_path.suffix == ".tex":
                    target = ROOT_DIR / "paper/figures" / file_path.name
                else:
                    target = dest_path / file_path.name
                
                if file_path.is_file():
                    print(f"Moving {file_path.name} -> {target.parent}")
                    shutil.move(str(file_path), str(target))
    
    # Also grab files from the parent Neurofinance folder if any
    for tex_file in (ROOT_DIR / "Neurofinance" / "NeuroFininace").glob("*.tex"):
        if "figure" in tex_file.name.lower():
            shutil.move(str(tex_file), str(ROOT_DIR / "paper/figures" / tex_file.name))
        else:
            shutil.move(str(tex_file), str(ROOT_DIR / "paper" / tex_file.name))

if __name__ == "__main__":
    create_structure()
    move_files()
    print("Reorganization complete!")
