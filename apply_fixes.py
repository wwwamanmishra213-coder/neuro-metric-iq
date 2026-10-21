import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ======================================================================
# 1. NEW HTML FOR screenNeuroplasticity
# ======================================================================
new_nback_html = '''<!-- ==================== SCREEN 5: NEUROPLASTICITY TRACKER (DUAL N-BACK) ==================== -->
    <section id="screenNeuroplasticity" class="hidden max-w-4xl mx-auto w-full space-y-6 px-3 sm:px-6">
      <div class="holo-card rounded-3xl p-6 sm:p-8 space-y-6">
        <div class="flex items-center justify-between border-b border-emerald-500/20 pb-3">
          <div>
            <span class="text-xs font-mono text-emerald-400 uppercase tracking-widest font-semibold flex items-center space-x-2">
              <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400/50"></span>
              <span>Neuroplasticity Tracker (Dual N-Back)</span>
            </span>
            <p class="text-xs text-slate-300 mt-0.5">Jaeggi PNAS Working Memory Model &bull; N=2 Continuous Multimodal Updating</p>
          </div>
          <div class="flex items-center space-x-2.5">
            <span id="nbackStepBadge" class="text-xs font-mono text-emerald-300 font-bold bg-emerald-950/60 px-3 py-1.5 rounded-xl border border-emerald-500/30">
              Step 1 of 40
            </span>
            <button onclick="AssessmentController.exitToMenu()" class="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-red-400 text-xs font-mono text-red-400 hover:text-red-300 transition touch-manipulation">Exit</button>
          </div>
        </div>

        <!-- Dynamic Status Prompt & Pacing Timer -->
        <div class="p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-emerald-200 text-xs font-mono flex items-center justify-between">
          <span id="nbackInstructionText">ENCODING PHASE: Memorize spatial position & letter (Step 1 of 2)... Auto-advancing</span>
          <span id="nbackTimer" class="font-bold text-white text-sm bg-slate-900/80 px-2.5 py-0.5 rounded-lg border border-emerald-500/30">2.5s</span>
        </div>

        <!-- 3x3 Spatial Grid with Center Letter Token -->
        <div class="p-6 bg-slate-950/70 rounded-2xl border border-emerald-500/20 flex flex-col items-center justify-center">
          <div id="nbackGrid" class="grid grid-cols-3 gap-3 w-64 h-64 mx-auto p-2">
            <!-- 9 Spatial Cells -->
          </div>
          <div class="mt-4 px-5 py-2 rounded-xl bg-slate-900 border border-emerald-500/30 text-center">
            <span class="text-[10px] font-mono text-slate-400 uppercase tracking-widest block">Stream Auditory/Visual Token</span>
            <span id="nbackLetterToken" class="text-2xl font-mono font-bold text-emerald-300">A</span>
          </div>
        </div>

        <!-- Response Area: State-Dependent -->
        <!-- 1. Encoding-Only Buffer Panel (Steps 1 to N: Match Buttons Hidden) -->
        <div id="nbackEncodingPanel" class="flex flex-col items-center justify-center p-3 space-y-2">
          <button id="nbackBtnContinue" onclick="NBackEngine.advanceEncoding()" class="w-full sm:w-auto px-8 py-3 rounded-xl bg-gradient-to-r from-emerald-400 to-cyan-500 hover:from-emerald-300 text-black font-mono text-xs font-bold transition holo-glow-cyan touch-manipulation flex items-center justify-center space-x-2 active:scale-95 cursor-pointer">
            <span>Next / Continue (Space)</span>
            <span id="nbackEncodingTimerPill" class="px-2 py-0.5 rounded bg-black/30 text-white font-mono text-[10px]">2.5s</span>
          </button>
          <span class="text-[10px] font-mono text-slate-400">Encoding trial auto-advances in 2.5s</span>
        </div>

        <!-- 2. Active Comparison Response Panel (Steps > N: Revealed for Evaluation) -->
        <div id="nbackResponsePanel" class="hidden grid grid-cols-2 sm:grid-cols-4 gap-2.5">
          <button id="nbackBtnPos" onclick="NBackEngine.recordResponse('position')" class="py-3 px-2 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 active:scale-95 border border-emerald-500/40 text-emerald-300 font-mono text-xs font-bold transition touch-manipulation cursor-pointer flex flex-col items-center justify-center space-y-0.5">
            <span>Position Match</span>
            <span class="text-[9px] text-emerald-400/80 font-normal">Key: [A]</span>
          </button>
          <button id="nbackBtnLet" onclick="NBackEngine.recordResponse('letter')" class="py-3 px-2 rounded-xl bg-cyan-500/20 hover:bg-cyan-500/30 active:scale-95 border border-cyan-500/40 text-cyan-300 font-mono text-xs font-bold transition touch-manipulation cursor-pointer flex flex-col items-center justify-center space-y-0.5">
            <span>Letter Match</span>
            <span class="text-[9px] text-cyan-400/80 font-normal">Key: [L]</span>
          </button>
          <button id="nbackBtnBoth" onclick="NBackEngine.recordResponse('both')" class="py-3 px-2 rounded-xl bg-purple-500/20 hover:bg-purple-500/30 active:scale-95 border border-purple-500/40 text-purple-300 font-mono text-xs font-bold transition touch-manipulation cursor-pointer flex flex-col items-center justify-center space-y-0.5">
            <span>Dual Match</span>
            <span class="text-[9px] text-purple-400/80 font-normal">Key: [Space]</span>
          </button>
          <button id="nbackBtnNone" onclick="NBackEngine.recordResponse('none')" class="py-3 px-2 rounded-xl bg-slate-800 hover:bg-slate-750 active:scale-95 border border-slate-750 text-slate-300 font-mono text-xs font-bold transition touch-manipulation cursor-pointer flex flex-col items-center justify-center space-y-0.5">
            <span>No Match</span>
            <span class="text-[9px] text-slate-400/80 font-normal">Key: [N] / Pass</span>
          </button>
        </div>

        <div class="flex items-center justify-between text-xs font-mono text-slate-400 pt-2 border-t border-emerald-500/20">
          <span id="nbackScoreTelemetry">Hits: 0 &bull; Misses: 0</span>
          <span>Jaeggi PNAS Continuous Updating Loop</span>
        </div>
      </div>
    </section>'''

html = re.sub(
    r'<!-- =+ SCREEN 5: NEUROPLASTICITY TRACKER \(DUAL N-BACK\) =+ -->\s*<section id="screenNeuroplasticity".*?</section>',
    new_nback_html,
    html,
    flags=re.DOTALL
)

# ======================================================================
# 2. NEW JAVASCRIPT FOR MemoryTestEngine & DMTS (Robust Matrix Generator & Visual Renderer)
# ======================================================================
new_mem_js = '''// ==================== 1. MEMORY RECOGNITION (DMTS) ENGINE ====================
    window.MemoryTestEngine = {
      currentTrial: 0,
      totalTrials: 40,
      trialStartTime: 0,
      latencies: [],
      correctCount: 0,
      timerId: null,
      countdownInterval: null,
      currentTrialData: null,

      start() {
        this.currentTrial = 0;
        this.correctCount = 0;
        this.latencies = [];
        this.clearTimers();
        showScreen('screenMemory');
        this.runTrial(0);
      },

      clearTimers() {
        if (this.timerId) {
          clearTimeout(this.timerId);
          this.timerId = null;
        }
        if (this.countdownInterval) {
          clearInterval(this.countdownInterval);
          this.countdownInterval = null;
        }
      },

      // Procedural generation of serializable 4x4 matrix configurations + 3 distinct mutated distractors
      generateTrial(trialIndex) {
        const palette = ['#22d3ee', '#818cf8', '#34d399', '#fbbf24', '#f43f5e', '#c084fc', '#38bdf8', '#a855f7'];

        // Seeded pseudo-random generator for 100% reproducible trial progression
        let seed = (trialIndex + 1) * 9301 + 49297;
        const rnd = () => {
          seed = (seed * 9301 + 49297) % 233280;
          return seed / 233280;
        };

        const available = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];
        for (let i = available.length - 1; i > 0; i--) {
          const j = Math.floor(rnd() * (i + 1));
          [available[i], available[j]] = [available[j], available[i]];
        }

        const numActive = 5 + (trialIndex % 2); // 5 or 6 illuminated cells
        const targetActive = available.slice(0, numActive).sort((a, b) => a - b);
        const inactive = available.slice(numActive);

        // Assign colors
        const targetColors = {};
        targetActive.forEach((idx, cIdx) => {
          targetColors[idx] = palette[(trialIndex * 2 + cIdx) % palette.length];
        });

        const targetData = {
          size: 4,
          active: targetActive,
          colors: targetColors
        };

        // Distractor 1: Swap 1 active cell with 1 inactive cell (Single feature mutation)
        const d1Active = [...targetActive];
        const swapOut1 = d1Active[0];
        const swapIn1 = inactive[0];
        d1Active[0] = swapIn1;
        d1Active.sort((a, b) => a - b);
        const d1Colors = { ...targetColors };
        delete d1Colors[swapOut1];
        d1Colors[swapIn1] = palette[(trialIndex + 2) % palette.length];
        const d1Data = { size: 4, active: d1Active, colors: d1Colors };

        // Distractor 2: Swap 2 active cells with 2 inactive cells (Double feature mutation)
        const d2Active = [...targetActive];
        const swapOut2a = d2Active[1] !== undefined ? d2Active[1] : d2Active[0];
        const swapOut2b = d2Active[2] !== undefined ? d2Active[2] : d2Active[0];
        const swapIn2a = inactive[1] !== undefined ? inactive[1] : inactive[0];
        const swapIn2b = inactive[2] !== undefined ? inactive[2] : inactive[0];
        const d2Set = new Set(d2Active);
        d2Set.delete(swapOut2a);
        d2Set.delete(swapOut2b);
        d2Set.add(swapIn2a);
        d2Set.add(swapIn2b);
        const d2ActiveArr = Array.from(d2Set).sort((a, b) => a - b);
        const d2Colors = { ...targetColors };
        delete d2Colors[swapOut2a];
        delete d2Colors[swapOut2b];
        d2Colors[swapIn2a] = palette[(trialIndex + 3) % palette.length];
        d2Colors[swapIn2b] = palette[(trialIndex + 4) % palette.length];
        const d2Data = { size: 4, active: d2ActiveArr, colors: d2Colors };

        // Distractor 3: Rotated coordinates 90-degrees (Structural rotation mutation)
        // 90-degree CW rotation in 4x4: (r, c) -> (c, 3 - r) => new_idx = c * 4 + (3 - r)
        const d3Active = targetActive.map(idx => {
          const r = Math.floor(idx / 4);
          const c = idx % 4;
          return c * 4 + (3 - r);
        }).sort((a, b) => a - b);
        const d3Colors = {};
        d3Active.forEach((idx, cIdx) => {
          d3Colors[idx] = palette[(trialIndex + cIdx + 1) % palette.length];
        });
        const d3Data = { size: 4, active: d3Active, colors: d3Colors };

        // Bundle into 4 options and shuffle deterministically
        const rawOptions = [
          { isCorrect: true, matrixData: targetData },
          { isCorrect: false, matrixData: d1Data },
          { isCorrect: false, matrixData: d2Data },
          { isCorrect: false, matrixData: d3Data }
        ];

        for (let i = rawOptions.length - 1; i > 0; i--) {
          const j = Math.floor(rnd() * (i + 1));
          [rawOptions[i], rawOptions[j]] = [rawOptions[j], rawOptions[i]];
        }

        return {
          id: trialIndex + 1,
          targetData: targetData,
          options: rawOptions
        };
      },

      // Render crisp, high-contrast inline SVG matrix
      renderMatrixSVG(matrixData, width = 84, height = 84) {
        if (!matrixData) return '';
        const size = matrixData.size || 4;
        const activeSet = new Set(matrixData.active || []);
        const colors = matrixData.colors || {};

        let rects = '';
        const cellSize = 19;
        const gap = 4;
        const offset = 6;

        for (let r = 0; r < size; r++) {
          for (let c = 0; c < size; c++) {
            const idx = r * size + c;
            const x = offset + c * (cellSize + gap);
            const y = offset + r * (cellSize + gap);
            const isActive = activeSet.has(idx);

            if (isActive) {
              const color = colors[idx] || '#22d3ee';
              rects += `
                <rect x="${x}" y="${y}" width="${cellSize}" height="${cellSize}" rx="4" fill="${color}" stroke="#ffffff" stroke-width="1.5"/>
                <circle cx="${x + cellSize / 2}" cy="${y + cellSize / 2}" r="3" fill="#ffffff" opacity="0.9"/>
              `;
            } else {
              rects += `
                <rect x="${x}" y="${y}" width="${cellSize}" height="${cellSize}" rx="4" fill="#090d16" stroke="#1e293b" stroke-width="1"/>
              `;
            }
          }
        }

        return `
          <svg width="${width}" height="${height}" viewBox="0 0 100 100" class="rounded-xl border border-slate-700/80 bg-slate-950 p-1 shadow-inner inline-block">
            <rect x="2" y="2" width="96" height="96" rx="8" fill="#040711" stroke="#334155" stroke-width="1"/>
            ${rects}
          </svg>
        `;
      },

      // Render high-frequency visual noise mask buffer
      renderMaskSVG(width = 96, height = 96) {
        let rects = '';
        const noiseColors = ['#22d3ee', '#818cf8', '#34d399', '#f43f5e', '#fbbf24', '#a855f7'];
        const cellSize = 19;
        const gap = 4;
        const offset = 6;

        for (let r = 0; r < 4; r++) {
          for (let c = 0; c < 4; c++) {
            const x = offset + c * (cellSize + gap);
            const y = offset + r * (cellSize + gap);
            const isFilled = ((r + c) % 2 === 0);
            const color = noiseColors[(r * 4 + c) % noiseColors.length];
            if (isFilled) {
              rects += `<rect x="${x}" y="${y}" width="${cellSize}" height="${cellSize}" rx="4" fill="${color}" stroke="#ffffff" stroke-width="1" opacity="0.85"/>`;
            } else {
              rects += `<rect x="${x}" y="${y}" width="${cellSize}" height="${cellSize}" rx="4" fill="#090d16" stroke="#475569" stroke-width="1"/>`;
            }
          }
        }

        return `
          <svg width="${width}" height="${height}" viewBox="0 0 100 100" class="rounded-xl border-2 border-dashed border-cyan-400 bg-slate-950 p-1 animate-pulse shadow-lg shadow-cyan-950 inline-block">
            <rect x="2" y="2" width="96" height="96" rx="8" fill="#040711"/>
            ${rects}
          </svg>
        `;
      },

      runTrial(index) {
        this.clearTimers();

        if (index >= this.totalTrials) {
          this.finish();
          return;
        }

        this.currentTrial = index;
        const trial = this.generateTrial(index);
        this.currentTrialData = trial;

        document.getElementById('memoryTrialBadge').textContent = `Trial ${index + 1} of ${this.totalTrials}`;
        document.getElementById('memoryInstructionText').textContent = 'Phase 1: Memorize target matrix configuration (2.5s)...';

        const pct = Math.round(((index) / this.totalTrials) * 100);
        const pb1 = document.getElementById('memoryProgressBar');
        if (pb1) pb1.style.width = `${pct}%`;

        const displayArea = document.getElementById('memoryDisplayArea');
        const grid = document.getElementById('memoryProbeGrid');
        if (grid) {
          grid.classList.add('hidden');
          grid.innerHTML = '';
        }
        if (displayArea) {
          displayArea.innerHTML = `
            <div class="flex flex-col items-center justify-center p-2">
              ${this.renderMatrixSVG(trial.targetData, 100, 100)}
            </div>
          `;
        }

        // Phase 1 timer countdown
        let phase1Left = 2500;
        const timerEl = document.getElementById('memoryPhaseTimer');
        if (timerEl) timerEl.textContent = '2.5s';

        this.countdownInterval = setInterval(() => {
          phase1Left -= 100;
          if (timerEl) timerEl.textContent = Math.max(0, (phase1Left / 1000)).toFixed(1) + 's';
          if (phase1Left <= 0) {
            this.clearTimers();
            this.enterRetentionDelay(trial);
          }
        }, 100);
      },

      // Phase 2: Retention Interval (Visual Mask Buffer)
      enterRetentionDelay(trial) {
        this.clearTimers();
        document.getElementById('memoryInstructionText').textContent = 'Phase 2: Retention interval (1.5s Visual Mask Buffer)...';
        const displayArea = document.getElementById('memoryDisplayArea');
        if (displayArea) {
          displayArea.innerHTML = `
            <div class="flex flex-col items-center justify-center space-y-1.5 p-1">
              ${this.renderMaskSVG(88, 88)}
              <span class="text-[10px] font-mono text-cyan-300 font-bold uppercase tracking-widest flex items-center space-x-1.5">
                <span class="inline-block w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
                <span>MASK BUFFER ACTIVE</span>
              </span>
            </div>
          `;
        }

        let phase2Left = 1500;
        const timerEl = document.getElementById('memoryPhaseTimer');
        if (timerEl) timerEl.textContent = '1.5s';

        this.countdownInterval = setInterval(() => {
          phase2Left -= 100;
          if (timerEl) timerEl.textContent = Math.max(0, (phase2Left / 1000)).toFixed(1) + 's';
          if (phase2Left <= 0) {
            this.clearTimers();
            this.presentProbe(trial);
          }
        }, 100);
      },

      // Phase 3: Discrimination Phase with Visual Matrix Injection inside all 4 choice buttons
      presentProbe(trial) {
        this.clearTimers();
        const displayArea = document.getElementById('memoryDisplayArea');
        if (displayArea) {
          displayArea.innerHTML = `
            <div class="flex items-center space-x-2 text-cyan-400 font-mono text-xs font-bold uppercase tracking-wider py-1">
              <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
              <span>DISCRIMINATION PHASE: Select matching pattern below</span>
            </div>
          `;
        }
        const inst = document.getElementById('memoryInstructionText');
        if (inst) {
          inst.innerHTML = 'Phase 3: Select matching target matrix from memory &mdash; <strong class="text-white">Click choice or press keys [1]-[4] / [A]-[D]</strong>:';
        }
        const timerEl = document.getElementById('memoryPhaseTimer');
        if (timerEl) timerEl.textContent = 'Active';

        const grid = document.getElementById('memoryProbeGrid');
        if (grid) {
          grid.innerHTML = '';
          grid.classList.remove('hidden');

          this.trialStartTime = Date.now();
          const letters = ['A', 'B', 'C', 'D'];

          trial.options.forEach((opt, idx) => {
            const letter = letters[idx];
            const num = idx + 1;
            const div = document.createElement('div');
            div.className = 'matrix-holo-tile rounded-2xl p-2.5 sm:p-3 flex flex-col items-center justify-between relative cursor-pointer active:scale-95 hover:border-indigo-400 transition-all touch-manipulation group bg-slate-900/90 border border-slate-700/80 hover:shadow-lg hover:shadow-indigo-950/60';
            div.setAttribute('data-choice-idx', idx);
            div.innerHTML = `
              <div class="flex items-center justify-between w-full mb-1">
                <span class="px-2.5 py-0.5 rounded-lg bg-indigo-500/20 border border-indigo-400/40 text-indigo-300 font-mono text-xs font-bold group-hover:bg-indigo-400 group-hover:text-black transition">Choice [${letter}]</span>
                <span class="text-[10px] font-mono text-slate-400 bg-slate-800/80 px-2 py-0.5 rounded">Key: ${num}</span>
              </div>
              <div class="flex items-center justify-center my-1.5 w-full">
                ${this.renderMatrixSVG(opt.matrixData, 80, 80)}
              </div>
              <span class="text-[11px] font-mono text-indigo-300 font-semibold group-hover:text-white mt-0.5">Select Option ${letter}</span>
            `;
            div.onclick = () => this.recordAnswer(opt.isCorrect);
            grid.appendChild(div);
          });
        }
      },

      recordAnswerByKey(idx) {
        const grid = document.getElementById('memoryProbeGrid');
        if (grid && !grid.classList.contains('hidden')) {
          const tiles = grid.querySelectorAll('[data-choice-idx]');
          if (tiles && tiles[idx]) {
            tiles[idx].click();
          }
        }
      },

      recordAnswer(isCorrect) {
        this.clearTimers();
        const latency = (Date.now() - this.trialStartTime) / 1000;
        this.latencies.push(latency);
        if (isCorrect) this.correctCount++;

        const avgLat = (this.latencies.reduce((a, b) => a + b, 0) / this.latencies.length).toFixed(2);
        const accPct = Math.round((this.correctCount / (this.currentTrial + 1)) * 100);

        const accEl = document.getElementById('memoryAccuracyTelemetry');
        if (accEl) accEl.textContent = `Accuracy: ${accPct}%`;
        const latEl = document.getElementById('memoryLatencyTelemetry');
        if (latEl) latEl.textContent = `Avg Latency: ${avgLat}s`;

        this.runTrial(this.currentTrial + 1);
      },

      finish() {
        this.clearTimers();
        const acc = Math.round((this.correctCount / this.totalTrials) * 100);
        const avgLat = (this.latencies.reduce((a, b) => a + b, 0) / this.latencies.length).toFixed(2);
        const score = Math.round(90 + (acc * 0.35) - (avgLat * 5));
        const finalScore = Math.max(75, Math.min(145, score));

        document.getElementById('genericReportTitle').textContent = 'Visual Memory Recognition Dossier';
        document.getElementById('genericReportSubtitle').textContent = 'PEBL-Standard Delayed Match-to-Sample (DMTS) Protocol (40 Trials)';

        document.getElementById('genericReportHero').innerHTML = `
          <div class="p-4 rounded-2xl bg-indigo-950/40 border border-indigo-500/30">
            <span class="text-[10px] font-mono text-slate-400 uppercase tracking-widest block mb-1">RETENTION ACCURACY</span>
            <span class="text-4xl sm:text-5xl font-mono font-extrabold text-indigo-300">${acc}%</span>
          </div>
          <div class="p-4 rounded-2xl bg-cyan-950/40 border border-cyan-500/30">
            <span class="text-[10px] font-mono text-slate-400 uppercase tracking-widest block mb-1">MEMORY RECOGNITION INDEX</span>
            <span class="text-4xl sm:text-5xl font-mono font-extrabold text-cyan-400">${finalScore}</span>
          </div>
          <div class="p-4 rounded-2xl bg-purple-950/40 border border-purple-500/30">
            <span class="text-[10px] font-mono text-slate-400 uppercase tracking-widest block mb-1">MEAN RECOGNITION LATENCY</span>
            <span class="text-4xl sm:text-5xl font-mono font-extrabold text-purple-300">${avgLat}s</span>
          </div>
        `;

        document.getElementById('genericReportBreakdown').innerHTML = `
          <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 space-y-3">
            <div class="flex justify-between text-xs font-mono">
              <span class="text-slate-400">Total Trials: ${this.totalTrials}</span>
              <span class="text-indigo-300 font-bold">${this.correctCount} / ${this.totalTrials} Correct (${acc}%)</span>
            </div>
            <div class="w-full bg-slate-950 h-2.5 rounded-full overflow-hidden">
              <div class="bg-gradient-to-r from-indigo-500 to-cyan-400 h-full rounded-full" style="width: ${acc}%;"></div>
            </div>
          </div>
        `;

        document.getElementById('genericReportInterpretation').innerHTML = `
          <p>• <strong>Visuospatial Sketchpad Retention:</strong> You successfully recognized ${this.correctCount} of ${this.totalTrials} abstract matrix configurations under temporal decay intervals, indicating ${acc >= 75 ? 'high structural fidelity' : 'standard retention capacity'} in prefrontal-hippocampal consolidation across 40 full-load trials.</p>
          <p>• <strong>Discrimination Latency:</strong> Average identification latency of ${avgLat}s demonstrates fast feature extraction and sustained vigilance across extended trial blocks.</p>
        `;

        showScreen('screenGenericReport');
      }
    };
    window.DMTSBrain = window.MemoryTestEngine;
'''

html = re.sub(
    r'// =+ 1\. MEMORY RECOGNITION \(DMTS\) ENGINE =+\s*window\.MemoryTestEngine = \{.*?\n\s*\};\n',
    new_mem_js,
    html,
    flags=re.DOTALL
)

# ======================================================================
# 3. NEW JAVASCRIPT FOR NBackEngine (Jaeggi PNAS Model: Initial Buffer & Sequential Pacing)
# ======================================================================
new_nback_js = '''// ==================== 2. NEUROPLASTICITY (DUAL N-BACK) ENGINE ====================
    window.NBackEngine = {
      step: 0,
      totalSteps: 40,
      n: 2,
      history: [],
      hits: 0,
      misses: 0,
      tokens: ['K', 'R', 'M', 'Q', 'X', 'T'],
      timerId: null,
      countdownInterval: null,
      timeLeftMs: 0,

      start() {
        this.step = 0;
        this.history = [];
        this.hits = 0;
        this.misses = 0;
        this.clearTimers();
        showScreen('screenNeuroplasticity');
        this.runStep(0);
      },

      clearTimers() {
        if (this.timerId) {
          clearTimeout(this.timerId);
          this.timerId = null;
        }
        if (this.countdownInterval) {
          clearInterval(this.countdownInterval);
          this.countdownInterval = null;
        }
      },

      runStep(index) {
        this.clearTimers();

        if (index >= this.totalSteps) {
          this.finish();
          return;
        }

        this.step = index;
        document.getElementById('nbackStepBadge').textContent = `Step ${index + 1} of ${this.totalSteps}`;

        const pct = Math.round(((index) / this.totalSteps) * 100);
        const pb2 = document.getElementById('nbackProgressBar');
        if (pb2) pb2.style.width = `${pct}%`;

        // Generate stimulus with controlled ~35% match rate after step N
        let pos = Math.floor(Math.random() * 9);
        let token = this.tokens[Math.floor(Math.random() * this.tokens.length)];

        if (index >= this.n && Math.random() < 0.35) {
          const past = this.history[index - this.n];
          if (Math.random() < 0.5) pos = past.pos;
          else token = past.token;
        }

        this.history.push({ pos, token });

        // Render 3x3 Grid
        const grid = document.getElementById('nbackGrid');
        if (grid) {
          grid.innerHTML = '';
          for (let i = 0; i < 9; i++) {
            const cell = document.createElement('div');
            cell.className = (i === pos)
              ? 'rounded-xl bg-emerald-400 border-2 border-white flex items-center justify-center font-bold text-black holo-glow-cyan animate-pulse shadow-lg shadow-emerald-500/50'
              : 'rounded-xl bg-slate-900 border border-slate-800';
            grid.appendChild(cell);
          }
        }

        const letterEl = document.getElementById('nbackLetterToken');
        if (letterEl) letterEl.textContent = token;

        const instructionEl = document.getElementById('nbackInstructionText');
        const timerEl = document.getElementById('nbackTimer');
        const encodingPanel = document.getElementById('nbackEncodingPanel');
        const responsePanel = document.getElementById('nbackResponsePanel');
        const pillEl = document.getElementById('nbackEncodingTimerPill');

        if (index < this.n) {
          // ==================== ENCODING-ONLY BUFFER (i <= N) ====================
          if (instructionEl) {
            instructionEl.textContent = `ENCODING PHASE: Memorize spatial position & letter (Step ${index + 1} of ${this.n})... Auto-advancing`;
          }
          if (encodingPanel) encodingPanel.classList.remove('hidden');
          if (responsePanel) responsePanel.classList.add('hidden');

          this.timeLeftMs = 2500;
          if (timerEl) timerEl.textContent = '2.5s';
          if (pillEl) pillEl.textContent = '2.5s';

          this.countdownInterval = setInterval(() => {
            this.timeLeftMs -= 100;
            const sec = Math.max(0, (this.timeLeftMs / 1000)).toFixed(1) + 's';
            if (timerEl) timerEl.textContent = sec;
            if (pillEl) pillEl.textContent = sec;
            if (this.timeLeftMs <= 0) {
              this.clearTimers();
              this.runStep(index + 1);
            }
          }, 100);
        } else {
          // ==================== ACTIVE COMPARISON PHASE (i > N) ====================
          if (instructionEl) {
            instructionEl.textContent = 'EVALUATE MATCH: Does current stimulus match 2 steps back?';
          }
          if (encodingPanel) encodingPanel.classList.add('hidden');
          if (responsePanel) responsePanel.classList.remove('hidden');

          this.timeLeftMs = 3000;
          if (timerEl) timerEl.textContent = '3.0s';

          this.countdownInterval = setInterval(() => {
            this.timeLeftMs -= 100;
            const sec = Math.max(0, (this.timeLeftMs / 1000)).toFixed(1) + 's';
            if (timerEl) timerEl.textContent = sec;
            if (this.timeLeftMs <= 0) {
              this.clearTimers();
              this.recordResponse('timeout');
            }
          }, 100);
        }
      },

      advanceEncoding() {
        if (this.step < this.n) {
          this.clearTimers();
          this.runStep(this.step + 1);
        }
      },

      recordResponse(type) {
        this.clearTimers();

        if (this.step >= this.n) {
          const target = this.history[this.step - this.n];
          const current = this.history[this.step];

          const posMatch = (target.pos === current.pos);
          const letterMatch = (target.token === current.token);
          const hasAnyMatch = posMatch || letterMatch;

          let isCorrect = false;
          if (type === 'both' && posMatch && letterMatch) isCorrect = true;
          else if (type === 'position' && posMatch && !letterMatch) isCorrect = true;
          else if (type === 'letter' && !posMatch && letterMatch) isCorrect = true;
          else if (type === 'none' && !posMatch && !letterMatch) isCorrect = true;
          else if (type === 'timeout') {
            isCorrect = !hasAnyMatch;
          }

          if (isCorrect) this.hits++;
          else this.misses++;

          const scoreEl = document.getElementById('nbackScoreTelemetry');
          if (scoreEl) {
            scoreEl.textContent = `Hits: ${this.hits} • Misses: ${this.misses}`;
          }
        }

        this.runStep(this.step + 1);
      },

      finish() {
        this.clearTimers();
        const totalEvaluated = Math.max(1, this.totalSteps - this.n);
        const accuracy = Math.round((this.hits / totalEvaluated) * 100);
        const plasticityIndex = Math.round(95 + (accuracy * 0.3));

        document.getElementById('genericReportTitle').textContent = 'Neuroplasticity Tracking Dossier';
        document.getElementById('genericReportSubtitle').textContent = 'Jaeggi Dual N-Back Working Memory Updating Metric (40 Steps)';

        document.getElementById('genericReportHero').innerHTML = `
          <div class="p-4 rounded-2xl bg-emerald-950/40 border border-emerald-500/30">
            <span class="text-[10px] font-mono text-slate-400 uppercase tracking-widest block mb-1">UPDATING ACCURACY</span>
            <span class="text-4xl sm:text-5xl font-mono font-extrabold text-emerald-400">${accuracy}%</span>
          </div>
          <div class="p-4 rounded-2xl bg-cyan-950/40 border border-cyan-500/30">
            <span class="text-[10px] font-mono text-slate-400 uppercase tracking-widest block mb-1">PLASTICITY RESERVE INDEX</span>
            <span class="text-4xl sm:text-5xl font-mono font-extrabold text-cyan-300">${plasticityIndex}</span>
          </div>
          <div class="p-4 rounded-2xl bg-purple-950/40 border border-purple-500/30">
            <span class="text-[10px] font-mono text-slate-400 uppercase tracking-widest block mb-1">RESERVE CLASSIFICATION</span>
            <span class="text-xl sm:text-2xl font-mono font-bold text-purple-300 mt-2 block">${accuracy >= 75 ? 'High Plasticity' : 'Adaptive Reserve'}</span>
          </div>
        `;

        document.getElementById('genericReportBreakdown').innerHTML = `
          <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 space-y-3">
            <div class="flex justify-between text-xs font-mono">
              <span class="text-slate-400">Total Steps: ${this.totalSteps} (Encoding: ${this.n}, Active: ${totalEvaluated})</span>
              <span class="text-emerald-300 font-bold">${this.hits} Correct / ${this.misses} Misses</span>
            </div>
            <div class="w-full bg-slate-950 h-2.5 rounded-full overflow-hidden">
              <div class="bg-gradient-to-r from-emerald-400 to-cyan-400 h-full rounded-full" style="width: ${accuracy}%;"></div>
            </div>
          </div>
        `;

        document.getElementById('genericReportInterpretation').innerHTML = `
          <p>• <strong>Working Memory Updating:</strong> Successfully maintained dual modalities across 40 continuous serial presentations, achieving ${accuracy}% matching accuracy on N=2 temporal intervals.</p>
          <p>• <strong>Clinical Reserve Metric:</strong> High performance on dual n-back demonstrates resilience against proactive interference and robust executive control in dorsolateral prefrontal cortex networks.</p>
        `;

        showScreen('screenGenericReport');
      }
    };
'''

html = re.sub(
    r'// =+ 2\. NEUROPLASTICITY \(DUAL N-BACK\) ENGINE =+\s*window\.NBackEngine = \{.*?\n\s*\};\n',
    new_nback_js,
    html,
    flags=re.DOTALL
)

# ======================================================================
# 4. NEW KEYDOWN LISTENER (Space/A/L/N for Dual N-Back + 1-4/A-D for DMTS)
# ======================================================================
new_keydown_code = '''window.addEventListener('keydown', (e) => {
      // 1. Processing Speed Test
      if (typeof app !== 'undefined' && app.state && app.state.speed && app.state.speed.active) {
        if (e.key.toLowerCase() === 'y') {
          app.recordSpeedResponse(true);
          return;
        } else if (e.key.toLowerCase() === 'n') {
          app.recordSpeedResponse(false);
          return;
        }
      }

      const isScreenActive = (id) => {
        const el = document.getElementById(id);
        return el && !el.classList.contains('hidden');
      };

      const key = e.key.toLowerCase();
      const num = parseInt(e.key);

      // 2. DMTS Memory Test (Keys 1-4 or A-D)
      if (isScreenActive('screenMemory')) {
        const letterMap = { 'a': 0, 'b': 1, 'c': 2, 'd': 3 };
        const engine = window.MemoryTestEngine || window.DMTSBrain;
        if (letterMap.hasOwnProperty(key)) {
          if (engine && engine.recordAnswerByKey) {
            engine.recordAnswerByKey(letterMap[key]);
            return;
          }
        }
        if (!isNaN(num) && num >= 1 && num <= 4) {
          if (engine && engine.recordAnswerByKey) {
            engine.recordAnswerByKey(num - 1);
            return;
          }
        }
      }

      // 3. Neuroplasticity Dual N-Back
      if (isScreenActive('screenNeuroplasticity')) {
        if (window.NBackEngine) {
          // If in Encoding phase (step < 2)
          if (window.NBackEngine.step < window.NBackEngine.n) {
            if (e.key === ' ' || e.code === 'Space') {
              e.preventDefault();
              window.NBackEngine.advanceEncoding();
              return;
            }
          } else {
            // In Active Comparison phase
            if (key === 'a') {
              window.NBackEngine.recordResponse('position');
              return;
            } else if (key === 'l') {
              window.NBackEngine.recordResponse('letter');
              return;
            } else if (e.key === ' ' || e.code === 'Space') {
              e.preventDefault();
              window.NBackEngine.recordResponse('both');
              return;
            } else if (key === 'n') {
              window.NBackEngine.recordResponse('none');
              return;
            }
          }
        }
      }

      // 4. Personality Test (Keys 1-5)
      if (isScreenActive('screenPersonality')) {
        if (!isNaN(num) && num >= 1 && num <= 5) {
          if (window.PersonalityTestEngine) {
            window.PersonalityTestEngine.recordAnswer(num);
            return;
          }
        }
      }

      // 5. Multiple Intelligences (Keys 1-5)
      if (isScreenActive('screenMulti')) {
        if (!isNaN(num) && num >= 1 && num <= 5) {
          if (window.MultiIntelligenceEngine) {
            window.MultiIntelligenceEngine.recordAnswer(num);
            return;
          }
        }
      }

      // 6. Clinical Screeners (Keys 1-5)
      if (isScreenActive('screenClinical')) {
        if (!isNaN(num) && num >= 1 && num <= 5) {
          const grid = document.getElementById('clinicalOptionsGrid');
          if (grid) {
            const btn = grid.querySelector(`[data-opt-key="${num}"]`);
            if (btn) {
              btn.click();
              return;
            }
          }
        }
      }

      // 7. Fluid Matrix & Quantitative Workspace (Keys 1-6 and Enter)
      if (isScreenActive('screenWorkspace')) {
        if (!isNaN(num) && num >= 1 && num <= 6) {
          const optionTile = document.getElementById(`optionTile_${num}`);
          if (optionTile) optionTile.click();
        }

        if (e.key === 'Enter') {
          const btnNext = document.getElementById('btnNextItem');
          if (btnNext && !btnNext.disabled) {
            btnNext.click();
          }
        }
      }
    });
  </script>'''

html = re.sub(
    r'window\.addEventListener\(\'keydown\',\s*\(e\)\s*=>\s*\{.*?</script>',
    new_keydown_code,
    html,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Both fixes applied successfully to index.html!")
