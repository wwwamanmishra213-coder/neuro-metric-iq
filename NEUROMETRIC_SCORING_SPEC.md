# NEUROMETRIC SCORING SPECIFICATION & STATISTICAL CONTRACT
**Document Version:** 1.0.0  
**Status:** ACTIVE SPECIFICATION  
**Scope:** Architecture, Formulations, Mathematical Assumptions, and Validation Guardrails

---

## 1. Architectural Principles

The NeuroMetric scoring engine enforces strict separation of concerns across 9 conceptual layers:

```
[Layer 1: Observed Events] ──────► Keypresses, timestamps, raw choices, coordinates
          │
[Layer 2: Raw Domain Metrics] ───► Items attempted, correct counts, error counts, span lengths
          │
[Layer 3: Performance Indices] ──► Accuracies (%), items/min, throughput, response-time median/SD
          │
[Layer 4: Heuristic Scaling] ────► Calibrated linear z-scores (clearly labeled UNSTANDARDIZED)
          │
[Layer 5: Composite Synthesis] ──► Weighted General Ability Index & Heuristic Composite
          │
[Layer 6: Theoretical CDF] ──────► Gauss error function mapping against N(100, 15)
          │
[Layer 7: Uncertainty & SEM] ────► Conventional 95% CI (X ± 1.96 * SEM) with method provenance
          │
[Layer 8: Evidence-Based Report] ► Objective descriptive findings without clinical overreach
          │
[Layer 9: Provenance Metadata] ──► Validation status, sample provenance, software version
```

---

## 2. Domain Scoring Specifications

### Domain 1: Fluid Reasoning ($G_f$)
* **Task Description:** Raven's-style $3 \times 3$ vector matrix pattern induction with 6 multiple-choice alternatives.
* **Items:** $K = 8$ items.
* **Recorded Inputs:**
  * `item_id`: Integer ($1 \le i \le 8$)
  * `user_choice`: Integer ($1 \le c \le 6$) or `null` if unattempted
  * `is_correct`: Boolean
  * `latency_ms`: Float (response time in milliseconds)
* **Raw Outputs:**
  * `items_attempted`: $\sum_{i=1}^K \mathbb{I}(\text{user\_choice}_i \neq \text{null})$
  * `items_correct`: $\sum_{i=1}^K \mathbb{I}(\text{is\_correct}_i = \text{true})$
  * `accuracy_pct`: $\frac{\text{items\_correct}}{\text{items\_attempted}} \times 100$ (if attempted $> 0$; else `null`)
  * `mean_latency_sec`: Mean of valid item latencies in seconds
* **Unstandardized Heuristic Index Formula:**
  $$z_{Gf} = \frac{\text{items\_correct} - \mu_{Gf}}{\sigma_{Gf}} = \frac{\text{items\_correct} - 4.2}{1.8}$$
  $$\text{Index}_{Gf} = \text{clamp}(100 + 15 \times z_{Gf}, 55, 145)$$
* **Validation Status:** `RAW_PERFORMANCE_VERIFIED | HEURISTIC_UNSTANDARDIZED`

---

### Domain 2: Visuospatial Working Memory ($G_{wm}$)
* **Task Description:** Digital Corsi Block-Tapping task. Sequence of glowing grid blocks flashed at 850ms cadence; forward exact-order recall.
* **Trials:** Up to 5 adaptive trials starting at span 4 up to span 8.
* **Recorded Inputs:**
  * `trial_id`: Integer ($1 \le t \le 5$)
  * `sequence_length`: Integer ($4 \le L \le 8$)
  * `target_sequence`: Array of block indices
  * `user_sequence`: Array of selected block indices
  * `exact_match`: Boolean ($\text{target\_sequence} = \text{user\_sequence}$)
* **Raw Outputs:**
  * `max_span_completed`: Longest sequence length achieved with exact match ($4 \le L \le 8$, or $0$ if none)
  * `trials_attempted`: Integer ($0 \le N \le 5$)
  * `trials_passed`: Count of exact match successes
* **Unstandardized Heuristic Index Formula:**
  $$\text{SpanScore} = \text{max\_span\_completed} + (0.2 \times \text{trials\_passed})$$
  $$z_{Gwm} = \frac{\text{SpanScore} - 5.5}{1.2}$$
  $$\text{Index}_{Gwm} = \text{clamp}(100 + 15 \times z_{Gwm}, 55, 145)$$
* **Validation Status:** `RAW_PERFORMANCE_VERIFIED | HEURISTIC_UNSTANDARDIZED`

---

### Domain 3: Quantitative Induction ($G_q$)
* **Task Description:** Mathematical pattern induction and numerical sequence extrapolation.
* **Items:** $K = 6$ items (arithmetic, quadratic, prime power, recursive, factorial, digit sum).
* **Recorded Inputs:**
  * `item_id`: Integer ($1 \le i \le 6$)
  * `user_choice`: Selected value or option ID
  * `is_correct`: Boolean
  * `latency_ms`: Response time in milliseconds
* **Raw Outputs:**
  * `items_attempted`: Count of attempted items
  * `items_correct`: Count of correct items
  * `accuracy_pct`: $\frac{\text{items\_correct}}{\text{items\_attempted}} \times 100$
* **Unstandardized Heuristic Index Formula:**
  $$z_{Gq} = \frac{\text{items\_correct} - \mu_{Gq}}{\sigma_{Gq}} = \frac{\text{items\_correct} - 3.1}{1.5}$$
  $$\text{Index}_{Gq} = \text{clamp}(100 + 15 \times z_{Gq}, 55, 145)$$
* **Validation Status:** `RAW_PERFORMANCE_VERIFIED | HEURISTIC_UNSTANDARDIZED`

---

### Domain 4: Symbolic Processing Speed ($G_s$)
* **Task Description:** 45-second rapid visual discrimination; detect whether target glyph exists inside search array of 6 symbols.
* **Duration:** Exact 45.0 seconds timed window.
* **Recorded Inputs:**
  * Individual trial records: target, search array, target presence (`bool`), user decision (`bool`), trial latency (`ms`).
* **Raw Outputs:**
  * `trials_attempted`: Total trials executed within time window
  * `trials_correct`: Total accurate classifications
  * `trials_incorrect`: False positives + false negatives
  * `throughput_per_minute`: $\frac{\text{trials\_correct}}{\text{elapsed\_seconds}} \times 60$
  * `median_latency_ms`: Median reaction time on valid trials
  * `accuracy_pct`: $\frac{\text{trials\_correct}}{\text{trials\_attempted}} \times 100$
* **Unstandardized Heuristic Index Formula:**
  $$\text{NetSpeed} = \max(0, \text{trials\_correct} - 0.5 \times \text{trials\_incorrect})$$
  $$z_{Gs} = \frac{\text{NetSpeed} - 12.0}{4.0}$$
  $$\text{Index}_{Gs} = \text{clamp}(100 + 15 \times z_{Gs}, 55, 145)$$
* **Validation Status:** `RAW_PERFORMANCE_VERIFIED | HEURISTIC_UNSTANDARDIZED`

---

## 3. Composite Calculation & Discrepancy Analysis

### A. Heuristic Composite Index (HCI)
To prevent misleading users with an unverified "Clinical Full Scale IQ," the overall score is formally designated as the **Heuristic Composite Index (HCI)**.
$$z_{\text{composite}} = 0.35 z_{Gf} + 0.25 z_{Gwm} + 0.25 z_{Gq} + 0.15 z_{Gs}$$
$$\text{HCI} = \text{clamp}(\text{round}(100 + 15 \times [z_{\text{composite}} \times 1.18]), 55, 145)$$

### B. General Ability Index (GAI) Trigger
Clinical neuropsychology (WAIS-IV / WISC-V guidelines) requires calculating the General Ability Index when a significant discrepancy exists between core reasoning and working memory or processing speed:
* **Trigger Condition:** $|\text{Index}_{Gf} - \text{Index}_{Gs}| \ge 20 \text{ points}$
* **GAI Formula:**
  $$z_{\text{GAI}} = \frac{0.60 z_{Gf} + 0.40 z_{Gq}}{0.85}$$
  $$\text{GAI} = \text{clamp}(\text{round}(100 + 15 \times z_{\text{GAI}}), 55, 145)$$
* **Clinical Note:** The GAI reflects higher-order reasoning potential free of visual scanning or motor keyboard latency constraints.

---

## 4. Normal Curve & Uncertainty Engine

### A. Theoretical Cumulative Normal Percentile
$$\text{Percentile} = 100 \times \Phi\left(\frac{X - 100}{15}\right) = \frac{100}{2}\left[1 + \text{erf}\left(\frac{X - 100}{15\sqrt{2}}\right)\right]$$
* **Approximation Used:** Abramowitz & Stegun formula 7.1.26 with absolute error $< 1.5 \times 10^{-7}$.
* **Labeling Requirement:** Must explicitly display: `"Theoretical percentile under normal distribution N(100, 15); not an empirical population norm."`

### B. Confidence Interval & SEM Contract
* Formula: $\text{CI}_{95\%} = X \pm 1.96 \times \text{SEM}$
* **Constraint:** If an empirical reliability coefficient $r_{xx}$ is unverified, the SEM must be documented as `SEM_THEORETICAL = 3.67` (assuming $r_{xx} = 0.94$).
* **Calculation:**
  $$\text{Margin}_{95\%} = \text{round}(1.96 \times 3.67) = \text{round}(7.19) = 7 \text{ points}$$
  $$\text{CI}_{95\%} = [X - 7, X + 7]$$
* **Prohibition:** Hardcoding arbitrary intervals (such as $\pm 4$) while claiming 95% confidence is strictly forbidden.

---

## 5. Machine-Readable Output Contract (JSON Schema)

```json
{
  "assessment_id": "string (UUID)",
  "assessment_version": "3.1.0-audited",
  "assessment_timestamp": "string (ISO-8601 UTC)",
  "status": "completed | incomplete | invalid",
  "completion_summary": {
    "subtests_total": 4,
    "subtests_completed": "integer (0-4)",
    "total_elapsed_seconds": "number"
  },
  "domains": {
    "Gf": {
      "name": "Fluid Matrix Reasoning",
      "items_attempted": "integer",
      "items_correct": "integer",
      "accuracy_pct": "number | null",
      "raw_score": "integer",
      "heuristic_index": "integer",
      "theoretical_percentile": "number",
      "mean_latency_sec": "number | null",
      "validation_status": "RAW_PERFORMANCE_VERIFIED | HEURISTIC_UNSTANDARDIZED"
    },
    "Gwm": {
      "name": "Spatial Working Memory",
      "max_span_completed": "integer",
      "trials_attempted": "integer",
      "trials_passed": "integer",
      "heuristic_index": "integer",
      "theoretical_percentile": "number",
      "validation_status": "RAW_PERFORMANCE_VERIFIED | HEURISTIC_UNSTANDARDIZED"
    },
    "Gq": {
      "name": "Quantitative Induction",
      "items_attempted": "integer",
      "items_correct": "integer",
      "accuracy_pct": "number | null",
      "heuristic_index": "integer",
      "theoretical_percentile": "number",
      "validation_status": "RAW_PERFORMANCE_VERIFIED | HEURISTIC_UNSTANDARDIZED"
    },
    "Gs": {
      "name": "Processing Speed",
      "trials_attempted": "integer",
      "trials_correct": "integer",
      "trials_incorrect": "integer",
      "throughput_per_minute": "number",
      "median_latency_ms": "number | null",
      "heuristic_index": "integer",
      "theoretical_percentile": "number",
      "validation_status": "RAW_PERFORMANCE_VERIFIED | HEURISTIC_UNSTANDARDIZED"
    }
  },
  "composite": {
    "value": "integer",
    "score_type": "HEURISTIC_COMPOSITE_INDEX",
    "theoretical_percentile": "number",
    "formula_version": "CHC-Heuristic-v3.1",
    "validation_status": "UNVALIDATED_CUSTOM_INDEX",
    "classification": "string"
  },
  "discrepancy_analysis": {
    "detected": "boolean",
    "point_difference": "integer",
    "gai_value": "integer | null",
    "gai_theoretical_percentile": "number | null",
    "clinical_note": "string | null"
  },
  "uncertainty": {
    "sem": 3.67,
    "confidence_level": "95%",
    "margin_of_error": 7,
    "confidence_interval": [ "integer", "integer" ],
    "method": "Conventional-Normal-Approximation (1.96 * SEM)",
    "validation_status": "THEORETICAL_ESTIMATE"
  },
  "norm_reference": {
    "dataset_id": null,
    "sample_size": null,
    "population_description": null,
    "validation_status": "NO_CLINICAL_NORMS_ATTACHED"
  }
}
```
