# Analysis of Financial Market Dynamics using Neurocomputing for COVID-19 Regime Transitions

**Authors:** Dr. N. Ahana Priyanka, R. Harishkanna, Dr. R. Sneka Nandhini  
**Institute:** Sri Sivasubramaniya Nadar College of Engineering, Chennai, India

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🧠 Overview

Financial markets are traditionally modeled as rational systems. However, real-world evidence shows collective decision-making is heavily influenced by emotional, risk-based, and control mechanisms. 

This repository contains the research, code, and analytical findings for our study introducing the **Financial Connectome**—a neuroscience-inspired pipeline that models the financial market as a collective cognitive network. We present the **Neuro-Decision Systems (NDS) framework** to investigate how market dynamics reorganize under the systemic stress of the COVID-19 pandemic.

## 📊 Dataset & Scope

- **Data Source:** NIFTY Bank Index
- **Timeframe:** 1,516 trading days (2017–2023)
- **Pre-COVID Regime:** Jan 2017 – Mar 2020 (773 days)
- **Post-COVID Regime:** Apr 2020 – Feb 2023 (743 days)

We engineered **22 distinct market features** across Price & Returns, Momentum & Trend, Volatility & Risk, and Volume dimensions.

## 🔬 The Five-System Neurocomputational Framework

We conceptually mapped collective market behavior to five neuroanatomically-inspired decision systems:

| System | Brain Region Analogy | Functional Role |
| :--- | :--- | :--- |
| **Value** | vmPFC | Greed / Opportunity (Reward seeking) |
| **Risk** | Amygdala | Fear / Safety (Threat detection) |
| **Sentiment** | dmPFC | Herd Mentality (Social following) |
| **Anomaly Detection** | Insula | Gut Feeling (Abnormality sensing) |
| **Control** | dlPFC | Strategy (Signal filtering) |

*Note: This mapping serves as a structural analogy to organize market dynamics and does not imply direct neurobiological measurement.*

## ⚙️ Methodology & Architecture

Our framework utilizes a four-stage pipeline:
1. **Data Ingestion Layer:** Processes historical NIFTY Bank Index data.
2. **Neuro-Financial Computing Layer:** Transforms raw data into 22 engineered features, translating noisy observations into structured inputs.
3. **Classification Layer:** Employs five independent **XGBoost** classifiers (one for each decision system) to predict binary activation states. The classifiers achieved robust predictive performance (96.05% – 98.25% test accuracy).
4. **Evaluation Layer:** Aggregates system outputs into the **Neuro-Decision Score (NDS)**, evaluating regime rigidity and flexibility.

## 📈 Key Findings

1. **The Market Paradox:** The market stabilized in a new, risk-aware state rather than reverting to its pre-pandemic equilibrium. We observed a counterintuitive combination of **increased stability** (temporal rigidity) and **increased risk-dominance**.
2. **Structural Shift to Risk-Dominance:** The Neuro-Decision Score (NDS) distribution shifted from a balanced state (near zero) Pre-COVID to a significantly negative distribution Post-COVID (indicating risk-dominance), confirmed via Kolmogorov–Smirnov and permutation tests ($p < 0.001$).
3. **Increased State Persistence:** Average state persistence (run length) increased by approximately 24%, while switching frequencies declined consistently across all systems. 
4. **Synchronized Hyperactivity:** Post-pandemic markets exhibited heightened sensitivity, with higher activation frequencies across all five cognitive systems. Systems began to fire simultaneously, indicating a loss of independent behavior.

## 📂 Repository Structure

- `Final Paper/`: Contains the complete LaTeX source (`main.tex`), figures, and the final compiled `.pdf` and `.docx` versions of the research paper.
- `src/`: Source code for feature engineering, machine learning pipelines, and statistical tests.
- `scripts/`: Executable scripts for generating analysis models and data processing.
- `results/`: Output visual analytics, time-series charts, correlation graphs, and stability heatmaps.

## 🚀 Applications

This framework provides a structured, quantifiable approach to analyzing market regime reconfiguration under sustained uncertainty. It has practical applications in macro-risk monitoring, systemic stress detection, and the evaluation of algorithmic trading strategies beyond traditional price-action models.