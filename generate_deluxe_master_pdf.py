import asyncio
import os
import pymupdf
from playwright.async_api import async_playwright

async def generate_deluxe_pdf():
    print("Generating Deluxe Clinical Master Dossier PDF (A4 Protocol)...", flush=True)

    with open('pdf_border_protocol.js', 'r', encoding='utf-8') as f:
        protocol_js = f.read()

    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;800;900&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    @page {{
      size: 210mm 297mm;
      margin: 0;
    }}
    *, *::before, *::after {{ box-sizing: border-box; }}
    html, body {{
      margin: 0;
      padding: 0;
      background: #0B0A0C;
      color: #E8E0D2;
      font-family: 'Source Serif 4', Georgia, serif;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    .a4-page {{
      width: 210mm;
      height: 297mm;
      position: relative;
      overflow: hidden;
      page-break-after: always;
      break-after: page;
      padding: 22mm 18mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #0B0A0C;
    }}
    .cinzel {{ font-family: 'Cinzel', serif; }}
    .mono {{ font-family: 'JetBrains Mono', monospace; }}
  </style>
  <script>{protocol_js}</script>
</head>
<body>

  <!-- ==================== FOLIO I: PSYCHOMETRIC COMPOSITE & SCREENER MATRIX ==================== -->
  <div class="a4-page" id="folio1">
    <div id="svgLayer1" class="absolute inset-0 pointer-events-none"></div>
    <div style="position: relative; z-index: 5; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
      
      <!-- Header -->
      <div style="border-bottom: 2px solid #C6A15B; padding-bottom: 8px; display: flex; justify-content: space-between; align-items: flex-end;">
        <div>
          <div class="mono" style="font-size: 10px; color: #E8CB83; letter-spacing: 2px; text-transform: uppercase;">
            THE ARCANE WILLOW CODEX • CLINICAL NEUROPSYCHIATRIC DOSSIER
          </div>
          <div class="cinzel" style="font-size: 20px; font-weight: 800; color: #FFFFFF; letter-spacing: 1px;">
            FOLIO I • GENERAL INTELLECTUAL COMPOSITE & SCREENER MATRIX
          </div>
        </div>
        <div class="mono" style="font-size: 9.5px; color: #9A9AA5; text-align: right;">
          VALIDATION NONCE: <strong style="color: #34D399;">SEC-A4-9984X</strong><br>
          NORMATIVE SAMPLE: <strong style="color: #E8CB83;">ADULT N=2,200 (σ=15)</strong>
        </div>
      </div>

      <!-- Split Hero Block: FSIQ Callout + Gaussian Distribution -->
      <div style="display: grid; grid-template-columns: 1.15fr 1.85fr; gap: 12px; margin-top: 10px;">
        <!-- Left Hero Card -->
        <div style="background: #15131A; border: 1.5px solid #72512D; border-radius: 8px; padding: 12px; text-align: center; display: flex; flex-direction: column; justify-content: center;">
          <div class="mono" style="font-size: 9.5px; color: #9A9AA5; letter-spacing: 1.5px;">FULL SCALE INTELLIGENCE QUOTIENT</div>
          <div class="mono" style="font-size: 46px; font-weight: 900; color: #E8CB83; line-height: 1; margin: 4px 0;">138</div>
          <div class="cinzel" style="font-size: 12px; font-weight: bold; color: #FFFFFF;">VERY SUPERIOR</div>
          <div class="mono" style="font-size: 10px; color: #34D399; margin-top: 3px;">99.4th Percentile • GAI: 141</div>
          <div style="font-size: 9px; color: #9A9AA5; margin-top: 6px; border-top: 1px solid rgba(198,161,91,0.2); pt-1;">
            95% Confidence Interval: [132 — 143] (Mensa High-IQ Threshold)
          </div>
        </div>

        <!-- Right Gaussian Bell Curve Chart -->
        <div style="background: #15131A; border: 1.5px solid #72512D; border-radius: 8px; padding: 10px 14px; display: flex; flex-direction: column; justify-content: space-between;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="cinzel" style="font-size: 10px; font-weight: bold; color: #E8CB83;">GAUSSIAN NORMAL PROBABILITY DENSITY (μ=100, σ=15)</span>
            <span class="mono" style="font-size: 8.5px; color: #34D399; background: #064E3B; padding: 1px 6px; border-radius: 3px;">TOP 0.6% POPULATION</span>
          </div>
          <!-- Gaussian SVG Curve -->
          <svg viewBox="0 0 500 130" style="width: 100%; height: 95px; margin: 2px 0;">
            <defs>
              <linearGradient id="curveGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#E8CB83" stop-opacity="0.35"/>
                <stop offset="100%" stop-color="#C6A15B" stop-opacity="0.0"/>
              </linearGradient>
            </defs>
            <!-- Bell Curve Path -->
            <path d="M 20 110 Q 150 110, 200 70 Q 250 15, 250 15 Q 250 15, 300 70 Q 350 110, 480 110 Z" fill="url(#curveGrad)"/>
            <path d="M 20 110 Q 150 110, 200 70 Q 250 15, 250 15 Q 250 15, 300 70 Q 350 110, 480 110" fill="none" stroke="#C6A15B" stroke-width="2"/>
            <!-- Mean Axis (100) -->
            <line x1="250" y1="15" x2="250" y2="110" stroke="#9A9AA5" stroke-width="1" stroke-dasharray="3,3"/>
            <text x="250" y="122" fill="#9A9AA5" font-size="8.5" font-family="monospace" text-anchor="middle">μ=100</text>
            <!-- Mensa Threshold (130) -->
            <line x1="375" y1="50" x2="375" y2="110" stroke="#F59E0B" stroke-width="1.2" stroke-dasharray="2,2"/>
            <text x="375" y="122" fill="#F59E0B" font-size="8" font-family="monospace" text-anchor="middle">130 (Mensa)</text>
            <!-- Candidate Pin (138) -->
            <line x1="415" y1="30" x2="415" y2="110" stroke="#34D399" stroke-width="2"/>
            <circle cx="415" cy="30" r="4.5" fill="#34D399"/>
            <rect x="385" y="12" width="60" height="15" rx="3" fill="#064E3B" stroke="#34D399" stroke-width="0.8"/>
            <text x="415" y="23" fill="#FFFFFF" font-size="8.5" font-family="monospace" font-weight="bold" text-anchor="middle">IQ 138 ★</text>
          </svg>
          <div class="mono" style="font-size: 8.5px; color: #9A9AA5; display: flex; justify-content: space-between;">
            <span>-3σ (55)</span><span>-2σ (70)</span><span>-1σ (85)</span><span>Mean (100)</span><span>+1σ (115)</span><span>+2σ (130)</span><span>+3σ (145)</span>
          </div>
        </div>
      </div>

      <!-- CHC Cognitive Factor Breakdown (4 Pillars) -->
      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-top: 10px;">
        <div style="background: #15131A; border: 1px solid #72512D; border-radius: 6px; padding: 8px; text-align: center;">
          <div class="mono" style="font-size: 8.5px; color: #9A9AA5;">FLUID REASONING (Gf)</div>
          <div class="mono" style="font-size: 20px; font-weight: bold; color: #E8CB83;">142</div>
          <div class="mono" style="font-size: 8px; color: #34D399;">99.7th Percentile</div>
        </div>
        <div style="background: #15131A; border: 1px solid #72512D; border-radius: 6px; padding: 8px; text-align: center;">
          <div class="mono" style="font-size: 8.5px; color: #9A9AA5;">WORKING MEMORY (Gwm)</div>
          <div class="mono" style="font-size: 20px; font-weight: bold; color: #E8CB83;">130</div>
          <div class="mono" style="font-size: 8px; color: #34D399;">97.7th Percentile</div>
        </div>
        <div style="background: #15131A; border: 1px solid #72512D; border-radius: 6px; padding: 8px; text-align: center;">
          <div class="mono" style="font-size: 8.5px; color: #9A9AA5;">QUANTITATIVE LOGIC (Gq)</div>
          <div class="mono" style="font-size: 20px; font-weight: bold; color: #E8CB83;">136</div>
          <div class="mono" style="font-size: 8px; color: #34D399;">99.2nd Percentile</div>
        </div>
        <div style="background: #15131A; border: 1px solid #72512D; border-radius: 6px; padding: 8px; text-align: center;">
          <div class="mono" style="font-size: 8.5px; color: #9A9AA5;">PROCESSING SPEED (Gs)</div>
          <div class="mono" style="font-size: 20px; font-weight: bold; color: #E8CB83;">125</div>
          <div class="mono" style="font-size: 8px; color: #34D399;">95.0th Percentile</div>
        </div>
      </div>

      <!-- Strictly Typed 6-Row Screener Matrix Table -->
      <div style="margin-top: 10px; background: #15131A; border: 1.5px solid #72512D; border-radius: 8px; padding: 10px 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(198,161,91,0.25); padding-bottom: 4px; margin-bottom: 6px;">
          <span class="cinzel" style="font-size: 10.5px; font-weight: bold; color: #E8CB83; letter-spacing: 0.5px;">
            ✦ CLINICAL PSYCHIATRIC & NEUROBEHAVIORAL SCREENER MATRIX (DSM-5 & ICD-11)
          </span>
          <span class="mono" style="font-size: 8.5px; color: #9A9AA5;">6 STANDARDIZED SCALES</span>
        </div>
        <table style="width: 100%; border-collapse: collapse; font-family: monospace; font-size: 9.5px; text-align: left;">
          <thead>
            <tr style="border-bottom: 1px solid rgba(198,161,91,0.4); color: #E8CB83;">
              <th style="padding: 4px 6px;">CLINICAL DOMAIN</th>
              <th style="padding: 4px 6px;">INSTRUMENT</th>
              <th style="padding: 4px 6px;">SCORE / CUTOFF</th>
              <th style="padding: 4px 6px;">PCTL</th>
              <th style="padding: 4px 6px;">SEVERITY</th>
              <th style="padding: 4px 6px; text-align: right;">STATUS</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
              <td style="padding: 4px 6px; color: #FFFFFF;">Adult ADHD / Executive Inattention</td>
              <td style="padding: 4px 6px; color: #9A9AA5;">ASRS-v1.1</td>
              <td style="padding: 4px 6px; color: #E8CB83;">34 / 24</td>
              <td style="padding: 4px 6px; color: #9A9AA5;">88th</td>
              <td style="padding: 4px 6px; color: #EF4444; font-weight: bold;">Elevated</td>
              <td style="padding: 4px 6px; text-align: right;"><span style="background: #450A0A; color: #EF4444; padding: 1px 6px; border-radius: 3px; font-weight: bold;">SIGNIFICANT</span></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
              <td style="padding: 4px 6px; color: #FFFFFF;">Autonomic Vigilance / Stress</td>
              <td style="padding: 4px 6px; color: #9A9AA5;">DASS-21 (Stress)</td>
              <td style="padding: 4px 6px; color: #E8CB83;">6 / 27</td>
              <td style="padding: 4px 6px; color: #9A9AA5;">54th</td>
              <td style="padding: 4px 6px; color: #F59E0B;">Subclinical</td>
              <td style="padding: 4px 6px; text-align: right;"><span style="background: #3B2404; color: #F59E0B; padding: 1px 6px; border-radius: 3px; font-weight: bold;">MONITOR</span></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
              <td style="padding: 4px 6px; color: #FFFFFF;">Internalized Somatization & Fatigue</td>
              <td style="padding: 4px 6px; color: #9A9AA5;">PHQ-15</td>
              <td style="padding: 4px 6px; color: #E8CB83;">9 / 21</td>
              <td style="padding: 4px 6px; color: #9A9AA5;">70th</td>
              <td style="padding: 4px 6px; color: #EF4444;">Moderate</td>
              <td style="padding: 4px 6px; text-align: right;"><span style="background: #450A0A; color: #EF4444; padding: 1px 6px; border-radius: 3px; font-weight: bold;">ELEVATED</span></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
              <td style="padding: 4px 6px; color: #FFFFFF;">Perfectionistic Cognitive Rigidity</td>
              <td style="padding: 4px 6px; color: #9A9AA5;">FMPS-Brief</td>
              <td style="padding: 4px 6px; color: #E8CB83;">11 / 30</td>
              <td style="padding: 4px 6px; color: #9A9AA5;">38th</td>
              <td style="padding: 4px 6px; color: #10B981;">Low-Mod</td>
              <td style="padding: 4px 6px; text-align: right;"><span style="background: #064E3B; color: #10B981; padding: 1px 6px; border-radius: 3px; font-weight: bold;">WITHIN NORM</span></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
              <td style="padding: 4px 6px; color: #FFFFFF;">Sensory Processing Sensitivity</td>
              <td style="padding: 4px 6px; color: #9A9AA5;">HSP-Short</td>
              <td style="padding: 4px 6px; color: #E8CB83;">36 / 63</td>
              <td style="padding: 4px 6px; color: #9A9AA5;">63rd</td>
              <td style="padding: 4px 6px; color: #F59E0B;">Moderate</td>
              <td style="padding: 4px 6px; text-align: right;"><span style="background: #3B2404; color: #F59E0B; padding: 1px 6px; border-radius: 3px; font-weight: bold;">COMPENSATED</span></td>
            </tr>
            <tr>
              <td style="padding: 4px 6px; color: #FFFFFF;">Emotional Suppression / Stoic Mask</td>
              <td style="padding: 4px 6px; color: #9A9AA5;">ERQ-Suppress</td>
              <td style="padding: 4px 6px; color: #E8CB83;">3 / 12</td>
              <td style="padding: 4px 6px; color: #9A9AA5;">22nd</td>
              <td style="padding: 4px 6px; color: #10B981;">Baseline</td>
              <td style="padding: 4px 6px; text-align: right;"><span style="background: #064E3B; color: #10B981; padding: 1px 6px; border-radius: 3px; font-weight: bold;">CLEARED</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Footer -->
      <div style="border-top: 1px solid rgba(198,161,91,0.3); padding-top: 6px; display: flex; justify-content: space-between; font-size: 9px; font-family: monospace; color: #9A9AA5;">
        <span>NEUROMETRIC PSYCHOMETRIC ENGINE</span>
        <span style="color: #E8CB83;">FOLIO I OF III • MASTER CLINICAL DOSSIER</span>
        <span>CONFIDENTIAL MEDICAL RECORD</span>
      </div>

    </div>
  </div>

  <!-- ==================== FOLIO II: MULTIMODAL FACIAL & VOCAL TELEMETRY ==================== -->
  <div class="a4-page" id="folio2">
    <div id="svgLayer2" class="absolute inset-0 pointer-events-none"></div>
    <div style="position: relative; z-index: 5; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
      
      <!-- Header -->
      <div style="border-bottom: 2px solid #C6A15B; padding-bottom: 8px; display: flex; justify-content: space-between; align-items: flex-end;">
        <div>
          <div class="mono" style="font-size: 10px; color: #E8CB83; letter-spacing: 2px; text-transform: uppercase;">
            THE ARCANE WILLOW CODEX • SENSOR BIOMETRICS
          </div>
          <div class="cinzel" style="font-size: 20px; font-weight: 800; color: #FFFFFF; letter-spacing: 1px;">
            FOLIO II • MULTIMODAL FACIAL, GAZE & ACOUSTIC TELEMETRY
          </div>
        </div>
        <div class="mono" style="font-size: 9.5px; color: #34D399; background: #064E3B; padding: 2px 8px; border-radius: 3px; font-weight: bold;">
          WEBRTC LOCAL VOLATILE STREAM
        </div>
      </div>

      <!-- 3-Column Multimodal Sensor Grid -->
      <div style="display: grid; grid-template-columns: 1fr 1.15fr 1fr; gap: 8px; margin-top: 10px;">
        <!-- Optical Gaze Card -->
        <div style="background: #15131A; border: 1px solid #72512D; border-radius: 6px; padding: 8px 10px;">
          <div class="mono" style="font-size: 10px; color: #E8CB83; font-weight: bold; margin-bottom: 4px;">
            👁️ OPTICAL GAZE & OCULAR
          </div>
          <div class="mono" style="font-size: 9.5px; color: #E8E0D2; line-height: 1.5;">
            • Fixation Hold: <strong style="color: #34D399;">95.4%</strong> (Central)<br>
            • Saccadic Latency: <strong style="color: #E8CB83;">142 ms</strong> (Reflex)<br>
            • Blink Frequency: <strong style="color: #9A9AA5;">14.2 /min</strong>
          </div>
        </div>

        <!-- Real-Time Facial Expression Matrix Card -->
        <div style="background: #15131A; border: 1px solid #72512D; border-radius: 6px; padding: 8px 10px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <span class="mono" style="font-size: 10px; color: #E8CB83; font-weight: bold;">😊 FACIAL EXPRESSION</span>
            <span class="mono" style="font-size: 8px; color: #34D399; background: #064E3B; padding: 1px 4px; border-radius: 2px;">FOCUSED (68%)</span>
          </div>
          <div class="mono" style="font-size: 9px; color: #E8E0D2; line-height: 1.45;">
            • Focus: <strong style="color: #34D399;">68%</strong> | Strain: <strong style="color: #F59E0B;">14%</strong><br>
            • Smile (AU12): <strong style="color: #E8CB83;">10%</strong> | Perplex: <strong style="color: #9A9AA5;">8%</strong><br>
            • Facial Tension: <strong style="color: #34D399;">Low (16.2%)</strong>
          </div>
        </div>

        <!-- Acoustic Vocal Prosody Card -->
        <div style="background: #15131A; border: 1px solid #72512D; border-radius: 6px; padding: 8px 10px;">
          <div class="mono" style="font-size: 10px; color: #E8CB83; font-weight: bold; margin-bottom: 4px;">
            🎙️ VOCAL ACOUSTIC FFT
          </div>
          <div class="mono" style="font-size: 9.5px; color: #E8E0D2; line-height: 1.5;">
            • Pitch F0: <strong style="color: #E8CB83;">124.8 Hz</strong><br>
            • Jitter Quotient: <strong style="color: #34D399;">0.38%</strong><br>
            • Stress Index: <strong style="color: #34D399;">18.4% (Nominal)</strong>
          </div>
        </div>
      </div>

      <!-- Neuro-Motor Reaction Telemetry -->
      <div style="margin-top: 10px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; text-align: center;">
        <div style="background: #15131A; border: 1.2px solid #72512D; border-radius: 6px; padding: 8px;">
          <span class="mono" style="font-size: 9.5px; color: #9A9AA5;">MEAN MOTOR REACTION</span>
          <div class="mono" style="font-size: 22px; font-weight: 900; color: #E8CB83;">218ms</div>
          <span class="mono" style="font-size: 8.5px; color: #34D399;">Normal Adult (200-280ms)</span>
        </div>
        <div style="background: #15131A; border: 1.2px solid #72512D; border-radius: 6px; padding: 8px;">
          <span class="mono" style="font-size: 9.5px; color: #9A9AA5;">INHIBITORY BRAKING</span>
          <div class="mono" style="font-size: 22px; font-weight: 900; color: #34D399;">95%</div>
          <span class="mono" style="font-size: 8.5px; color: #34D399;">Optimal Prefrontal Gating</span>
        </div>
        <div style="background: #15131A; border: 1.2px solid #72512D; border-radius: 6px; padding: 8px;">
          <span class="mono" style="font-size: 9.5px; color: #9A9AA5;">COMMISSION ERRORS</span>
          <div class="mono" style="font-size: 22px; font-weight: 900; color: #F59E0B;">1</div>
          <span class="mono" style="font-size: 8.5px; color: #9A9AA5;">Cutoff Threshold ≤ 3</span>
        </div>
      </div>

      <!-- Verbatim Patient Confession 1: Repressed Rage -->
      <div style="margin-top: 10px; background: #15131A; border-left: 4px solid #EF4444; border-radius: 0 6px 6px 0; padding: 10px 14px; border-top: 1px solid #72512D; border-right: 1px solid #72512D; border-bottom: 1px solid #72512D;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <span class="cinzel" style="font-size: 10.5px; font-weight: bold; color: #EF4444; text-transform: uppercase;">
            INQUIRY I: REPRESSED RAGE & BETRAYAL CATALYSIS
          </span>
          <span class="mono" style="font-size: 8.5px; color: #E8CB83;">[VERBATIM CLINICAL TRANSCRIPT]</span>
        </div>
        <div style="font-size: 11px; color: #F1F5F9; font-style: italic; background: #0B0A0C; padding: 8px 12px; border-radius: 4px; border: 1px solid #72512D; line-height: 1.5;">
          "When people make false accusations against my integrity despite my loyal dedication, an intense internal fire of indignation is ignited."
        </div>
        <div style="font-size: 10px; color: #9A9AA5; margin-top: 4px;">
          • Clinical Biomarker: Sympathetic surge suppressed via stoic intellectualization.
        </div>
      </div>

      <!-- Verbatim Patient Confession 2: Stoic Emotional Armor -->
      <div style="margin-top: 8px; background: #15131A; border-left: 4px solid #3B82F6; border-radius: 0 6px 6px 0; padding: 10px 14px; border-top: 1px solid #72512D; border-right: 1px solid #72512D; border-bottom: 1px solid #72512D;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <span class="cinzel" style="font-size: 10.5px; font-weight: bold; color: #60A5FA; text-transform: uppercase;">
            INQUIRY II: STOIC DEFENSIVE ARMOR & VULNERABILITY SUPPRESSION
          </span>
          <span class="mono" style="font-size: 8.5px; color: #E8CB83;">[VERBATIM CLINICAL TRANSCRIPT]</span>
        </div>
        <div style="font-size: 11px; color: #F1F5F9; font-style: italic; background: #0B0A0C; padding: 8px 12px; border-radius: 4px; border: 1px solid #72512D; line-height: 1.5;">
          "Ever since childhood, I have maintained an impenetrable, stoic persona so that no vulnerability can be perceived or exploited."
        </div>
        <div style="font-size: 10px; color: #9A9AA5; margin-top: 4px;">
          • Clinical Biomarker: Chronic baseline hyper-vigilance manifesting as sub-occipital cranial tension.
        </div>
      </div>

      <!-- Footer -->
      <div style="border-top: 1px solid rgba(198,161,91,0.3); padding-top: 6px; display: flex; justify-content: space-between; font-size: 9px; font-family: monospace; color: #9A9AA5;">
        <span>NEUROMETRIC PSYCHOMETRIC ENGINE</span>
        <span style="color: #E8CB83;">FOLIO II OF III • MULTIMODAL SENSORS</span>
        <span>CONFIDENTIAL MEDICAL RECORD</span>
      </div>

    </div>
  </div>

  <!-- ==================== FOLIO III: NEURO-SOMATIC REHABILITATION ==================== -->
  <div class="a4-page" id="folio3">
    <div id="svgLayer3" class="absolute inset-0 pointer-events-none"></div>
    <div style="position: relative; z-index: 5; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
      
      <!-- Header -->
      <div style="border-bottom: 2px solid #C6A15B; padding-bottom: 8px; display: flex; justify-content: space-between; align-items: flex-end;">
        <div>
          <div class="mono" style="font-size: 10px; color: #E8CB83; letter-spacing: 2px; text-transform: uppercase;">
            THE ARCANE WILLOW CODEX • HOLISTIC PRESCRIPTION
          </div>
          <div class="cinzel" style="font-size: 20px; font-weight: 800; color: #FFFFFF; letter-spacing: 1px;">
            FOLIO III • 4-PILLAR REHABILITATION & NEURO-SOMATICS
          </div>
        </div>
        <div class="mono" style="font-size: 9.5px; color: #34D399;">
          CLINICALLY VERIFIED THERAPEUTIC REGIMEN
        </div>
      </div>

      <!-- 4 Pillars Grid -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
        <div style="background: #15131A; border: 1.2px solid #72512D; border-radius: 6px; padding: 9px 12px;">
          <div class="cinzel" style="font-size: 11px; font-weight: bold; color: #E8CB83; margin-bottom: 3px;">
            PILLAR I: NEURO-SOMATIC DOWN-REGULATION
          </div>
          <div style="font-size: 10.5px; line-height: 1.45; color: #E8E0D2;">
            Cyclic physiological sighing (double inhale + extended 8-sec exhale) to stimulate vagal brake and down-regulate sympathetic hyperarousal.
          </div>
        </div>

        <div style="background: #15131A; border: 1.2px solid #72512D; border-radius: 6px; padding: 9px 12px;">
          <div class="cinzel" style="font-size: 11px; font-weight: bold; color: #E8CB83; margin-bottom: 3px;">
            PILLAR II: COGNITIVE FLEXIBILITY RETRAINING
          </div>
          <div style="font-size: 10.5px; line-height: 1.45; color: #E8E0D2;">
            Dismantle binary black-and-white attribution traps using Socratic cognitive reframing and daily cognitive defusion exercises.
          </div>
        </div>

        <div style="background: #15131A; border: 1.2px solid #72512D; border-radius: 6px; padding: 9px 12px;">
          <div class="cinzel" style="font-size: 11px; font-weight: bold; color: #E8CB83; margin-bottom: 3px;">
            PILLAR III: CHRONO-BIOLOGICAL ENTRAINMENT
          </div>
          <div style="font-size: 10.5px; line-height: 1.45; color: #E8E0D2;">
            10,000 lux natural sunlight within 30 min of waking; strict blue-light curfew after 21:00 to restore restorative Stage 3 SWS delta power.
          </div>
        </div>

        <div style="background: #15131A; border: 1.2px solid #72512D; border-radius: 6px; padding: 9px 12px;">
          <div class="cinzel" style="font-size: 11px; font-weight: bold; color: #E8CB83; margin-bottom: 3px;">
            PILLAR IV: INTELLECTUAL HYGIENE & DOPAMINE
          </div>
          <div style="font-size: 10.5px; line-height: 1.45; color: #E8E0D2;">
            Enforce daily 90-minute deep-work cognitive sprints punctuated by non-digital sensory reset periods to prevent executive burnout.
          </div>
        </div>
      </div>

      <!-- Sacred Mudras & Hand Gestures Section -->
      <div style="margin-top: 10px; background: #15131A; border: 1.5px solid #72512D; border-radius: 8px; padding: 10px 14px;">
        <div class="cinzel" style="font-size: 11px; font-weight: bold; color: #E8CB83; border-bottom: 1px solid rgba(198,161,91,0.25); padding-bottom: 4px; margin-bottom: 8px;">
          ✦ THERAPEUTIC NEURO-SOMATIC MUDRAS (BIO-ELECTRIC INTEGRATION)
        </div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
          <!-- Gyan Mudra -->
          <div style="background: #0B0A0C; border: 1px solid rgba(198,161,91,0.3); border-radius: 6px; padding: 8px; text-align: center;">
            <div style="font-size: 18px; margin-bottom: 2px;">👌</div>
            <div class="cinzel" style="font-size: 10.5px; font-weight: bold; color: #E8CB83;">GYAN MUDRA</div>
            <div class="mono" style="font-size: 8.5px; color: #34D399; margin: 2px 0;">Vagus Nerve Grounding</div>
            <div style="font-size: 9.5px; color: #9A9AA5; line-height: 1.35;">
              Thumb and index fingertip contact. Calms involuntary eye tremor and stabilizes neural alpha rhythms.
            </div>
          </div>
          <!-- Prana Mudra -->
          <div style="background: #0B0A0C; border: 1px solid rgba(198,161,91,0.3); border-radius: 6px; padding: 8px; text-align: center;">
            <div style="font-size: 18px; margin-bottom: 2px;">🤞</div>
            <div class="cinzel" style="font-size: 10.5px; font-weight: bold; color: #E8CB83;">PRANA MUDRA</div>
            <div class="mono" style="font-size: 8.5px; color: #34D399; margin: 2px 0;">Vital Energy Restoration</div>
            <div style="font-size: 9.5px; color: #9A9AA5; line-height: 1.35;">
              Thumb tip touches ring and little fingertips. Alleviates somatization fatigue and sharpens optical focus.
            </div>
          </div>
          <!-- Hakini Mudra -->
          <div style="background: #0B0A0C; border: 1px solid rgba(198,161,91,0.3); border-radius: 6px; padding: 8px; text-align: center;">
            <div style="font-size: 18px; margin-bottom: 2px;">👐</div>
            <div class="cinzel" style="font-size: 10.5px; font-weight: bold; color: #E8CB83;">HAKINI MUDRA</div>
            <div class="mono" style="font-size: 8.5px; color: #34D399; margin: 2px 0;">Hemispheric Coherence</div>
            <div style="font-size: 9.5px; color: #9A9AA5; line-height: 1.35;">
              All ten fingertips touch lightly together. Optimizes interhemispheric transfer for high-IQ working memory.
            </div>
          </div>
        </div>
      </div>

      <!-- Solfeggio Frequencies & Classical Indian Raag Therapy -->
      <div style="margin-top: 10px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <!-- Solfeggio Sound Therapy -->
        <div style="background: #15131A; border: 1.2px solid #72512D; border-radius: 6px; padding: 9px 12px;">
          <div class="cinzel" style="font-size: 10.5px; font-weight: bold; color: #E8CB83; margin-bottom: 4px;">
            🎼 SOLFEGGIO NEURO-ACOUSTIC RESONANCE
          </div>
          <div class="mono" style="font-size: 9.5px; color: #E8E0D2; line-height: 1.5;">
            • <strong style="color: #34D399;">528 Hz (Transformation / Reset)</strong>: Cellular recovery.<br>
            • <strong style="color: #E8CB83;">432 Hz (Cellular Harmony)</strong>: Heart rate variability balance.<br>
            • <strong style="color: #9A9AA5;">396 Hz (Liberation)</strong>: Dissolution of subconscious guilt.
          </div>
        </div>

        <!-- Classical Raag Therapy -->
        <div style="background: #15131A; border: 1.2px solid #72512D; border-radius: 6px; padding: 9px 12px;">
          <div class="cinzel" style="font-size: 10.5px; font-weight: bold; color: #E8CB83; margin-bottom: 4px;">
            🎶 CLASSICAL INDIAN RAAG PRESCRIPTIONS
          </div>
          <div class="mono" style="font-size: 9.5px; color: #E8E0D2; line-height: 1.5;">
            • <strong style="color: #E8CB83;">Raag Darbari Kanada (Night)</strong>: Heavy somatic tranquility.<br>
            • <strong style="color: #34D399;">Raag Bageshri (Evening)</strong>: Cathartic emotional release.<br>
            • <strong style="color: #60A5FA;">Raag Ahir Bhairav (Dawn)</strong>: Restores morning diurnal cortisol.
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div style="border-top: 1px solid rgba(198,161,91,0.3); padding-top: 6px; display: flex; justify-content: space-between; font-size: 9px; font-family: monospace; color: #9A9AA5;">
        <span>NEUROMETRIC PSYCHOMETRIC ENGINE</span>
        <span style="color: #E8CB83;">FOLIO III OF III • HOLISTIC REHABILITATION</span>
        <span>FINAL CLINICAL CERTIFICATION</span>
      </div>

    </div>
  </div>

  <script>
    // Inject distinct premium borders using our mathematical protocol:
    // Page 1: Sacred Geometry Mandala
    document.getElementById('svgLayer1').innerHTML = PdfBorderProtocol.generateSvg('sacred_mandala', 'portrait');
    // Page 2: Arcane Golden Willow
    document.getElementById('svgLayer2').innerHTML = PdfBorderProtocol.generateSvg('arcane_willow', 'portrait');
    // Page 3: Art Deco Stepped Chevron
    document.getElementById('svgLayer3').innerHTML = PdfBorderProtocol.generateSvg('art_deco_chevron', 'portrait');
  </script>
</body>
</html>
"""

    temp_html = os.path.abspath('deluxe_master_dossier.html')
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    out_pdf = r"C:\Users\wwwam\Downloads\NeuroMetric_Clinical_Master_Dossier_Deluxe_A4.pdf"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        file_url = f"file:///{temp_html.replace(os.sep, '/')}"
        await page.goto(file_url, wait_until='networkidle')
        await page.wait_for_timeout(1000)

        await page.pdf(
            path=out_pdf,
            format='A4',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        )
        await browser.close()

    print(f"Deluxe PDF generated: {out_pdf} ({os.path.getsize(out_pdf)} bytes)", flush=True)

    # Render pages 1, 2, 3 into preview images
    doc = pymupdf.open(out_pdf)
    print(f"Total pages in PDF: {len(doc)}", flush=True)
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(dpi=150)
        img_path = f"C:/Users/wwwam/.gemini/antigravity/brain/5d55040c-837b-4663-8bf0-2dfb1696f87e/deluxe_master_p{i+1}.png"
        pix.save(img_path)
        print(f"Saved visual sample: {img_path}", flush=True)

if __name__ == '__main__':
    asyncio.run(generate_deluxe_pdf())
