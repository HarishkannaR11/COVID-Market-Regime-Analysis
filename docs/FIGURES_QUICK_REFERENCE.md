# Statistical Validation Figures - Quick Reference

## Generated Figures (All 300 DPI, Publication-Ready)

### Figure 1: NDS Statistical Validation (4-Panel)

**Location:** `NDS-ImprovedModels/Publication_Figures/nds_statistical_validation_4panel.png` (+ PDF)

**Layout:**
```
┌─────────────────────────────────────────┐
│  Pre-COVID NDS   │   Post-COVID NDS     │
│  Distribution    │   Distribution       │
│  (Panel A)       │   (Panel B)          │
├──────────────────┴──────────────────────┤
│  Distribution    │   Q-Q Plot           │
│  Comparison      │   (Theoretical       │
│  (KS Test)       │   Quantiles)         │
│  (Panel C)       │   (Panel D)          │
└─────────────────────────────────────────┘
```

**Key Statistics Shown:**
- Panel A: Pre-COVID (n=773, μ=0.000, σ=2.014)
- Panel B: Post-COVID (n=743, μ=-2.010, σ=4.853)
- Panel C: KS Test (D=0.1097, p=1.95×10⁻⁴, d=0.291)
- Panel D: Q-Q regression (R², slope, fit)

**Purpose:** Comprehensive distributional analysis matching reference layout

---

### Figure 2: Three Statistical Tests (3-Panel)

**Location:** `NDS-ImprovedModels/Publication_Figures/three_statistical_tests.png` (+ PDF)

**Layout:**
```
┌────────────────────────────────────────────────────────┐
│  KS Test CDF  │  Permutation Test  │  Mann-Whitney U  │
│  Comparison   │  Null Distribution │  Rank Comparison │
│  (Panel A)    │  (Panel B)         │  (Panel C)       │
└────────────────────────────────────────────────────────┘
```

**Key Statistics Shown:**
- Panel A: KS D=0.1097, p=1.95×10⁻⁴
- Panel B: Permutation p<0.0001, n=10,000
- Panel C: Mann-Whitney U=[value], p<0.001

**Purpose:** Detailed visualization of all three requested hypothesis tests

---

## Suggested Figure Captions

### For Manuscript

**Figure 1:**
```
Comprehensive NDS distribution analysis comparing pre-COVID (2017-2020, n=773) 
and post-COVID (2020-2023, n=743) periods. (A) Pre-COVID distribution shows 
mean NDS = 0.000 (SD = 2.014). (B) Post-COVID distribution shows mean NDS = -2.010 
(SD = 4.853). (C) Distribution comparison demonstrates Kolmogorov-Smirnov 
statistic D = 0.1097 (p < 0.001), confirming statistically significant regime 
shift. (D) Q-Q plot shows deviation from reference line, validating distributional change.
```

**Figure 2:**
```
Three statistical hypothesis tests validating post-COVID regime shift significance. 
(A) Kolmogorov-Smirnov test comparing cumulative distribution functions (D = 0.1097, 
p < 0.001). (B) Permutation test with 10,000 iterations (p < 0.0001), showing 
observed difference at 100th percentile of null distribution. (C) Mann-Whitney U 
test comparing rank distributions (p < 0.001). All three independent tests converge 
on highly significant results.
```

---

## How to Regenerate

```bash
cd "c:\Users\krish\New folder\NeuroFininace\NDS-ImprovedModels"
python create_comprehensive_statistical_figure.py
```

**Runtime:** ~15-20 seconds  
**Output:** Both PNG and PDF versions at 300 DPI

---

## In-Text Citations

**When referencing Figure 1:**
- "Distribution analysis revealed significant regime shift (Figure [X])"
- "Pre-COVID (μ=0.000) vs Post-COVID (μ=-2.010) NDS distributions differ significantly (Figure [X]A,B)"
- "Q-Q plot confirms distributional change (Figure [X]D)"

**When referencing Figure 2:**
- "Three independent statistical tests confirmed significance (Figure [X])"
- "Permutation testing ruled out sampling variability (p<0.0001; Figure [X]B)"
- "All hypothesis tests converged on p<0.001 (Figure [X])"

**When referencing both:**
- "Statistical validation (Figures [X] and [X+1]) demonstrates robust evidence for regime shift"
- "Distribution comparison and formal hypothesis testing (Figures [X], [X+1]) confirm p<0.001"

---

## Test Results Summary

| Test | Location | Result | Interpretation |
|------|----------|--------|----------------|
| **Kolmogorov-Smirnov** | Fig 2A | D=0.1097, p<0.001 | Distributions differ |
| **Permutation (10k)** | Fig 2B | p<0.0001 | NOT random chance |
| **Mann-Whitney U** | Fig 2C | p<0.001 | Ranks differ |
| **Distribution Viz** | Fig 1C | KS overlay | Visual confirmation |
| **Q-Q Plot** | Fig 1D | Deviation | Non-linear shift |

---

## Integration Checklist

- [ ] Review both figures for clarity and quality
- [ ] Choose figure numbering in manuscript
- [ ] Insert figures in appropriate sections (likely Results)
- [ ] Write/adapt captions using templates above
- [ ] Add in-text references where discussing statistical validation
- [ ] Ensure figure quality in compiled PDF (300 DPI maintained)
- [ ] Cross-reference with Tables 1 and 2
- [ ] Update response letter with figure numbers
- [ ] Verify all statistical values match between figures, tables, and text

---

## File Sizes (Approximate)

- `nds_statistical_validation_4panel.png`: ~2-3 MB
- `nds_statistical_validation_4panel.pdf`: ~200-300 KB
- `three_statistical_tests.png`: ~2-3 MB  
- `three_statistical_tests.pdf`: ~200-300 KB

All files are suitable for submission and publication.

---

## Color Information

**Pre-COVID:** Steel Blue (#4A7BA7)  
**Post-COVID:** Brick Red (#B85450)

**Accessibility:**
- ✓ High contrast
- ✓ Print-friendly (grayscale compatible)
- ✓ Colorblind-friendly (distinct hues)

---

## Related Documentation

- **Detailed guide:** `Paper/STATISTICAL_FIGURES_DOCUMENTATION.md`
- **Statistical results:** `NDS-ImprovedModels/STATISTICAL_TESTING_RESULTS.md`
- **Complete summary:** `Paper/COMPLETE_REVIEWER_RESPONSE_SUMMARY.md`
- **Generation script:** `NDS-ImprovedModels/create_comprehensive_statistical_figure.py`

---

**Quick Answer:** "Where are the figures?"
→ `NeuroFininace/NDS-ImprovedModels/Publication_Figures/`

**Quick Answer:** "How do I regenerate?"
→ `python create_comprehensive_statistical_figure.py`

**Quick Answer:** "What do they show?"
→ Figure 1: Distribution analysis (4 panels)  
→ Figure 2: Three statistical tests (KS, Permutation, MW-U)

**Quick Answer:** "Are they publication-ready?"
→ Yes! 300 DPI, PNG + PDF, proper formatting
