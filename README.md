# COVID-Market-Regime-Analysis (Economic Nervous System)

This repository contains the research, code, and analytical findings for our study on market regime shifts surrounding the COVID-19 pandemic, analyzed through the novel lens of **Neurofinance** and the **Economic Nervous System**.

## Overview
Traditional financial models often rely on the assumption of perfectly logical and predictable behavior, ignoring the mixture of emotion and logic involved in real decision-making. This work introduces the **Financial Connectome** to investigate the long-standing paradox between neuroscience and finance by jointly examining emotional, risk-based, and rational decision systems at the market level.

Using NIFTY Bank Index data spanning 1,516 trading days across Pre-COVID (2017–2020) and Post-COVID (2020–2023) regimes, we engineered 25 market features to map onto five neuroanatomically-inspired brain systems (Value, Risk, Sentiment, Insula, and Control).

## Key Findings
- **The Market Paradox:** We discovered a counterintuitive combination of increased stability (longer regime persistence) and increased risk-dominance. The market did not revert to its pre-pandemic equilibrium.
- **Risk-Dominant Shift:** The Neuro-Decision Score (NDS) distribution shifted from a balanced 0.00 pre-COVID to a deeply negative -2.01 post-COVID, indicating a structural move toward risk-dominant decision-making.
- **System Activation:** All five mapped cognitive systems showed significantly increased post-pandemic activation frequencies.

## Repository Structure
- `src/`: Source code for feature engineering, machine learning pipelines, and statistical validation.
- `scripts/`: Executable scripts for generating analysis models and data processing.
- `paper/`: Complete LaTeX source code, figures, and tables for the final research paper.
- `results/`: Output visual analytics, time-series charts, correlation graphs, and stability heatmaps.

## Methodology
The analytical pipeline processes financial data through a neurocomputational framework, employing XGBoost classifiers to determine binary activation states. These are consolidated into a composite **Neuro-Decision Score (NDS)**, allowing for temporal and statistical persistence analysis that reveals the post-COVID market paradox.