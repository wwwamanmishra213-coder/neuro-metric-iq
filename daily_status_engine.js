/* ==========================================================================
   NEUROMETRIC DAILY COGNITIVE STATUS & PUSH ALARM ENGINE
   - Daily Status Management (Energy, Focus, Mood, Sleep, Cognitive Readiness)
   - Alarm Scheduler with Web Audio chime synthesis (zero external audio files needed)
   - Web Push / HTML5 Notification API Protocol with local fallback HUD alert
   - Persistent LocalStorage State & Streak Counter
   ========================================================================== */

(function(root) {
  'use strict';

  const STORAGE_KEY_STATUS = 'neurometric_daily_status_log';
  const STORAGE_KEY_ALARM = 'neurometric_daily_alarm_config';

  const DailyStatusEngine = {
    audioCtx: null,
    alarmTimer: null,
    chimeInterval: null,

    init() {
      this.checkAlarmClock();
      // Check every 10 seconds for scheduled alarm
      setInterval(() => this.checkAlarmClock(), 10000);
      this.updateHeaderBadge();
    },

    // ==================== 1. MODAL / TAB CONTROLLER ====================
    openTab() {
      let modal = document.getElementById('dailyStatusModal');
      if (!modal) {
        this.renderModalDOM();
        modal = document.getElementById('dailyStatusModal');
      }
      if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        this.populateFormData();
        this.renderHistory();
      }
    },

    closeTab() {
      const modal = document.getElementById('dailyStatusModal');
      if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
      }
    },

    // ==================== 2. STATUS TRACKING LOGIC ====================
    saveDailyStatus() {
      const energy = parseInt(document.getElementById('statusEnergyRange')?.value || '7');
      const focus = parseInt(document.getElementById('statusFocusRange')?.value || '8');
      const sleep = parseFloat(document.getElementById('statusSleepHours')?.value || '7.5');
      const mood = document.getElementById('statusMoodSelect')?.value || 'Focused & Alert';
      const notes = document.getElementById('statusNotesInput')?.value || '';

      // Compute Cognitive Readiness Index (0 - 100)
      const readinessIndex = Math.min(100, Math.round(((energy * 3) + (focus * 4) + (Math.min(sleep, 8) * 3.75))));

      const todayStr = new Date().toISOString().split('T')[0];
      const log = this.getHistory();
      
      const newEntry = {
        date: todayStr,
        timestamp: new Date().toISOString(),
        energy,
        focus,
        sleep,
        mood,
        readinessIndex,
        notes
      };

      // Filter out duplicate for today
      const filtered = log.filter(e => e.date !== todayStr);
      filtered.unshift(newEntry);

      localStorage.setItem(STORAGE_KEY_STATUS, JSON.stringify(filtered.slice(0, 30)));

      // Trigger celebratory chime
      this.playSyntheticChime(587.33, 880); // D5 -> A5

      // Show toast
      this.showToast(`✓ Daily Status Saved! Cognitive Readiness: ${readinessIndex}/100`);
      this.renderHistory();
    },

    getHistory() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY_STATUS);
        return raw ? JSON.parse(raw) : [];
      } catch (e) {
        return [];
      }
    },

    getAlarmConfig() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY_ALARM);
        return raw ? JSON.parse(raw) : { enabled: false, time: '09:00', label: 'Morning Cognitive Assessment' };
      } catch (e) {
        return { enabled: false, time: '09:00', label: 'Morning Cognitive Assessment' };
      }
    },

    // ==================== 3. ALARM & PUSH NOTIFICATION PROTOCOL ====================
    async requestNotificationPermission() {
      if (!('Notification' in window)) {
        alert('This browser does not support desktop push notifications. Audio alarm chime will still work.');
        return false;
      }
      if (Notification.permission === 'granted') return true;
      if (Notification.permission !== 'denied') {
        const permission = await Notification.requestPermission();
        return permission === 'granted';
      }
      return false;
    },

    async setAlarm() {
      const timeVal = document.getElementById('alarmTimeInput')?.value || '09:00';
      const labelVal = document.getElementById('alarmLabelInput')?.value || 'Daily Cognitive Assessment Protocol';
      const isEnabled = document.getElementById('alarmEnableToggle')?.checked ?? true;

      // Ask for push notification permission
      if (isEnabled) {
        await this.requestNotificationPermission();
      }

      const config = {
        enabled: isEnabled,
        time: timeVal,
        label: labelVal,
        lastTriggeredDate: null
      };

      localStorage.setItem(STORAGE_KEY_ALARM, JSON.stringify(config));
      this.updateHeaderBadge();

      if (isEnabled) {
        this.playSyntheticChime(440, 659.25); // A4 -> E5 pleasant chime
        this.showToast(`⏰ Daily Alarm set for ${timeVal}! Push notification & audio alert active.`);
      } else {
        this.showToast('Alarm disabled.');
      }
    },

    checkAlarmClock() {
      const config = this.getAlarmConfig();
      if (!config.enabled || !config.time) return;

      const now = new Date();
      const currentHours = String(now.getHours()).padStart(2, '0');
      const currentMinutes = String(now.getMinutes()).padStart(2, '0');
      const currentTimeStr = `${currentHours}:${currentMinutes}`;
      const todayStr = now.toISOString().split('T')[0];

      if (currentTimeStr === config.time && config.lastTriggeredDate !== todayStr) {
        // Trigger Alarm Protocol
        config.lastTriggeredDate = todayStr;
        localStorage.setItem(STORAGE_KEY_ALARM, JSON.stringify(config));
        this.triggerAlarmAlert(config);
      }
    },

    triggerAlarmAlert(config) {
      // 1. Play repeating rhythmic attention-attracting binaural alarm chime
      this.startAlarmChimeLoop();

      // 2. Trigger native OS Push Notification
      if ('Notification' in window && Notification.permission === 'granted') {
        try {
          new Notification('🧠 NEUROMETRIC COGNITIVE ALARM', {
            body: `${config.label || 'Time for your daily cognitive assessment & status update!'} (Scheduled for ${config.time})`,
            icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%2306b6d4"><circle cx="12" cy="12" r="10"/></svg>',
            requireInteraction: true
          });
        } catch (e) {
          console.warn('Notification error:', e);
        }
      }

      // 3. Render prominent Screen Alert Modal
      this.renderAlarmBanner(config);
    },

    startAlarmChimeLoop() {
      let count = 0;
      this.stopAlarmChime();
      this.playSyntheticChime(523.25, 659.25, 783.99); // C5, E5, G5 triad
      
      this.chimeInterval = setInterval(() => {
        count++;
        this.playSyntheticChime(523.25, 659.25, 783.99);
        if (count >= 10) {
          this.stopAlarmChime();
        }
      }, 2000);
    },

    stopAlarmChime() {
      if (this.chimeInterval) {
        clearInterval(this.chimeInterval);
        this.chimeInterval = null;
      }
    },

    renderAlarmBanner(config) {
      let banner = document.getElementById('nmActiveAlarmBanner');
      if (banner && banner.parentNode) banner.parentNode.removeChild(banner);

      banner = document.createElement('div');
      banner.id = 'nmActiveAlarmBanner';
      banner.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);z-index:9999999;width:90%;max-width:540px;background:#0F172A;border:2px solid #F59E0B;border-radius:20px;box-shadow:0 20px 60px rgba(245,158,11,0.5);padding:20px;font-family:sans-serif;animation:pulse 2s infinite;';
      banner.innerHTML = `
        <div style="display:flex;align-items:start;justify-content:space-between;gap:15px;">
          <div style="font-size:32px;">⏰</div>
          <div style="flex:1;">
            <div style="font-size:11px;font-family:monospace;font-weight:bold;color:#FBBF24;letter-spacing:1.5px;text-transform:uppercase;">NEUROMETRIC DAILY COGNITIVE PROTOCOL</div>
            <div style="font-size:15px;font-weight:bold;color:#FFFFFF;margin-top:2px;">${config.label || 'Time for your daily brain assessment!'}</div>
            <div style="font-size:12px;color:#94A3B8;margin-top:4px;">Scheduled alarm at ${config.time}. Ready to test your focus & log daily readiness?</div>
            <div style="display:flex;gap:10px;margin-top:14px;">
              <button onclick="DailyStatusEngine.stopAlarmChime(); document.getElementById('nmActiveAlarmBanner').remove(); DailyStatusEngine.openTab();" style="background:#F59E0B;color:#000;font-weight:bold;font-size:12px;font-family:monospace;padding:8px 16px;border-radius:10px;border:none;cursor:pointer;">
                📊 Log Daily Status
              </button>
              <button onclick="DailyStatusEngine.stopAlarmChime(); document.getElementById('nmActiveAlarmBanner').remove(); if(window.AssessmentController) AssessmentController.startBattery();" style="background:#06B6D4;color:#000;font-weight:bold;font-size:12px;font-family:monospace;padding:8px 16px;border-radius:10px;border:none;cursor:pointer;">
                🧠 Start Cognitive Test
              </button>
              <button onclick="DailyStatusEngine.stopAlarmChime(); document.getElementById('nmActiveAlarmBanner').remove();" style="background:#1E293B;color:#94A3B8;font-size:12px;padding:8px 12px;border-radius:10px;border:1px solid #334155;cursor:pointer;">
                Dismiss
              </button>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(banner);
    },

    // ==================== 4. WEB AUDIO SYNTHETIC CHIME ====================
    playSyntheticChime(...freqs) {
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        if (!this.audioCtx) this.audioCtx = new AudioCtx();
        if (this.audioCtx.state === 'suspended') {
          this.audioCtx.resume();
        }

        const now = this.audioCtx.currentTime;
        freqs.forEach((freq, idx) => {
          const osc = this.audioCtx.createOscillator();
          const gain = this.audioCtx.createGain();

          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, now + (idx * 0.12));

          gain.gain.setValueAtTime(0, now + (idx * 0.12));
          gain.gain.linearRampToValueAtTime(0.18, now + (idx * 0.12) + 0.04);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + (idx * 0.12) + 1.2);

          osc.connect(gain);
          gain.connect(this.audioCtx.destination);

          osc.start(now + (idx * 0.12));
          osc.stop(now + (idx * 0.12) + 1.3);
        });
      } catch (e) {
        console.warn('Audio chime error:', e);
      }
    },

    updateHeaderBadge() {
      const cfg = this.getAlarmConfig();
      const dot = document.getElementById('dailyAlarmPulseDot');
      const pill = document.getElementById('dailyAlarmHeaderPill');
      if (dot && pill) {
        if (cfg.enabled) {
          dot.className = 'w-2 h-2 rounded-full bg-emerald-400 animate-pulse';
          pill.className = 'text-[9px] sm:text-[10px] bg-emerald-950 px-1 py-0.5 rounded text-emerald-300 font-bold';
          pill.textContent = cfg.time || 'ALARM';
        } else {
          dot.className = 'w-2 h-2 rounded-full bg-amber-400';
          pill.className = 'text-[9px] sm:text-[10px] bg-amber-950 px-1 py-0.5 rounded text-amber-200 font-bold';
          pill.textContent = 'STATUS';
        }
      }
    },

    showToast(msg) {
      let toast = document.getElementById('nmDailyToast');
      if (toast && toast.parentNode) toast.parentNode.removeChild(toast);

      toast = document.createElement('div');
      toast.id = 'nmDailyToast';
      toast.style.cssText = 'position:fixed;bottom:24px;left:24px;z-index:999999;background:#0A101D;border:1px solid #F59E0B;color:#FDE68A;padding:12px 20px;border-radius:14px;font-family:monospace;font-size:12px;box-shadow:0 10px 30px rgba(245,158,11,0.25);display:flex;align-items:center;gap:10px;';
      toast.innerHTML = `<span style="font-size:16px;">📅</span><span>${msg}</span>`;
      document.body.appendChild(toast);
      setTimeout(() => { if (toast && toast.parentNode) toast.parentNode.removeChild(toast); }, 4000);
    },

    populateFormData() {
      const cfg = this.getAlarmConfig();
      const timeInp = document.getElementById('alarmTimeInput');
      const labelInp = document.getElementById('alarmLabelInput');
      const toggle = document.getElementById('alarmEnableToggle');

      if (timeInp) timeInp.value = cfg.time || '09:00';
      if (labelInp) labelInp.value = cfg.label || 'Daily Cognitive Assessment Protocol';
      if (toggle) toggle.checked = !!cfg.enabled;
    },

    renderHistory() {
      const tbody = document.getElementById('dailyStatusHistoryBody');
      if (!tbody) return;

      const log = this.getHistory();
      if (log.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="py-4 text-center text-slate-500 font-mono text-[11px]">No status logs recorded yet. Log today\'s bio-metrics above!</td></tr>`;
        return;
      }

      tbody.innerHTML = log.map(e => `
        <tr class="border-b border-slate-800 text-[11px] font-mono">
          <td class="py-2.5 text-amber-300 font-bold">${e.date}</td>
          <td class="py-2.5 text-cyan-300">${e.energy}/10</td>
          <td class="py-2.5 text-purple-300">${e.focus}/10</td>
          <td class="py-2.5 text-slate-300">${e.sleep}h</td>
          <td class="py-2.5 font-bold ${e.readinessIndex >= 80 ? 'text-emerald-400' : (e.readinessIndex >= 60 ? 'text-amber-400' : 'text-rose-400')}">
            ${e.readinessIndex}%
          </td>
        </tr>
      `).join('');
    },

    renderModalDOM() {
      const existing = document.getElementById('dailyStatusModal');
      if (existing) return;

      const div = document.createElement('div');
      div.id = 'dailyStatusModal';
      div.className = 'fixed inset-0 bg-black/85 backdrop-blur-md z-50 hidden items-center justify-center p-3 sm:p-5 no-print';
      div.innerHTML = `
        <div class="holo-card max-w-2xl w-full rounded-3xl p-5 sm:p-7 space-y-4 relative border border-amber-500/40 shadow-2xl shadow-amber-950/60 font-sans max-h-[92vh] overflow-y-auto">
          
          <!-- Header -->
          <div class="flex items-start justify-between border-b border-amber-500/20 pb-3">
            <div class="flex items-center space-x-3">
              <span class="text-3xl text-amber-400">📅</span>
              <div>
                <h3 class="text-base sm:text-lg font-bold text-white flex items-center gap-2 font-mono">
                  <span>DAILY COGNITIVE STATUS & ALARM PROTOCOL</span>
                  <span class="text-[9px] font-mono px-2 py-0.5 rounded bg-amber-950 border border-amber-500/50 text-amber-300 font-bold">BIO-TELEMETRY</span>
                </h3>
                <span class="text-[10px] font-mono text-amber-300/80 uppercase tracking-widest">Circadian Tracking • Push Alarm Notification • Readiness Index</span>
              </div>
            </div>
            <button class="w-8 h-8 rounded-lg bg-slate-900 border border-slate-700 hover:border-amber-400 text-slate-400 hover:text-white flex items-center justify-center text-sm font-mono transition" onclick="DailyStatusEngine.closeTab()">✕</button>
          </div>

          <!-- Section 1: Daily Bio-Telemetry & Readiness Log -->
          <div class="p-4 rounded-2xl bg-slate-950/80 border border-amber-500/30 space-y-3 font-mono text-xs">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2">
              <span class="text-amber-300 font-bold flex items-center gap-1.5">
                <span>⚡</span> LOG TODAY'S BIO-METRICS
              </span>
              <span class="text-[10px] text-slate-400">Calculates Daily Readiness Score</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <div>
                <label class="block text-slate-300 text-[11px] mb-1">ENERGY LEVEL (1 - 10): <span id="lblEnergyVal" class="text-cyan-400 font-bold">7</span></label>
                <input type="range" id="statusEnergyRange" min="1" max="10" value="7" class="w-full accent-cyan-400" oninput="document.getElementById('lblEnergyVal').textContent = this.value">
              </div>

              <div>
                <label class="block text-slate-300 text-[11px] mb-1">MENTAL FOCUS (1 - 10): <span id="lblFocusVal" class="text-purple-400 font-bold">8</span></label>
                <input type="range" id="statusFocusRange" min="1" max="10" value="8" class="w-full accent-purple-400" oninput="document.getElementById('lblFocusVal').textContent = this.value">
              </div>

              <div>
                <label class="block text-slate-300 text-[11px] mb-1">SLEEP DURATION (HOURS):</label>
                <input type="number" id="statusSleepHours" step="0.5" min="2" max="14" value="7.5" class="w-full bg-black border border-slate-700 rounded-xl px-3 py-1.5 text-white text-xs outline-none focus:border-amber-400">
              </div>

              <div>
                <label class="block text-slate-300 text-[11px] mb-1">DOMINANT MOOD STATE:</label>
                <select id="statusMoodSelect" class="w-full bg-black border border-slate-700 rounded-xl px-3 py-1.5 text-white text-xs outline-none focus:border-amber-400">
                  <option value="Focused & Alert">Focused & Alert (Optimal)</option>
                  <option value="Calm & Relaxed">Calm & Relaxed</option>
                  <option value="Mild Fatigue">Mild Mental Fatigue</option>
                  <option value="Stressed / Overstimulated">Stressed / Overstimulated</option>
                  <option value="Brain Fog / Sleep Deprived">Brain Fog / Sleep Deprived</option>
                </select>
              </div>
            </div>

            <div class="pt-1 flex items-center justify-between">
              <input type="text" id="statusNotesInput" placeholder="Optional notes (e.g., drank coffee, exercised, fasted)..." class="flex-1 bg-black border border-slate-800 rounded-xl px-3 py-1.5 text-white text-[11px] outline-none mr-2 focus:border-amber-400">
              <button onclick="DailyStatusEngine.saveDailyStatus()" class="px-4 py-2 rounded-xl bg-gradient-to-r from-amber-400 to-orange-400 text-black font-bold text-xs hover:brightness-110 active:scale-95 transition shadow-lg shadow-amber-500/20">
                Save Status
              </button>
            </div>
          </div>

          <!-- Section 2: Push Notification & Sound Alarm Protocol -->
          <div class="p-4 rounded-2xl bg-gradient-to-br from-slate-950/90 to-indigo-950/30 border border-indigo-500/30 space-y-3 font-mono text-xs">
            <div class="flex items-center justify-between border-b border-indigo-500/20 pb-2">
              <span class="text-indigo-300 font-bold flex items-center gap-1.5">
                <span>⏰</span> DAILY TEST ALARM & PUSH PROTOCOL
              </span>
              <label class="flex items-center gap-2 cursor-pointer">
                <span class="text-[10px] text-slate-400">ACTIVE:</span>
                <input type="checkbox" id="alarmEnableToggle" checked class="w-4 h-4 accent-amber-400 cursor-pointer">
              </label>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label class="block text-slate-300 text-[11px] mb-1">DAILY ALARM TIME (24H):</label>
                <input type="time" id="alarmTimeInput" value="09:00" class="w-full bg-black border border-slate-700 rounded-xl px-3 py-2 text-amber-300 text-sm font-bold outline-none focus:border-amber-400">
              </div>

              <div>
                <label class="block text-slate-300 text-[11px] mb-1">ALARM PROTOCOL LABEL:</label>
                <input type="text" id="alarmLabelInput" value="Daily Cognitive Assessment Protocol" class="w-full bg-black border border-slate-700 rounded-xl px-3 py-2 text-white text-xs outline-none focus:border-amber-400">
              </div>
            </div>

            <div class="flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-slate-800">
              <button type="button" onclick="DailyStatusEngine.playSyntheticChime(523.25, 659.25, 783.99)" class="text-[10px] text-cyan-400 hover:underline flex items-center gap-1">
                <span>🔔</span> Test Alarm Chime
              </button>
              <button onclick="DailyStatusEngine.setAlarm()" class="px-5 py-2 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-bold text-xs hover:brightness-110 active:scale-95 transition shadow-lg shadow-indigo-500/20">
                Confirm & Set Daily Alarm
              </button>
            </div>
          </div>

          <!-- Section 3: 30-Day Status History -->
          <div class="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2">
            <div class="flex items-center justify-between border-b border-slate-800 pb-2 font-mono">
              <span class="text-white font-bold text-xs flex items-center gap-1.5">
                <span>📈</span> RECENT STATUS LOGS
              </span>
              <span class="text-[10px] text-amber-400">READINESS TREND</span>
            </div>
            <div class="overflow-x-auto max-h-40 overflow-y-auto custom-scrollbar">
              <table class="w-full text-left">
                <thead>
                  <tr class="text-slate-400 border-b border-slate-800 text-[10px] font-mono">
                    <th class="py-1.5">DATE</th>
                    <th class="py-1.5">ENERGY</th>
                    <th class="py-1.5">FOCUS</th>
                    <th class="py-1.5">SLEEP</th>
                    <th class="py-1.5">READINESS</th>
                  </tr>
                </thead>
                <tbody id="dailyStatusHistoryBody">
                  <!-- Rendered dynamically -->
                </tbody>
              </table>
            </div>
          </div>

        </div>
      `;
      document.body.appendChild(div);
    }
  };

  root.DailyStatusEngine = DailyStatusEngine;

  // Initialize on DOM ready
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => DailyStatusEngine.init());
    } else {
      DailyStatusEngine.init();
    }
  }

})(typeof window !== 'undefined' ? window : this);
