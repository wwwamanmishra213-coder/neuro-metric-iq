# NEURO-METRIC | Cognitive Assessment & Heuristic Composite Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Chromium](https://img.shields.io/badge/Chromium-100%25%20Compatible-cyan.svg)](https://www.chromium.org)
[![Three.js](https://img.shields.io/badge/3D%20Engine-Three.js%20WebGL-purple.svg)](https://threejs.org)
[![Test Suite](https://img.shields.io/badge/Tests-16%20Passed%20%2F%200%20Failed-emerald.svg)](#test-suite--verification)
[![Scale](https://img.shields.io/badge/Scale-Wechsler%20Ref%20(%CE%BC%3D100%2C%20%CF%83%3D15)-blue.svg)](#)

A browser-based non-verbal cognitive assessment battery and Heuristic Composite Index (HCI) estimation engine wrapped in a futuristic 3D holographic HUD interface. Built with hardware-accelerated WebGL (`Three.js`), dynamic SVG vector induction logic, and grounded in the Cattell–Horn–Carroll (CHC) cognitive framework.

---

## Psychometric Integrity & Audit Overview

The engine underwent a comprehensive code and statistical audit to ensure every reported number is traceable to observed data and defensible mathematical models.

- **Audited Scoring Engine (`scoring-engine.js`):** A standalone, fully deterministic, zero-dependency UMD module that calculates subtest indices, normal distributions, standard errors, and clinical discrepancies.
- **True 95% Confidence Intervals:** Formally verified via $X \pm 1.96 \times \text{SEM}$. For $\text{SEM} = 3.67$ at $X = 112$, the exact $95\%$ margin is $\pm 7.19$ points ($105 - 119$). The previous unverified $\pm 4$ spread ($108 - 116$) represented only a $72.4\%$ interval.
- **General Ability Index (GAI):** In accordance with WAIS-IV neuropsychological guidelines, when core reasoning ($G_f$) diverges from processing speed ($G_s$) by $\ge 20$ points (1.33+ SD), the composite is classified as **non-unitary**. The engine automatically surfaces the GAI (estimating $121$, $91.6$th percentile) to isolate inductive reasoning from motor/device latency.
- **Transparency & Classification:** Avoids unverified clinical claims ("IRT standardized N=10,000", "Official Mensa Qualifying"). Clearly marks scores as `HEURISTIC_COMPOSITE_INDEX` under a theoretical $N(100, 15)$ Gaussian reference model.

Full audit documentation:
- [NEUROMETRIC_AUDIT.md](file:///c:/Users/wwwam/Downloads/how%20to%20calculate%20iq/NEUROMETRIC_AUDIT.md) — Baseline defect inventory and reverse-engineered calculations.
- [NEUROMETRIC_SCORING_SPEC.md](file:///c:/Users/wwwam/Downloads/how%20to%20calculate%20iq/NEUROMETRIC_SCORING_SPEC.md) — Formal scoring specification and data contracts.
- [NEUROMETRIC_VALIDATION_REPORT.md](file:///c:/Users/wwwam/Downloads/how%20to%20calculate%20iq/NEUROMETRIC_VALIDATION_REPORT.md) — Validation report and standardization roadmap.

---

## Subtest Battery

1. **Fluid Matrix Reasoning ($G_f$):** 8 culture-fair Raven's & JCTI-style vector logic puzzles (rotations, XOR boolean logic, and vertex arithmetic).
2. **Spatial Working Memory ($G_{wm}$):** Digital Corsi Block-Tapping task testing dorsolateral prefrontal cortex (dlPFC) retention buffer across spans 4 to 8.
3. **Quantitative Induction ($G_q$):** High-order numerical series synthesis and mathematical pattern deduction.
4. **Symbolic Processing Speed ($G_s$):** 45-second burst discrimination task tracking millisecond reaction latency and throughput.

---

## Test Suite & Verification

The scoring engine includes a comprehensive 16-test automated verification suite covering edge cases, Gaussian monotonicity, exact confidence bounds, clinical discrepancy triggers, and audit case reproduction.

To execute the verification suite:

```bash
node test_scoring_engine.js
```

### Test Summary:
```
=============================================================
RUNNING NEUROMETRIC SCORING ENGINE AUDIT & VERIFICATION TESTS
Engine Version: 3.1.0-audited
=============================================================

GROUP 1: Mathematical & Statistical Foundations (6 tests) -> ALL PASS
GROUP 2: Normal Distribution & Percentile Properties (4 tests) -> ALL PASS
GROUP 3: Uncertainty & Confidence Intervals (2 tests) -> ALL PASS
GROUP 4: Subtests, Composite & Clinical Discrepancy (4 tests) -> ALL PASS

=============================================================
TEST SUMMARY: 16 PASSED, 0 FAILED (TOTAL: 16)
=============================================================
```

---

## Quick Start

### 1. Native Desktop Mode (Windows)
Double-click:
```cmd
Run_IQ_Test.bat
```
*Auto-detects Google Chrome or Microsoft Edge and launches the engine as a standalone borderless desktop app (`--app=file:///...`).*

### 2. PowerShell
```powershell
powershell -ExecutionPolicy Bypass -File .\Run_IQ_Test.ps1
```

### 3. Direct Browser
Open `index.html` directly in any modern Chromium browser (Chrome, Edge, Brave, Opera).

---

## Keyboard Shortcuts

- **Matrix & Math Subtests:** Keys `[1]` to `[6]` to select options, `[Enter]` to confirm & advance.
- **Processing Speed:** Key `[Y]` for Present, `[N]` for Absent.

---

## Scientific & Psychometric Disclaimer

NeuroMetric is an experimental research and educational cognitive assessment tool. While its mathematical conversions, Gaussian error functions, and clinical discrepancy detection follow established neuropsychological guidelines (e.g. WAIS-IV GAI derivation and Abramowitz & Stegun normal approximations), scores are derived from heuristic calibrations and theoretical distributions rather than a clinically normed standardization sample ($N=10,000$). These results do not constitute medical, psychiatric, or official neuropsychological diagnosis.

---

## License

MIT License. Designed for authorized neurocognitive research and educational assessment.
