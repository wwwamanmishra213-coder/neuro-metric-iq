/**
 * ARCANE WILLOW CODEX & CLINICAL DOSSIER
 * PDF BORDER DESIGN SYSTEM & COORDINATE PROTOCOL (A4 SPECIFICATION)
 * 
 * Standard ISO 216 A4 Dimensions:
 * - Portrait:  210mm x 297mm | 595.28pt x 841.89pt | Aspect 1 : 1.4142
 * - Landscape: 297mm x 210mm | 841.89pt x 595.28pt | Aspect 1.4142 : 1
 * 
 * 20 Distinct Architectural Vector Borders with Exact Bounding Coordinates
 */

(function(root) {
  'use strict';

  const A4_SPECS = {
    portrait: {
      widthMm: 210,
      heightMm: 297,
      widthPt: 595.28,
      heightPt: 841.89,
      viewBox: "0 0 1000 1414",
      aspectRatio: 1.4142,
      marginMm: { top: 22, right: 18, bottom: 22, left: 18 },
      safeBox: { x: 85, y: 105, width: 830, height: 1204 }
    },
    landscape: {
      widthMm: 297,
      heightMm: 210,
      widthPt: 841.89,
      heightPt: 595.28,
      viewBox: "0 0 1414 1000",
      aspectRatio: 0.7071,
      marginMm: { top: 18, right: 22, bottom: 18, left: 22 },
      safeBox: { x: 105, y: 85, width: 1204, height: 830 }
    }
  };

  const BORDER_TEMPLATES = {
    // 1. ARCANE WILLOW (Current Signature)
    arcane_willow: {
      id: "arcane_willow",
      name: "Arcane Golden Willow",
      category: "Arcane Botanical",
      palette: { primary: "#C6A15B", secondary: "#E8CB83", accent: "#72512D", bg: "#0B0A0C" },
      cornerSize: 80,
      sideMargin: 40,
      coordinates: {
        outerFrame: { x1: 28, y1: 28, x2: 972, y2: 1386 },
        innerFrame: { x1: 40, y1: 40, x2: 960, y2: 1374 },
        safeBox: { x: 70, y: 75, width: 860, height: 1264 }
      },
      render: (w, h, p) => `
        <!-- Double Regal Frame Perimeter -->
        <rect x="26" y="26" width="${w-52}" height="${h-52}" fill="none" stroke="${p.accent}" stroke-width="1.8" opacity="0.75"/>
        <rect x="38" y="38" width="${w-76}" height="${h-76}" fill="none" stroke="${p.primary}" stroke-width="1.2" opacity="0.9"/>
        <rect x="44" y="44" width="${w-88}" height="${h-88}" fill="none" stroke="${p.secondary}" stroke-width="0.5" stroke-dasharray="4,4" opacity="0.5"/>

        <!-- 4 Botanical Willow Corner Flourishes (Tightly Bounded: Zero Text Collision) -->
        ${[ [38, 38, 1, 1], [w-38, 38, -1, 1], [38, h-38, 1, -1], [w-38, h-38, -1, -1] ].map(([cx, cy, sx, sy]) => `
          <g transform="translate(${cx}, ${cy})">
            <!-- Corner Rosette -->
            <circle cx="0" cy="0" r="3.5" fill="${p.secondary}"/>
            <polygon points="0,-9 9,0 0,9 -9,0" fill="none" stroke="${p.primary}" stroke-width="1"/>
            <!-- Botanical Willow Branch (Curving strictly in corner margin) -->
            <path d="M 0 0 Q ${sx * 16} ${sy * 6} ${sx * 26} ${sy * 26}" fill="none" stroke="${p.primary}" stroke-width="1.5"/>
            <path d="M 0 0 Q ${sx * 6} ${sy * 16} ${sx * 26} ${sy * 26}" fill="none" stroke="${p.secondary}" stroke-width="1" opacity="0.7"/>
            <circle cx="${sx * 26}" cy="${sy * 26}" r="2.5" fill="${p.secondary}"/>
            <!-- Delicate Margin Leafbuds -->
            <path d="M 0 ${sy * 18} Q ${sx * 5} ${sy * 24} 0 ${sy * 30}" fill="none" stroke="${p.primary}" stroke-width="1"/>
            <path d="M ${sx * 18} 0 Q ${sx * 24} ${sy * 5} ${sx * 30} 0" fill="none" stroke="${p.primary}" stroke-width="1"/>
          </g>
        `).join('')}

        <!-- Mid-Point Cardinal Diamond Seals -->
        <g fill="${p.primary}">
          <polygon points="${w/2},30 ${w/2+7},38 ${w/2},46 ${w/2-7},38"/>
          <polygon points="${w/2},${h-46} ${w/2+7},${h-38} ${w/2},${h-30} ${w/2-7},${h-38}"/>
          <polygon points="30,${h/2} 38,${h/2+7} 46,${h/2} 38,${h/2-7}"/>
          <polygon points="${w-46},${h/2} ${w-38},${h/2+7} ${w-30},${h/2} ${w-38},${h/2-7}"/>
        </g>
      `
    },

    // 2. SACRED GEOMETRY MANDALA
    sacred_mandala: {
      id: "sacred_mandala",
      name: "Sacred Geometry Mandala",
      category: "Geometric Arcane",
      palette: { primary: "#D4AF37", secondary: "#FFF8DC", accent: "#5C4033", bg: "#0D0A14" },
      cornerSize: 140,
      sideMargin: 45,
      coordinates: {
        outerFrame: { x1: 35, y1: 35, x2: 965, y2: 1379 },
        innerFrame: { x1: 50, y1: 50, x2: 950, y2: 1364 },
        safeBox: { x: 90, y: 110, width: 820, height: 1194 }
      },
      render: (w, h, p) => `
        <rect x="35" y="35" width="${w-70}" height="${h-70}" fill="none" stroke="${p.primary}" stroke-width="1.5" stroke-dasharray="8,4"/>
        <rect x="48" y="48" width="${w-96}" height="${h-96}" fill="none" stroke="${p.primary}" stroke-width="2"/>
        <!-- 4 Mandala Corner Rosettes -->
        ${[ [48, 48], [w-48, 48], [48, h-48], [w-48, h-48] ].map(([cx, cy]) => `
          <g transform="translate(${cx}, ${cy})">
            <circle cx="0" cy="0" r="42" fill="none" stroke="${p.primary}" stroke-width="1.2"/>
            <circle cx="0" cy="0" r="28" fill="none" stroke="${p.secondary}" stroke-width="0.8"/>
            <polygon points="0,-36 25,-25 36,0 25,25 0,36 -25,25 -36,0 -25,-25" fill="none" stroke="${p.primary}" stroke-width="1"/>
            <polygon points="0,-25 25,0 0,25 -25,0" fill="${p.accent}" opacity="0.3"/>
            <circle cx="0" cy="0" r="5" fill="${p.secondary}"/>
          </g>
        `).join('')}
        <!-- Mid-Point Cardinal Diamonds -->
        <g fill="${p.primary}">
          <polygon points="${w/2},38 ${w/2+10},48 ${w/2},58 ${w/2-10},48"/>
          <polygon points="${w/2},${h-58} ${w/2+10},${h-48} ${w/2},${h-38} ${w/2-10},${h-48}"/>
          <polygon points="38,${h/2} 48,${h/2+10} 58,${h/2} 48,${h/2-10}"/>
          <polygon points="${w-58},${h/2} ${w-48},${h/2+10} ${w-38},${h/2} ${w-48},${h/2-10}"/>
        </g>
      `
    },

    // 3. ART DECO CHEVRON
    art_deco_chevron: {
      id: "art_deco_chevron",
      name: "Art Deco Stepped Chevron",
      category: "Architectural Classic",
      palette: { primary: "#E5C158", secondary: "#F3E5AB", accent: "#8B6508", bg: "#0A0D12" },
      cornerSize: 120,
      sideMargin: 38,
      coordinates: {
        outerFrame: { x1: 28, y1: 28, x2: 972, y2: 1386 },
        innerFrame: { x1: 42, y1: 42, x2: 958, y2: 1372 },
        safeBox: { x: 80, y: 95, width: 840, height: 1224 }
      },
      render: (w, h, p) => `
        <rect x="28" y="28" width="${w-56}" height="${h-56}" fill="none" stroke="${p.primary}" stroke-width="3"/>
        <rect x="36" y="36" width="${w-72}" height="${h-72}" fill="none" stroke="${p.accent}" stroke-width="1"/>
        <rect x="46" y="46" width="${w-92}" height="${h-92}" fill="none" stroke="${p.secondary}" stroke-width="1.5"/>
        <!-- Stepped Chevrons on 4 Corners -->
        <g stroke="${p.primary}" stroke-width="2" fill="none">
          <!-- Top Left -->
          <polyline points="28,80 80,80 80,28"/>
          <polyline points="28,105 105,105 105,28"/>
          <!-- Top Right -->
          <polyline points="${w-28},80 ${w-80},80 ${w-80},28"/>
          <polyline points="${w-28},105 ${w-105},105 ${w-105},28"/>
          <!-- Bottom Left -->
          <polyline points="28,${h-80} 80,${h-80} 80,${h-28}"/>
          <polyline points="28,${h-105} 105,${h-105} 105,${h-28}"/>
          <!-- Bottom Right -->
          <polyline points="${w-28},${h-80} ${w-80},${h-80} ${w-80},${h-28}"/>
          <polyline points="${w-28},${h-105} ${w-105},${h-105} ${w-105},${h-28}"/>
        </g>
        <polygon points="${w/2},24 ${w/2+30},46 ${w/2},68 ${w/2-30},46" fill="${p.accent}" stroke="${p.secondary}" stroke-width="1.5"/>
        <polygon points="${w/2},${h-68} ${w/2+30},${h-46} ${w/2},${h-24} ${w/2-30},${h-46}" fill="${p.accent}" stroke="${p.secondary}" stroke-width="1.5"/>
      `
    },

    // 4. CYBER RETICLE TELEMETRY HUD
    cyber_reticle_hud: {
      id: "cyber_reticle_hud",
      name: "Cybernetic HUD Reticle",
      category: "Sci-Fi Telemetry",
      palette: { primary: "#00F0FF", secondary: "#7000FF", accent: "#003B46", bg: "#050811" },
      cornerSize: 110,
      sideMargin: 35,
      coordinates: {
        outerFrame: { x1: 25, y1: 25, x2: 975, y2: 1389 },
        innerFrame: { x1: 38, y1: 38, x2: 962, y2: 1376 },
        safeBox: { x: 75, y: 85, width: 850, height: 1244 }
      },
      render: (w, h, p) => `
        <!-- Outer Target Brackets -->
        <path d="M 25 120 L 25 25 L 120 25" fill="none" stroke="${p.primary}" stroke-width="3.5"/>
        <path d="M ${w-120} 25 L ${w-25} 25 L ${w-25} 120" fill="none" stroke="${p.primary}" stroke-width="3.5"/>
        <path d="M 25 ${h-120} L 25 ${h-25} L 120 ${h-25}" fill="none" stroke="${p.primary}" stroke-width="3.5"/>
        <path d="M ${w-120} ${h-25} L ${w-25} ${h-25} L ${w-25} ${h-120}" fill="none" stroke="${p.primary}" stroke-width="3.5"/>
        <!-- Fine Caliper Lines -->
        <rect x="40" y="40" width="${w-80}" height="${h-80}" fill="none" stroke="${p.primary}" stroke-width="1" opacity="0.4" stroke-dasharray="12,6"/>
        <!-- Telemetry Coordinate Ticks Left/Right -->
        ${Array.from({length: 13}).map((_, i) => `
          <line x1="25" y1="${150 + i * 90}" x2="35" y2="${150 + i * 90}" stroke="${p.primary}" stroke-width="1.5"/>
          <line x1="${w-35}" y1="${150 + i * 90}" x2="${w-25}" y2="${150 + i * 90}" stroke="${p.primary}" stroke-width="1.5"/>
        `).join('')}
        <!-- Top HUD Sensor Callouts -->
        <text x="50" y="22" fill="${p.primary}" font-family="monospace" font-size="10" font-weight="bold">SEC_01 // LAT: 45.242.08</text>
        <text x="${w-180}" y="22" fill="${p.primary}" font-family="monospace" font-size="10" font-weight="bold">FRAME // A4_ISO_216</text>
      `
    },

    // 5. CELTIC KNOT ILLUMINATION
    celtic_knot: {
      id: "celtic_knot",
      name: "Celtic Knotwork Illumination",
      category: "Ancient Manuscript",
      palette: { primary: "#2E8B57", secondary: "#D4AF37", accent: "#1B4D3E", bg: "#0C120C" },
      cornerSize: 150,
      sideMargin: 48,
      coordinates: {
        outerFrame: { x1: 35, y1: 35, x2: 965, y2: 1379 },
        innerFrame: { x1: 52, y1: 52, x2: 948, y2: 1362 },
        safeBox: { x: 92, y: 110, width: 816, height: 1194 }
      },
      render: (w, h, p) => `
        <rect x="35" y="35" width="${w-70}" height="${h-70}" fill="none" stroke="${p.secondary}" stroke-width="3"/>
        <rect x="52" y="52" width="${w-104}" height="${h-104}" fill="none" stroke="${p.primary}" stroke-width="1.8"/>
        <!-- Celtic Corner Weave Quadrants -->
        ${[ [52, 52], [w-52, 52], [52, h-52], [w-52, h-52] ].map(([cx, cy], idx) => {
          const sx = (idx % 2 === 0) ? 1 : -1;
          const sy = (idx < 2) ? 1 : -1;
          return `
            <g transform="translate(${cx}, ${cy}) scale(${sx}, ${sy})">
              <path d="M 0 0 C 30 10, 60 40, 80 80 C 40 60, 10 30, 0 0 Z" fill="${p.primary}" opacity="0.4"/>
              <path d="M 0 30 Q 30 30 30 0 M 0 60 Q 60 60 60 0 M 0 90 Q 90 90 90 0" fill="none" stroke="${p.secondary}" stroke-width="2.5"/>
              <circle cx="45" cy="45" r="8" fill="none" stroke="${p.secondary}" stroke-width="2"/>
              <circle cx="45" cy="45" r="3" fill="${p.secondary}"/>
            </g>
          `;
        }).join('')}
      `
    },

    // 6. GOTHIC SCRIPTORIUM
    gothic_scriptorium: {
      id: "gothic_scriptorium",
      name: "Gothic Cathedral Scriptorium",
      category: "Ecclesiastical Medieval",
      palette: { primary: "#A67C52", secondary: "#D4AF37", accent: "#4A0E17", bg: "#0D0B0E" },
      cornerSize: 135,
      sideMargin: 42,
      coordinates: {
        outerFrame: { x1: 32, y1: 32, x2: 968, y2: 1382 },
        innerFrame: { x1: 46, y1: 46, x2: 954, y2: 1368 },
        safeBox: { x: 86, y: 105, width: 828, height: 1204 }
      },
      render: (w, h, p) => `
        <rect x="32" y="32" width="${w-64}" height="${h-64}" fill="none" stroke="${p.primary}" stroke-width="2.5"/>
        <rect x="46" y="46" width="${w-92}" height="${h-92}" fill="none" stroke="${p.secondary}" stroke-width="1"/>
        <!-- Gothic Lancet Arch Top-Center -->
        <path d="M ${w/2-70} 46 C ${w/2-40} 10, ${w/2} 5, ${w/2} 5 C ${w/2} 5, ${w/2+40} 10, ${w/2+70} 46 Z" fill="${p.accent}" stroke="${p.secondary}" stroke-width="2"/>
        <circle cx="${w/2}" cy="28" r="7" fill="none" stroke="${p.secondary}" stroke-width="1.5"/>
        <!-- Trefoils at 4 Corners -->
        ${[ [46, 46], [w-46, 46], [46, h-46], [w-46, h-46] ].map(([cx, cy]) => `
          <g transform="translate(${cx}, ${cy})">
            <circle cx="0" cy="-14" r="10" fill="none" stroke="${p.secondary}" stroke-width="1.8"/>
            <circle cx="-12" cy="7" r="10" fill="none" stroke="${p.secondary}" stroke-width="1.8"/>
            <circle cx="12" cy="7" r="10" fill="none" stroke="${p.secondary}" stroke-width="1.8"/>
            <circle cx="0" cy="0" r="3" fill="${p.secondary}"/>
          </g>
        `).join('')}
      `
    },

    // 7. BAROQUE FILIGREE SCROLLWORK
    baroque_filigree: {
      id: "baroque_filigree",
      name: "Baroque Acanthus Filigree",
      category: "Ornamental Classical",
      palette: { primary: "#C5A059", secondary: "#F0E6D2", accent: "#5E4828", bg: "#0F0E0C" },
      cornerSize: 145,
      sideMargin: 46,
      coordinates: {
        outerFrame: { x1: 34, y1: 34, x2: 966, y2: 1380 },
        innerFrame: { x1: 50, y1: 50, x2: 950, y2: 1364 },
        safeBox: { x: 90, y: 110, width: 820, height: 1194 }
      },
      render: (w, h, p) => `
        <rect x="34" y="34" width="${w-68}" height="${h-68}" fill="none" stroke="${p.accent}" stroke-width="2"/>
        <rect x="48" y="48" width="${w-96}" height="${h-96}" fill="none" stroke="${p.primary}" stroke-width="1.5"/>
        <!-- Baroque S-Scrolls on Corners -->
        ${[ [50, 50], [w-50, 50], [50, h-50], [w-50, h-50] ].map(([cx, cy], i) => {
          const sx = (i % 2 === 0) ? 1 : -1;
          const sy = (i < 2) ? 1 : -1;
          return `
            <g transform="translate(${cx}, ${cy}) scale(${sx}, ${sy})">
              <path d="M 0 0 C 40 10, 60 50, 40 90 C 20 60, 30 30, 0 0" fill="${p.primary}" opacity="0.3"/>
              <path d="M 0 10 C 60 15, 90 60, 70 120 C 50 80, 50 40, 0 10" fill="none" stroke="${p.primary}" stroke-width="2"/>
              <circle cx="70" cy="120" r="4" fill="${p.secondary}"/>
            </g>
          `;
        }).join('')}
      `
    },

    // 8. BAUHAUS CONSTRUCTIVIST
    bauhaus_constructivist: {
      id: "bauhaus_constructivist",
      name: "Bauhaus Minimal Constructivist",
      category: "Modernist Minimal",
      palette: { primary: "#D9381E", secondary: "#F2C94C", accent: "#2F80ED", bg: "#111111" },
      cornerSize: 100,
      sideMargin: 30,
      coordinates: {
        outerFrame: { x1: 20, y1: 20, x2: 980, y2: 1394 },
        innerFrame: { x1: 32, y1: 32, x2: 968, y2: 1382 },
        safeBox: { x: 70, y: 80, width: 860, height: 1254 }
      },
      render: (w, h, p) => `
        <!-- Bold Asymmetrical Primary Lines -->
        <line x1="20" y1="20" x2="${w-20}" y2="20" stroke="${p.primary}" stroke-width="6"/>
        <line x1="20" y1="20" x2="20" y2="${h-20}" stroke="${p.accent}" stroke-width="6"/>
        <line x1="${w-20}" y1="20" x2="${w-20}" y2="${h-20}" stroke="#FFFFFF" stroke-width="1.5"/>
        <line x1="20" y1="${h-20}" x2="${w-20}" y2="${h-20}" stroke="${p.secondary}" stroke-width="3"/>
        <!-- Modular Corner Blocks -->
        <rect x="17" y="17" width="28" height="28" fill="${p.primary}"/>
        <circle cx="${w-35}" cy="35" r="16" fill="${p.secondary}"/>
        <rect x="17" y="${h-45}" width="28" height="28" fill="${p.accent}"/>
        <polygon points="${w-20},${h-20} ${w-55},${h-20} ${w-20},${h-55}" fill="#FFFFFF"/>
      `
    },

    // 9. ASTROLABE CELESTIAL
    astrolabe_celestial: {
      id: "astrolabe_celestial",
      name: "Astrolabe Celestial Mechanics",
      category: "Celestial Scientific",
      palette: { primary: "#48CAE4", secondary: "#ADE8F4", accent: "#023E8A", bg: "#03071E" },
      cornerSize: 140,
      sideMargin: 42,
      coordinates: {
        outerFrame: { x1: 30, y1: 30, x2: 970, y2: 1384 },
        innerFrame: { x1: 45, y1: 45, x2: 955, y2: 1369 },
        safeBox: { x: 85, y: 105, width: 830, height: 1204 }
      },
      render: (w, h, p) => `
        <rect x="30" y="30" width="${w-60}" height="${h-60}" fill="none" stroke="${p.primary}" stroke-width="1.5" stroke-dasharray="4,6"/>
        <rect x="45" y="45" width="${w-90}" height="${h-90}" fill="none" stroke="${p.accent}" stroke-width="2"/>
        <!-- 4 Corner Celestial Dials -->
        ${[ [45, 45], [w-45, 45], [45, h-45], [w-45, h-45] ].map(([cx, cy]) => `
          <g transform="translate(${cx}, ${cy})">
            <circle cx="0" cy="0" r="38" fill="none" stroke="${p.primary}" stroke-width="1.2"/>
            <circle cx="0" cy="0" r="22" fill="none" stroke="${p.secondary}" stroke-width="0.8" stroke-dasharray="2,3"/>
            <line x1="-38" y1="0" x2="38" y2="0" stroke="${p.primary}" stroke-width="0.8"/>
            <line x1="0" y1="-38" x2="0" y2="38" stroke="${p.primary}" stroke-width="0.8"/>
            <circle cx="0" cy="0" r="3" fill="${p.secondary}"/>
          </g>
        `).join('')}
        <!-- North Star Apex -->
        <polygon points="${w/2},25 ${w/2+8},40 ${w/2+28},42 ${w/2+12},54 ${w/2+18},74 ${w/2},60 ${w/2-18},74 ${w/2-12},54 ${w/2-28},42 ${w/2-8},40" fill="${p.secondary}"/>
      `
    },

    // 10. CLINICAL NEURO-GRID
    clinical_neuro_grid: {
      id: "clinical_neuro_grid",
      name: "Clinical Neuro-Diagnostic Grid",
      category: "Medical High-Tech",
      palette: { primary: "#10B981", secondary: "#34D399", accent: "#064E3B", bg: "#060B0E" },
      cornerSize: 115,
      sideMargin: 36,
      coordinates: {
        outerFrame: { x1: 26, y1: 26, x2: 974, y2: 1388 },
        innerFrame: { x1: 40, y1: 40, x2: 960, y2: 1374 },
        safeBox: { x: 78, y: 90, width: 844, height: 1234 }
      },
      render: (w, h, p) => `
        <rect x="26" y="26" width="${w-52}" height="${h-52}" fill="none" stroke="${p.accent}" stroke-width="2"/>
        <rect x="38" y="38" width="${w-76}" height="${h-76}" fill="none" stroke="${p.primary}" stroke-width="1.2"/>
        <!-- Diagnostic Metric Tick Rails -->
        ${Array.from({length: 15}).map((_, i) => `
          <line x1="26" y1="${120 + i * 80}" x2="33" y2="${120 + i * 80}" stroke="${p.primary}" stroke-width="1.5"/>
          <line x1="${w-33}" y1="${120 + i * 80}" x2="${w-26}" y2="${120 + i * 80}" stroke="${p.primary}" stroke-width="1.5"/>
        `).join('')}
        <!-- Corner ECG/EEG Waveform segments -->
        <polyline points="38,80 50,80 55,60 62,100 68,75 75,80 110,80" fill="none" stroke="${p.secondary}" stroke-width="1.8"/>
        <polyline points="${w-110},80 ${w-75},80 ${w-68},75 ${w-62},100 ${w-55},60 ${w-50},80 ${w-38},80" fill="none" stroke="${p.secondary}" stroke-width="1.8"/>
        <text x="50" y="22" fill="${p.secondary}" font-family="monospace" font-size="9" letter-spacing="1">CALIBRATED_A4_ISO // CLINICAL_SPEC</text>
      `
    },

    // 11. RENAISSANCE PARCHMENT
    renaissance_parchment: {
      id: "renaissance_parchment",
      name: "Renaissance Classical Parchment",
      category: "Antique Classic",
      palette: { primary: "#8C6D3B", secondary: "#D9C5A0", accent: "#4A3B2C", bg: "#161311" },
      cornerSize: 130,
      sideMargin: 44,
      coordinates: {
        outerFrame: { x1: 32, y1: 32, x2: 968, y2: 1382 },
        innerFrame: { x1: 48, y1: 48, x2: 952, y2: 1366 },
        safeBox: { x: 88, y: 104, width: 824, height: 1206 }
      },
      render: (w, h, p) => `
        <rect x="32" y="32" width="${w-64}" height="${h-64}" fill="none" stroke="${p.primary}" stroke-width="3"/>
        <rect x="42" y="42" width="${w-84}" height="${h-84}" fill="none" stroke="${p.accent}" stroke-width="1"/>
        <rect x="48" y="48" width="${w-96}" height="${h-96}" fill="none" stroke="${p.secondary}" stroke-width="1.5"/>
        <!-- Roman Egg and Dart Corner Bosses -->
        ${[ [48, 48], [w-48, 48], [48, h-48], [w-48, h-48] ].map(([cx, cy]) => `
          <g transform="translate(${cx}, ${cy})">
            <rect x="-18" y="-18" width="36" height="36" fill="${p.accent}" stroke="${p.primary}" stroke-width="1.5"/>
            <circle cx="0" cy="0" r="10" fill="${p.secondary}"/>
            <circle cx="0" cy="0" r="4" fill="${p.primary}"/>
          </g>
        `).join('')}
      `
    },

    // 12. VICTORIAN STEAMPUNK GEARWORK
    victorian_steampunk: {
      id: "victorian_steampunk",
      name: "Victorian Steampunk Brass",
      category: "Retro Mechanical",
      palette: { primary: "#B87333", secondary: "#E5A65E", accent: "#5C3818", bg: "#120E0A" },
      cornerSize: 135,
      sideMargin: 40,
      coordinates: {
        outerFrame: { x1: 28, y1: 28, x2: 972, y2: 1386 },
        innerFrame: { x1: 44, y1: 44, x2: 956, y2: 1370 },
        safeBox: { x: 84, y: 100, width: 832, height: 1214 }
      },
      render: (w, h, p) => `
        <rect x="28" y="28" width="${w-56}" height="${h-56}" fill="none" stroke="${p.primary}" stroke-width="3"/>
        <rect x="42" y="42" width="${w-84}" height="${h-84}" fill="none" stroke="${p.accent}" stroke-width="1.5"/>
        <!-- Brass Rivets Along Perimeter -->
        ${Array.from({length: 12}).map((_, i) => `
          <circle cx="${100 + i * ((w-200)/11)}" cy="35" r="3.5" fill="${p.secondary}" stroke="${p.accent}" stroke-width="1"/>
          <circle cx="${100 + i * ((w-200)/11)}" cy="${h-35}" r="3.5" fill="${p.secondary}" stroke="${p.accent}" stroke-width="1"/>
        `).join('')}
        <!-- Corner Cogwheels -->
        ${[ [44, 44], [w-44, 44], [44, h-44], [w-44, h-44] ].map(([cx, cy]) => `
          <g transform="translate(${cx}, ${cy})">
            <circle cx="0" cy="0" r="28" fill="none" stroke="${p.primary}" stroke-width="2.5" stroke-dasharray="6,4"/>
            <circle cx="0" cy="0" r="16" fill="${p.accent}" stroke="${p.secondary}" stroke-width="1.5"/>
            <circle cx="0" cy="0" r="5" fill="${p.secondary}"/>
          </g>
        `).join('')}
      `
    },

    // 13. ZEN SUMI CALLIGRAPHIC
    zen_sumi: {
      id: "zen_sumi",
      name: "Zen Sumi Calligraphic Ink",
      category: "Eastern Minimal",
      palette: { primary: "#E2E8F0", secondary: "#DC2626", accent: "#475569", bg: "#09090B" },
      cornerSize: 120,
      sideMargin: 35,
      coordinates: {
        outerFrame: { x1: 25, y1: 25, x2: 975, y2: 1389 },
        innerFrame: { x1: 38, y1: 38, x2: 962, y2: 1376 },
        safeBox: { x: 75, y: 85, width: 850, height: 1244 }
      },
      render: (w, h, p) => `
        <!-- Organic Brush Border -->
        <path d="M 30 50 Q 35 25 70 30 L ${w-70} 26 Q ${w-30} 24 ${w-30} 60 L ${w-28} ${h-60} Q ${w-32} ${h-25} ${w-65} ${h-28} L 65 ${h-30} Q 28 ${h-32} 30 ${h-65} Z" fill="none" stroke="${p.primary}" stroke-width="2.2" opacity="0.85"/>
        <line x1="42" y1="42" x2="${w-42}" y2="42" stroke="${p.accent}" stroke-width="0.8" opacity="0.5"/>
        <line x1="42" y1="${h-42}" x2="${w-42}" y2="${h-42}" stroke="${p.accent}" stroke-width="0.8" opacity="0.5"/>
        <!-- Red Hanko Vermilion Stamp (Bottom Right) -->
        <g transform="translate(${w-80}, ${h-80})">
          <rect x="0" y="0" width="36" height="36" fill="${p.secondary}" opacity="0.85" rx="3"/>
          <circle cx="18" cy="18" r="12" fill="none" stroke="#FFFFFF" stroke-width="1.8"/>
          <text x="18" y="22" fill="#FFFFFF" font-size="12" font-family="serif" text-anchor="middle" font-weight="bold">悟</text>
        </g>
      `
    },

    // 14. ISLAMIC GIRIH STRAPWORK
    islamic_girih: {
      id: "islamic_girih",
      name: "Islamic Girih Geometric Strapwork",
      category: "Geometric Sacred",
      palette: { primary: "#00A896", secondary: "#F4A261", accent: "#028090", bg: "#081214" },
      cornerSize: 145,
      sideMargin: 45,
      coordinates: {
        outerFrame: { x1: 30, y1: 30, x2: 970, y2: 1384 },
        innerFrame: { x1: 48, y1: 48, x2: 952, y2: 1366 },
        safeBox: { x: 88, y: 105, width: 824, height: 1204 }
      },
      render: (w, h, p) => `
        <rect x="30" y="30" width="${w-60}" height="${h-60}" fill="none" stroke="${p.primary}" stroke-width="2"/>
        <rect x="46" y="46" width="${w-92}" height="${h-92}" fill="none" stroke="${p.secondary}" stroke-width="1.5"/>
        <!-- 8-Pointed Star Interlace Corners -->
        ${[ [46, 46], [w-46, 46], [46, h-46], [w-46, h-46] ].map(([cx, cy]) => `
          <g transform="translate(${cx}, ${cy})">
            <rect x="-22" y="-22" width="44" height="44" fill="none" stroke="${p.secondary}" stroke-width="1.5"/>
            <rect x="-22" y="-22" width="44" height="44" fill="none" stroke="${p.primary}" stroke-width="1.5" transform="rotate(45)"/>
            <circle cx="0" cy="0" r="8" fill="${p.secondary}"/>
          </g>
        `).join('')}
      `
    },

    // 15. MAYAN STELE FRETWORK
    mayan_stele: {
      id: "mayan_stele",
      name: "Mayan Stele Monumental",
      category: "Mesoamerican Archaic",
      palette: { primary: "#E76F51", secondary: "#E9C46A", accent: "#264653", bg: "#130F0D" },
      cornerSize: 130,
      sideMargin: 42,
      coordinates: {
        outerFrame: { x1: 28, y1: 28, x2: 972, y2: 1386 },
        innerFrame: { x1: 44, y1: 44, x2: 956, y2: 1370 },
        safeBox: { x: 84, y: 100, width: 832, height: 1214 }
      },
      render: (w, h, p) => `
        <rect x="28" y="28" width="${w-56}" height="${h-56}" fill="none" stroke="${p.primary}" stroke-width="3"/>
        <!-- Step-Pyramid Fret Corners -->
        <g fill="${p.secondary}">
          <polygon points="28,28 78,28 78,44 54,44 54,68 28,68"/>
          <polygon points="${w-28},28 ${w-78},28 ${w-78},44 ${w-54},44 ${w-54},68 ${w-28},68"/>
          <polygon points="28,${h-28} 78,${h-28} 78,${h-44} 54,${h-44} 54,${h-68} 28,${h-68}"/>
          <polygon points="${w-28},${h-28} ${w-78},${h-28} ${w-78},${h-44} ${w-54},${h-44} ${w-54},${h-68} ${w-28},${h-68}"/>
        </g>
        <rect x="44" y="44" width="${w-88}" height="${h-88}" fill="none" stroke="${p.accent}" stroke-width="1.5"/>
      `
    },

    // 16. NORDIC RUNIC BAND
    nordic_runic: {
      id: "nordic_runic",
      name: "Nordic Elder Futhark Band",
      category: "Mythological Northern",
      palette: { primary: "#94A3B8", secondary: "#38BDF8", accent: "#1E293B", bg: "#080C14" },
      cornerSize: 125,
      sideMargin: 38,
      coordinates: {
        outerFrame: { x1: 26, y1: 26, x2: 974, y2: 1388 },
        innerFrame: { x1: 42, y1: 42, x2: 958, y2: 1372 },
        safeBox: { x: 80, y: 95, width: 840, height: 1224 }
      },
      render: (w, h, p) => `
        <rect x="26" y="26" width="${w-52}" height="${h-52}" fill="none" stroke="${p.primary}" stroke-width="2.5"/>
        <rect x="40" y="40" width="${w-80}" height="${h-80}" fill="none" stroke="${p.accent}" stroke-width="1"/>
        <!-- Runic Staves Across Top & Bottom -->
        <g fill="${p.secondary}" font-family="monospace" font-size="11" letter-spacing="12">
          <text x="65" y="36">ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ ᚷ ᚹ ᚺ ᚾ ᛁ ᛃ ᛇ ᛈ ᛉ ᛋ ᛏ ᛒ ᛖ ᛗ ᛚ ᛜ ᛟ ᛞ</text>
        </g>
        <!-- Nordic Dragon Terminal Knot Corners -->
        <circle cx="42" cy="42" r="14" fill="none" stroke="${p.secondary}" stroke-width="2"/>
        <circle cx="${w-42}" cy="42" r="14" fill="none" stroke="${p.secondary}" stroke-width="2"/>
        <circle cx="42" cy="${h-42}" r="14" fill="none" stroke="${p.secondary}" stroke-width="2"/>
        <circle cx="${w-42}" cy="${h-42}" r="14" fill="none" stroke="${p.secondary}" stroke-width="2"/>
      `
    },

    // 17. ART NOUVEAU FLORA
    art_nouveau: {
      id: "art_nouveau",
      name: "Art Nouveau Whiplash Flora",
      category: "Organic Flowing",
      palette: { primary: "#829672", secondary: "#D6CCA9", accent: "#4E5D44", bg: "#0D110D" },
      cornerSize: 140,
      sideMargin: 44,
      coordinates: {
        outerFrame: { x1: 30, y1: 30, x2: 970, y2: 1384 },
        innerFrame: { x1: 46, y1: 46, x2: 954, y2: 1368 },
        safeBox: { x: 86, y: 104, width: 828, height: 1206 }
      },
      render: (w, h, p) => `
        <rect x="30" y="30" width="${w-60}" height="${h-60}" fill="none" stroke="${p.primary}" stroke-width="1.8"/>
        <!-- Whiplash Asymmetrical S-Curves -->
        <path d="M 30 140 C 60 70, 70 30, 140 30 C 90 60, 60 90, 30 140 Z" fill="${p.secondary}" opacity="0.4"/>
        <path d="M 30 140 C 70 90, 90 70, 140 30" fill="none" stroke="${p.secondary}" stroke-width="2.5"/>
        <path d="M ${w-30} 140 C ${w-70} 90, ${w-90} 70, ${w-140} 30" fill="none" stroke="${p.secondary}" stroke-width="2.5"/>
        <path d="M 30 ${h-140} C 70 ${h-90}, 90 ${h-70}, 140 ${h-30}" fill="none" stroke="${p.secondary}" stroke-width="2.5"/>
        <path d="M ${w-30} ${h-140} C ${w-70} ${h-90}, ${w-90} ${h-70}, ${w-140} ${h-30}" fill="none" stroke="${p.secondary}" stroke-width="2.5"/>
      `
    },

    // 18. QUANTUM LATTICE
    quantum_lattice: {
      id: "quantum_lattice",
      name: "Quantum Hexagonal Lattice",
      category: "Quantum Physics",
      palette: { primary: "#A855F7", secondary: "#EC4899", accent: "#3B0764", bg: "#090514" },
      cornerSize: 120,
      sideMargin: 36,
      coordinates: {
        outerFrame: { x1: 26, y1: 26, x2: 974, y2: 1388 },
        innerFrame: { x1: 40, y1: 40, x2: 960, y2: 1374 },
        safeBox: { x: 78, y: 90, width: 844, height: 1234 }
      },
      render: (w, h, p) => `
        <rect x="26" y="26" width="${w-52}" height="${h-52}" fill="none" stroke="${p.primary}" stroke-width="2"/>
        <rect x="38" y="38" width="${w-76}" height="${h-76}" fill="none" stroke="${p.secondary}" stroke-width="1" stroke-dasharray="6,4"/>
        <!-- Hexagonal Carbon/Quantum Corner Rings -->
        ${[ [40, 40], [w-40, 40], [40, h-40], [w-40, h-40] ].map(([cx, cy]) => `
          <g transform="translate(${cx}, ${cy})">
            <polygon points="0,-24 20,-12 20,12 0,24 -20,12 -20,-12" fill="none" stroke="${p.primary}" stroke-width="2"/>
            <circle cx="0" cy="0" r="6" fill="${p.secondary}"/>
          </g>
        `).join('')}
      `
    },

    // 19. ALCHEMICAL TRANSMUTATION
    alchemical_ouroboros: {
      id: "alchemical_ouroboros",
      name: "Alchemical Transmutation Seal",
      category: "Occult Hermetic",
      palette: { primary: "#EAB308", secondary: "#FACC15", accent: "#713F12", bg: "#0A0A08" },
      cornerSize: 140,
      sideMargin: 44,
      coordinates: {
        outerFrame: { x1: 30, y1: 30, x2: 970, y2: 1384 },
        innerFrame: { x1: 48, y1: 48, x2: 952, y2: 1366 },
        safeBox: { x: 88, y: 104, width: 824, height: 1206 }
      },
      render: (w, h, p) => `
        <rect x="30" y="30" width="${w-60}" height="${h-60}" fill="none" stroke="${p.primary}" stroke-width="2.5"/>
        <rect x="46" y="46" width="${w-92}" height="${h-92}" fill="none" stroke="${p.accent}" stroke-width="1.2"/>
        <!-- Alchemical Triangles & Ouroboros -->
        ${[ [48, 48], [w-48, 48], [48, h-48], [w-48, h-48] ].map(([cx, cy]) => `
          <g transform="translate(${cx}, ${cy})">
            <circle cx="0" cy="0" r="26" fill="none" stroke="${p.primary}" stroke-width="1.8"/>
            <polygon points="0,-22 19,11 -19,11" fill="none" stroke="${p.secondary}" stroke-width="1.2"/>
            <circle cx="0" cy="0" r="4" fill="${p.secondary}"/>
          </g>
        `).join('')}
      `
    },

    // 20. MINIMALIST HAUTE COUTURE
    minimalist_haute_couture: {
      id: "minimalist_haute_couture",
      name: "Minimalist Haute Couture Hairline",
      category: "Modern High-Fashion",
      palette: { primary: "#FFFFFF", secondary: "#CCCCCC", accent: "#666666", bg: "#050505" },
      cornerSize: 90,
      sideMargin: 28,
      coordinates: {
        outerFrame: { x1: 20, y1: 20, x2: 980, y2: 1394 },
        innerFrame: { x1: 30, y1: 30, x2: 970, y2: 1384 },
        safeBox: { x: 65, y: 75, width: 870, height: 1264 }
      },
      render: (w, h, p) => `
        <rect x="20" y="20" width="${w-40}" height="${h-40}" fill="none" stroke="${p.primary}" stroke-width="0.8"/>
        <rect x="28" y="28" width="${w-56}" height="${h-56}" fill="none" stroke="${p.accent}" stroke-width="0.4"/>
        <!-- Precision Corner Crosshairs -->
        <g stroke="${p.primary}" stroke-width="0.75">
          <line x1="12" y1="20" x2="28" y2="20"/><line x1="20" y1="12" x2="20" y2="28"/>
          <line x1="${w-28}" y1="20" x2="${w-12}" y2="20"/><line x1="${w-20}" y1="12" x2="${w-20}" y2="28"/>
          <line x1="12" y1="${h-20}" x2="28" y2="${h-20}"/><line x1="20" y1="${h-28}" x2="20" y2="${h-12}"/>
          <line x1="${w-28}" y1="${h-20}" x2="${w-12}" y2="${h-20}"/><line x1="${w-20}" y1="${h-28}" x2="${w-20}" y2="${h-12}"/>
        </g>
        <!-- Fine Editorial Page Foliation Indicator -->
        <text x="${w/2}" y="15" fill="${p.secondary}" font-family="serif" font-size="7.5" letter-spacing="3" text-anchor="middle">FOLIO SPECIFICATION // A4 210 × 297 MM</text>
      `
    }
  };

  // ==================== PROTOCOL ENGINE API ====================
  const PdfBorderProtocol = {
    A4_SPECS,
    BORDER_TEMPLATES,

    getTemplateList() {
      return Object.values(BORDER_TEMPLATES).map(t => ({
        id: t.id,
        name: t.name,
        category: t.category,
        coordinates: t.coordinates
      }));
    },

    getTemplate(id) {
      return BORDER_TEMPLATES[id] || BORDER_TEMPLATES.arcane_willow;
    },

    /**
     * Generate Scalable Vector Graphic (SVG) for any of the 20 templates
     * @param {string} id - Border ID
     * @param {string} orientation - 'portrait' or 'landscape'
     * @param {object} customPalette - Override colors if desired
     */
    generateSvg(id = 'arcane_willow', orientation = 'portrait', customPalette = null) {
      const spec = A4_SPECS[orientation] || A4_SPECS.portrait;
      const tpl = BORDER_TEMPLATES[id] || BORDER_TEMPLATES.arcane_willow;
      const palette = customPalette ? { ...tpl.palette, ...customPalette } : tpl.palette;

      const isLandscape = orientation === 'landscape';
      const w = isLandscape ? 1414 : 1000;
      const h = isLandscape ? 1000 : 1414;

      const innerSvg = tpl.render(w, h, palette);

      return `
        <svg xmlns="http://www.w3.org/2000/svg" 
             viewBox="0 0 ${w} ${h}" 
             width="100%" 
             height="100%" 
             preserveAspectRatio="none"
             style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1;"
             data-border-id="${tpl.id}"
             data-orientation="${orientation}">
          <defs>
            <linearGradient id="goldGrad_${tpl.id}" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="${palette.primary}"/>
              <stop offset="50%" stop-color="${palette.secondary}"/>
              <stop offset="100%" stop-color="${palette.accent}"/>
            </linearGradient>
          </defs>
          ${innerSvg}
        </svg>
      `.trim();
    },

    /**
     * Compute exact safe text bounding box in CSS or PDF units
     */
    getSafeContentBox(id, orientation = 'portrait', unit = 'px') {
      const spec = A4_SPECS[orientation] || A4_SPECS.portrait;
      const tpl = BORDER_TEMPLATES[id] || BORDER_TEMPLATES.arcane_willow;
      const coords = tpl.coordinates.safeBox;

      if (unit === 'mm') {
        const scaleX = spec.widthMm / (orientation === 'landscape' ? 1414 : 1000);
        const scaleY = spec.heightMm / (orientation === 'landscape' ? 1000 : 1414);
        return {
          leftMm: (coords.x * scaleX).toFixed(2),
          topMm: (coords.y * scaleY).toFixed(2),
          widthMm: (coords.width * scaleX).toFixed(2),
          heightMm: (coords.height * scaleY).toFixed(2)
        };
      }

      return coords;
    }
  };

  // Universal export
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = PdfBorderProtocol;
  }
  root.PdfBorderProtocol = PdfBorderProtocol;

})(typeof window !== 'undefined' ? window : this);
