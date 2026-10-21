# NEUROMETRIC ENGINE: INITIAL AUDIT & MATHEMATICAL INSPECTION REPORT
**Document Version:** 1.0.0  
**Audit Date:** 2026-10-21  
**Auditors:** Senior Software Engineer, Psychometrician, Cognitive Science Researcher, Statistical Auditor  
**Status:** COMPLETE — BASELINE AUDIT

---

## 1. Executive Summary

This baseline audit investigates the **NeuroMetric** codebase located in `c:\Users\wwwam\Downloads\how to calculate iq`. The system is implemented as a single-page HTML5/WebGL application (`index.html`) with Windows batch and PowerShell desktop launchers (`Run_IQ_Test.bat`, `Run_IQ_Test.ps1`).

While the application features an engaging 3D visual presentation (Three.js WebGL and hardware-accelerated video) and functional interactive tasks (Matrix Reasoning, Corsi Block-Tapping, Number Series, and Symbol Search), **the scoring and reporting layer contains critical psychometric, statistical, and architectural defects**. Specifically, claims of "IRT standardization," a "10,000+ norming sample," and "Clinical FSIQ" were cosmetic assertions with zero empirical backing in the codebase. Furthermore, ad-hoc formulas, hardcoded confidence interval margins, and contradictory narrative descriptions undermine the scientific defensibility of the output.

---

## 2. Project Architecture & Codebase Inventory

| File Path | Purpose | Language / Tech | Audit Status |
| :--- | :--- | :--- | :--- |
| `index.html` | Core Web Application & Embedded Scoring Logic | HTML5, CSS3, Tailwind (CDN), Three.js r128, Vanilla JS | Inspected (Defects identified) |
| `Run_IQ_Test.bat` | Native Chromium App Launcher for Windows CMD | Windows Batch (`.bat`) | Functional |
| `Run_IQ_Test.ps1` | Native Chromium App Launcher for PowerShell | PowerShell (`.ps1`) | Functional |
| `background.mp4` | Looping 3D Cosmos Video Asset (~9 MB) | H.264 / MP4 Video | Verified |
| `preview.html` | Static 2D Prototype | HTML5 / CSS | Legacy reference |
| `preview_3d.html` | Standalone 3D WebGL Prototype | Three.js WebGL / HTML5 | Functional prototype |
| `README.md` | Project Documentation | Markdown | Requires updates to remove unverified claims |

---

## 3. Data Flow Tracing (User Input to Final Score)

```
[User Action]
     │
     ├── Subtest 1: Fluid Matrix (Gf) ────────► gfRaw (count correct out of 8)
     ├── Subtest 2: Corsi Block Span (Gwm) ───► gwmSpan (max sequence) + trialsSuccess * 0.2
     ├── Subtest 3: Quantitative (Gq) ────────► gqRaw (count correct out of 6)
     └── Subtest 4: Processing Speed (Gs) ────► netSpeedScore = gsCorrect - (gsIncorrect * 0.5)
                                                     │
                                                     ▼
                                      [Arbitrary Z-Transformation]
                                       zGf  = (gfRaw - 4.2) / 1.8
                                       zGwm = (gwmScore - 5.5) / 1.2
                                       zGq  = (gqRaw - 3.1) / 1.5
                                       zGs  = (netSpeed - 12.0) / 4.0
                                                     │
                                                     ▼
                                     [Subtest Standardized Scores]
                                       Score_i = round(100 + 15 * z_i)
                                                     │
                                                     ▼
                                      [Composite FSIQ Calculation]
                   compositeZ = 0.35*zGf + 0.25*zGwm + 0.25*zGq + 0.15*zGs
                   fsiqZ = compositeZ * 1.18  <-- [UNDOCUMENTED AD-HOC MULTIPLIER]
                   finalFSIQ = round(100 + 15 * fsiqZ)
                                                     │
                                                     ▼
                                     [Mathematical Percentile via erf]
                                       Percentile = 100 * Φ((finalFSIQ - 100) / 15)
                                                     │
                                                     ▼
                                         [Hardcoded Confidence Band]
                                         CI = finalFSIQ ± 4  <-- [MATHEMATICALLY DEFECTIVE]
```

---

## 4. Mathematical & Psychometric Audit of Existing Report Claims

The existing report issued for a test session produced:
* **FSIQ:** `112`
* **Percentile:** `78.8%`
* **Confidence Interval:** `108–116`
* **Reported SEM:** `~ 3.67 IQ points`
* **Sub-indices:** $G_f = 123, G_{wm} = 114, G_q = 109, G_s = 78$
* **Claimed Norm Sample:** `10,000+ IRT Standardized Participants`

### A. Percentile Verification
* Formula: $z = \frac{X - \mu}{\sigma} = \frac{112 - 100}{15} = \frac{12}{15} = +0.8000$
* Theoretical standard normal cumulative distribution:
  $$\Phi(0.80) = \frac{1}{2}\left[1 + \text{erf}\left(\frac{0.80}{\sqrt{2}}\right)\right] \approx 0.7881446 \Rightarrow \mathbf{78.81\%}$$
* **Finding:** The numerical percentile `78.8%` is **mathematically consistent** with a Gaussian distribution $N(100, 15)$. However, **it is purely a theoretical transformation of an unvalidated score**, not an empirical percentile from a normed cohort.

### B. Composite-Score Calculation Verification
* Simple arithmetic mean of factor scores:
  $$\bar{X} = \frac{123 + 114 + 109 + 78}{4} = \frac{424}{4} = \mathbf{106.0}$$
* Actual implementation formula in `index.html` (lines 1696–1699):
  ```javascript
  const compositeZ = (0.35 * zGf) + (0.25 * zGwm) + (0.25 * zGq) + (0.15 * zGs);
  const compositeInflationCorrection = 1.18;
  const fsiqZ = compositeZ * compositeInflationCorrection;
  let finalFSIQ = Math.round(100 + 15 * fsiqZ);
  ```
  Substituting user z-scores:
  * $z_{Gf} = (7 - 4.2) / 1.8 = 1.5556 \Rightarrow \text{Score} = 123$
  * $z_{Gwm} = (6.6 - 5.5) / 1.2 = 0.9167 \Rightarrow \text{Score} = 114$
  * $z_{Gq} = (4 - 3.1) / 1.5 = 0.6000 \Rightarrow \text{Score} = 109$
  * $z_{Gs} = (6.0 - 12) / 4.0 = -1.5000 \Rightarrow \text{Score} = 78$
  * $\text{compositeZ} = 0.35(1.5556) + 0.25(0.9167) + 0.25(0.6000) + 0.15(-1.5000) = 0.5444 + 0.2292 + 0.1500 - 0.2250 = 0.6986$
  * Applying multiplier $1.18$: $fsiqZ = 0.6986 \times 1.18 = 0.8243$
  * $FSIQ = \text{round}(100 + 15 \times 0.8243) = \text{round}(112.36) = \mathbf{112}$.
* **Finding:** The composite score is reproducible from the source code, but relies on an **ad-hoc inflation multiplier of 1.18** with no statistical derivation or empirical covariance matrix. In psychometrics, composites must be scaled based on the variance of the sum of correlated variables:
  $$\sigma_{\text{composite}}^2 = \sum w_i^2 \sigma_i^2 + 2\sum_{i < j} w_i w_j \text{Cov}(i, j)$$
  Without an empirical covariance matrix, the multiplier `1.18` is arbitrary. **Status: UNVERIFIED CUSTOM COMPOSITE.**

### C. Confidence Interval and SEM Verification
* Conventional 95% Confidence Interval formula:
  $$\text{CI}_{95\%} = X \pm 1.96 \times \text{SEM}$$
* Using stated SEM $= 3.67$:
  $$\text{Margin} = 1.96 \times 3.67 = 7.1932 \text{ IQ points}$$
  $$\text{Expected } \text{CI}_{95\%} = [112 - 7.19, 112 + 7.19] = [104.81, 119.19] \Rightarrow \mathbf{105 - 119}$$
* Actual code in `index.html` (line 1725):
  ```javascript
  document.getElementById('reportConfInterval').textContent = `${finalFSIQ - 4} — ${finalFSIQ + 4}`;
  ```
* **Finding:** The reported interval `108–116` was generated by a hardcoded margin of $\pm 4$ points, **not** by the $1.96 \times \text{SEM}$ formula. A margin of $\pm 4$ with SEM $= 3.67$ corresponds to $z = 4 / 3.67 = 1.09$, which is approximately a **72% confidence interval**, NOT a 95% interval! Presenting this as a 95% CI is a statistical error. **Status: DEFECTIVE.**

### D. Internal Consistency & Claim Verification
1. **Fabricated Norm Sample:** The document headers claimed `N = 10,000+ IRT Standardized Participants`. No IRT parameters ($a, b, c$), response matrices, calibration logs, or norm tables exist anywhere in the repository.
2. **Missing Latency Telemetry:** Line 1728 attempted to populate `telemetryMeanLatency`, but if no items were completed or during partial runs, the UI retained placeholder dashes (`--`).
3. **Clinical Overreach:** Calling the score "Full Scale IQ (FSIQ)" and invoking "Mensa Cutoff: ≥ 130" creates a false impression of clinical validity for an unproctored, unvalidated web screener.

---

## 5. Summary of Defect Classifications

| Component | Nature of Defect | Severity | Remediation Plan |
| :--- | :--- | :--- | :--- |
| Composite Calculation | Ad-hoc $1.18$ inflation factor without covariance documentation | HIGH | Modularize, document formula as an unvalidated heuristic composite, or report unweighted mean index. |
| Confidence Interval | Hardcoded $\pm 4$ points labeled as 95% CI with SEM 3.67 | CRITICAL | Calculate true interval $X \pm 1.96 \times \text{SEM}$ dynamically or label as unverified. |
| Empirical Norm Claims | "N=10,000+ IRT Norms" claim in UI and PDF | CRITICAL | Replace with explicit "Unstandardized Screener / Theoretical Reference Only" badges. |
| Modular Separation | UI logic, state, graphics, and scoring mixed in one monolithic HTML file | MEDIUM | Extract scoring engine into standalone, unit-tested module (`scoring-engine.js`). |
| Missing Response Handling | Division by zero or NaN risk if subtest is aborted | MEDIUM | Implement defensive contracts for missing, zero, and partial responses. |

---

## 6. Audit Conclusion

The NeuroMetric web application functions smoothly as an interactive multimedia screener, but its psychometric claims were overstated. Phase 3–9 will implement a transparent, modular, unit-tested scoring contract that reports raw metrics truthfully, calculates statistical formulas rigorously, and clearly communicates the boundaries between observed data and theoretical models.
