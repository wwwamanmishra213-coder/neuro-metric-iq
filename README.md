# NEURO-METRIC | 3D Holographic Cognitive & IQ Assessment Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Chromium](https://img.shields.io/badge/Chromium-100%25%20Compatible-cyan.svg)](https://www.chromium.org)
[![Three.js](https://img.shields.io/badge/3D%20Engine-Three.js%20WebGL-purple.svg)](https://threejs.org)
[![Norms](https://img.shields.io/badge/Scale-Wechsler%20(%CE%BC%3D100%2C%20%CF%83%3D15)-emerald.svg)](#)

A clinical-grade, non-verbal cognitive assessment battery and Full-Scale IQ (FSIQ) estimation engine wrapped in a futuristic 3D holographic HUD interface. Built with hardware-accelerated WebGL (`Three.js`), dynamic SVG vector induction logic, and grounded in the Cattell–Horn–Carroll (CHC) cognitive architecture.

---

## Key Features

- **3D Holographic Spatial HUD:**
  - Hardware-accelerated Three.js WebGL canvas with interactive mouse-responsive neural particle core and starfield.
  - Ambient 3D looping cosmos video background (`background.mp4`) with in-app toggle control.
  - Holographic frosted glassmorphism panels with luminous cyan/violet laser gradients and CRT scanline filter.
- **CHC Multi-Subtest Battery:**
  - **Fluid Matrix Reasoning ($G_f$):** 8 culture-fair Raven's & JCTI-style vector logic puzzles (rotations, XOR boolean logic, and vertex arithmetic).
  - **Spatial Working Memory ($G_{wm}$):** Digital Corsi Block-Tapping task testing dorsolateral prefrontal cortex (dlPFC) retention buffer across spans 4 to 8.
  - **Quantitative Induction ($G_q$):** High-order numerical series synthesis and mathematical pattern deduction.
  - **Symbolic Processing Speed ($Gs$):** 45-second burst discrimination task tracking millisecond reaction latency and throughput.
- **Clinical Psychometric Engine:**
  - Standard Wechsler Gaussian distribution ($\mu = 100, \sigma = 15$).
  - **General Ability Index (GAI) Detection:** Automatically detects large discrepancies ($\ge 20$ points) between reasoning ($G_f$) and processing speed ($G_s$) to prevent mathematical score suppression.
  - **Cumulative Gaussian Distribution:** Exact percentile ranking via error function integration with 95% Confidence Intervals ($\pm 4$ points).
  - Dynamic Wechsler bell curve plotting test-taker location relative to the Mensa cutoff ($130+$).
- **Clinical Report & Print Engine:**
  - Clean `@media print` isolation to export high-contrast PDF certificates (`Ctrl + P`) without UI clutter.

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

## License

MIT License. Designed for authorized neurocognitive research and educational assessment.
