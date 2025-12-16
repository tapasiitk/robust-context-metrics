# Attraction Effect Metrics: Identifying Measurement Vulnerabilities

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Paper](https://img.shields.io/badge/arXiv-Preprint-red.svg)](./paper/Rath_et_al_Context_Effects_Metrics.pdf)

**Authors:** Tapas Ranjan Rath, Nisheeth Srivastava, Narayanan Srinivasan  
**Affiliation:** Cognitive Science, Indian Institute of Technology Kanpur

---

## Abstract

This repository contains source code, simulations, and analysis supporting the research on context effects and decision-making metrics. The work analyzes the mathematical and empirical properties of widely used metrics (RST, ΔP, AST, ASC) for measuring the attraction effect—a decision-making bias where introducing an inferior option increases the preference for a competing option.

**Main findings:**
- Standard triplet-triplet metrics exhibit systematic vulnerabilities to false alarms and misses when baseline choice preferences are asymmetric
- Mathematical proofs demonstrate that RST and ΔP generate false positives under heterogeneous preference structures
- Agent-based simulations show that AST and ASC fail to detect opposing decoy effects across contexts
- Recommendations include baseline symmetry checks and pair-triplet experimental designs

---

## Table of Contents

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Key Metrics Analyzed](#key-metrics-analyzed)
- [Methodology](#methodology)
- [Results](#results)
- [Citation](#citation)
- [Contact](#contact)

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/tapasiitk/attraction-effect-metrics.git
cd attraction-effect-metrics

# Install dependencies
pip install -r requirements.txt

# Run notebooks in Jupyter
jupyter notebook notebooks/
```

---

## Project Structure

```
attraction-effect-metrics/
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── paper/
│   └── Rath_et_al_Context_Effects_Metrics.pdf
├── notebooks/
│   ├── 01_metric_misses_opposing_effects.ipynb
│   ├── 02_baseline_choice_bias.ipynb
│   ├── 03_rst_parameter_exploration.ipynb
│   └── 04_softmax_model_validation.ipynb
└── scripts/
    └── 05_heatmap_miss_rates_simulation.py

```

### Directory Descriptions

- **`paper/`** - Contains the full manuscript PDF with theoretical development and detailed results
- **`notebooks/`** - Jupyter notebooks with reproducible code and visualizations
  - Each notebook is self-contained and reproduces specific figures from the paper
  - Notebooks are numbered for sequential understanding of the analysis


---

## Installation

### Requirements

- Python 3.8 or higher
- pip or conda

### Setup

```bash
# Clone the repository
git clone https://github.com/tapasiitk/attraction-effect-metrics.git
cd attraction-effect-metrics

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook
```

### Dependencies

- **numpy** - Numerical computing
- **pandas** - Data manipulation and analysis
- **matplotlib** - Plotting and visualization
- **seaborn** - Statistical data visualization
- **scipy** - Scientific computing
- **jupyter** - Interactive notebooks

---

## Contents

### Notebooks

Each notebook reproduces specific analyses and figures from the paper:

| Notebook | Purpose | Figure(s) |
|----------|---------|-----------|
| `01_metric_misses_opposing_effects.ipynb` | AST/ASC metric failures under opposing decoy effects | Fig 7 |
| `02_baseline_choice_bias.ipynb` | Baseline choice shares across heterogeneous SICs | Fig 4 |
| `03_rst_parameter_exploration.ipynb` | RST false alarm rates across parameter space | Fig 2, 5 |
| `04_softmax_model_validation.ipynb` | Validation of softmax choice model | Appendix A |

### Code

- **`src/plotting_utils.py`** - Helper functions for:
  - Heatmap generation across parameter spaces
  - SIC (Subjective Indifference Curve) visualization
  - Metric comparison plots

---

## Key Metrics Analyzed

| Metric | Context | Reference Value | Vulnerability |
|--------|---------|-----------------|----------------|
| ΔP_target | Pair-Triplet | 0.0 | False alarms under baseline bias |
| RST | Triplet-Triplet | 0.5 | False positives when preference ratios ≠ 1 |
| RST_ew | Triplet-Triplet | 0.5 | Misses opposing effects |
| AST | Triplet-Triplet | 0.5 | Masks violations of regularity |
| ASC | Triplet-Triplet | 0.5 | Cancels opposing decoy effects |

---

## Methodology

### Mathematical Analysis

- **Section 4.1:** Formal proofs of RST false alarm conditions
- **Section 4.2:** Analysis of metric cancellation under opposing effects
- **Derivations:** Vulnerability conditions expressed as functions of baseline preference structures

### Simulation Framework

#### Agent-Based Modeling
- Agents characterized by heterogeneous **Subjective Indifference Curves (SICs)**
- Each agent has a unique linear indifference curve with varying slope
- No inter-agent interactions; focus on individual heterogeneity

#### Choice Model
- **Temperature-scaled softmax function** with parameters:
  - Input: Signed perpendicular distances from SIC to each item
  - β parameter: Controls temperature (β=1 for IIA-compliance; β=4.5 for violations)
  - N: Choice set size (2 for binary, 3 for triplet)

#### Parameter Space Exploration
- **SIC slopes:** Varied 0.5–2.0 to capture heterogeneous preferences
- **Baseline biases:** Systematically manipulated to study robustness
- **Decoy types:** Range decoys (maximum context effect conditions)

#### Tested Conditions

| Model | Behavior | Temperature (β) | Purpose |
|-------|----------|-----------------|---------|
| Model 1: IIA-Adherent | Complies with regularity & IIA | 1.0 | Detect false alarms |
| Model 2: IIA-Violating | Violates regularity with opposing effects | 4.5 | Detect misses |

---

## Results

### False Alarms (Figures 2, 5)

**Finding:** RST deviates from null value (0.5) even under IIA compliance
- Occurs in >80% of parameter space when baseline preference ratios ≠ 1
- Indicates metric sensitivity to prior biases, not genuine context effects
- **Implication:** Researchers may incorrectly conclude attraction effects exist

### Misses (Figure 7)

**Finding:** AST and ASC fail to detect genuine context effects
- When decoys in Context 1 and Context 2 produce opposing effects (ΔA > 0, ΔB < 0)
- Metrics approach null value despite clear regularity violations
- **Implication:** Genuine effects are masked by averaging across contexts

### Opposing Effects Masking (Figure 3)

**Mathematical result:** When ΔA = −ΔB, metrics cancel both effects:

```
AST − 0.5 = (ΔA + ΔB) / 2 ≈ 0
```

This demonstrates systematic underestimation when decoys exert asymmetric influences.

---

## Recommendations

1. **Include pair-triplet baselines** whenever possible in triplet-triplet designs
   - Provides direct comparison against regularity violation benchmark
   - Reduces confounding from baseline asymmetries

2. **Verify baseline symmetry** of choice shares before interpreting metrics
   - Check that P(A | {A,B}) ≈ P(B | {A,B}) ≈ 0.5
   - Document any deviations and account for them in analysis

3. **Report individual-level effects** alongside aggregate metrics
   - Enables detection of heterogeneity in SIC structures
   - Reveals whether averaging masks opposing effects



## Citation

If you use this code or methodology, please cite:

```bibtex
@article{Rath2025,
  title={Unmasking the Flaws of Triplet-Triplet Attraction Effect Measures: 
         Via Mathematical Analysis and Agent-Based Simulations},
  author={Rath, Tapas Ranjan and Srivastava, Nisheeth and Srinivasan, Narayanan},
  year={2025},
  journal={In preparation}
}
```

---

## License

This repository is provided under the MIT License. See [LICENSE](LICENSE) file for details.

---

## Contact

**Tapas Ranjan Rath**  
Indian Institute of Technology Kanpur  
Department of Cognitive Science  
Email: tapasr@iitk.ac.in  
Website: [https://www.cgs.iitk.ac.in/user/tapasr/](https://www.cgs.iitk.ac.in/user/tapasr/)

