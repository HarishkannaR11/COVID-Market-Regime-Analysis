import os
import shutil
from pathlib import Path

ROOT = Path.cwd()

destinations = {
    # Statistical Validation outputs
    "paradox": "experiments/statistical_validation/outputs/figures",
    "statistical": "experiments/statistical_validation/outputs/figures",
    "tests": "experiments/statistical_validation/outputs/figures",
    "significance": "experiments/statistical_validation/outputs/figures",
    "effect_sizes": "experiments/statistical_validation/outputs/figures",
    
    # Brain Activation outputs
    "activation": "experiments/brain_activation_analysis/outputs/figures",
    
    # Distribution Analysis Outputs
    "distribution": "experiments/distribution_analysis/outputs/figures",
    "boxplot": "experiments/distribution_analysis/outputs/figures",
    "histogram": "experiments/distribution_analysis/outputs/figures",
    "kde": "experiments/distribution_analysis/outputs/figures",
    "qqplot": "experiments/distribution_analysis/outputs/figures",
    "return": "experiments/distribution_analysis/outputs/figures",
    
    # Timeseries & Regimes outputs
    "timeseries": "experiments/timeseries_analysis/outputs/figures",
    "regime": "experiments/timeseries_analysis/outputs/figures",
    
    # Comparison Models
    "comparison": "experiments/rule_vs_ml_comparison/outputs/figures",
    "xgboost": "experiments/xgboost_nds_model/outputs/figures",
    
    # Paper Specific
    "architecture": "paper/figures",
    "framework": "paper/figures"
}

for path in ROOT.rglob("*"):
    # Target only image outputs 
    if path.suffix.lower() in [".png", ".jpg", ".jpeg", ".pdf"] and path.is_file():
        name = path.name.lower()
        
        # Don't move already organized paper figures
        if "paper" in path.parts:
            continue

        for key, folder in destinations.items():
            if key in name:
                target = ROOT / folder
                os.makedirs(target, exist_ok=True)

                try:
                    destination_file = target / path.name
                    if path != destination_file:
                        shutil.move(str(path), str(destination_file))
                        print(f"Moved {path.name} -> {folder}")
                except Exception as e:
                    print(f"Failed to move {path.name}: {e}")
                break # Only move to the first matching category
