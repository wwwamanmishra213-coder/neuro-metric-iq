# ARCANE WILLOW CODEX
### HTML Visual Prototype + Production-Ready ReportLab PDF Design System

An academic editorial design system fusing ancient fantasy manuscript aesthetics with modern scientific rigor. Designed for scholarly treatises, celestial mechanics, and neuropsychometric dossiers.

---

## 1. Design Philosophy & Aesthetic Foundation

- **Living Golden Willow Branches:** Organic vector willow tendrils cascading from the four corners, with pointed lanceolate leaves, delicate central veins, and luminous gold energy nodes.
- **Obsidian & Antique Gold Metallurgy:** Black obsidian foundations (`#0B0A0C`) with antique gold (`#C6A15B`), bright metallic gold (`#E8CB83`), deep bronze (`#72512D`), and warm parchment (`#E9E0CC`).
- **Rigorous Mathematical & Scientific Typesetting:** True mathematical equations ($F = G m_1 m_2 / r^2$, $v = \sqrt{GM/r}$), unit definitions, coordinate embedding grids, and vector celestial diagrams.
- **Separation of Concerns:** 
  - **HTML/CSS Prototype:** The visual design laboratory.
  - **ReportLab Python Engine:** The production publishing engine (searchable, selectable vector PDF).

---

## 2. Directory Structure

```
arcane-willow-codex/
├── index.html                   # Interactive HTML/CSS A4 visual prototype
├── styles.css                   # Editorial academic styling & print rules
├── assets/
│   ├── willow-frame.svg         # Double gold border, willow tendrils, central crest
│   ├── orbital-diagram.svg      # Keplerian orbital mechanics vector diagram
│   └── spacetime-diagram.svg    # General relativistic metric curvature diagram
├── pdf/
│   ├── design_config.py         # Shared design tokens, color palette, dimensions
│   └── generate_pdf.py          # ReportLab vector PDF compiler (searchable text)
├── output/
│   └── sample-codex.pdf         # Production A4 PDF output (100% vector & selectable)
└── README.md                    # Documentation & runbook
```

---

## 3. How to Preview and Run

### A. Preview the HTML Prototype
Simply open `arcane-willow-codex/index.html` in any modern web browser:
```bash
# Windows
start arcane-willow-codex/index.html
```
- Inspect the A4 canvas at normal zoom.
- Click **"Print / Export PDF"** to view standard browser print layout (`@page { size: A4 portrait; margin: 0; }`).
- Click **"✦ Bio-Telemetry Sync (Cam/Mic)"** to trigger the patient consent bio-telemetry modal.

### B. Generate / Recompile the Production PDF
Run the Python ReportLab generation script:
```bash
python arcane-willow-codex/pdf/generate_pdf.py
```
Output will be generated at `arcane-willow-codex/output/sample-codex.pdf`.

---

## 4. Patient Consent Camera & Microphone Add-on

As requested, the prototype includes a **Patient Bio-Telemetry Add-on**:
- **Informed Consent Gatekeeper:** Sensors remain completely offline until explicit patient consent is granted.
- **Real-Time Optical Gaze Viewport:** Hardware-accelerated camera stream framed by cybernetic targeting reticles.
- **Acoustic Stress Frequency Spectrogram:** Real-time fast-Fourier transform (FFT) visualizer rendered via Web Audio API (`AudioContext`, `AnalyserNode`).
- **Privacy Guarantee:** All processing remains strictly local within the client session; no external transmission or server storage.
- **Revocability:** Consent can be revoked with one click at any time, instantly closing device tracks.

---

## 5. Quality Assurance & Verification Summary

| Component | Tested Criteria | Result |
| :--- | :--- | :--- |
| **A4 Dimensions** | $210\,\text{mm} \times 297\,\text{mm}$ ($595.28 \times 841.89\,\text{pt}$) | **PASSED** (Exact standard) |
| **Selectable Text** | Full extraction of headers, prose, and formulas via `pypdf` | **PASSED** (100% searchable) |
| **Vector Fidelity** | Willow frame, corner nodes, and diagrams rendered as pure vector paths | **PASSED** (Infinite resolution) |
| **Safe Margins** | Text layout bounded by 22mm safe margin; zero leaf collision | **PASSED** |
| **Diagram 1** | Keplerian orbital mechanics with $\vec{v}$, $\vec{F}_g$, and $M$ focus | **PASSED** |
| **Diagram 2** | Relativistic spacetime funnel with photon geodesic deflection | **PASSED** |
| **Bio-Telemetry** | Interactive consent modal with camera & mic hooks | **PASSED** |
