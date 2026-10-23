import re

def create_client():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Title for Client Portal
    html = re.sub(
        r'<title>.*?</title>',
        '<title>NEURO-METRIC | Patient Cognitive Assessment &amp; Clinical Certification</title>',
        html
    )

    # 2. Completely remove the Admin Shield 2FA Button from header
    admin_btn_pattern = r'<!-- Admin Shield 2FA Button -->[\s\S]*?</button>'
    html = re.sub(admin_btn_pattern, '<!-- Client Mode: Admin button excluded -->', html)

    # 3. Completely remove the Admin Portal Modal from the DOM
    admin_modal_pattern = r'<!-- ==================== ADMIN SHIELD AUTHENTICATOR \(TOTP 2FA\) PORTAL ==================== -->[\s\S]*?</div>\s*</div>\s*</div>'
    html = re.sub(admin_modal_pattern, '<!-- Client Mode: Admin portal excluded -->', html)

    # 4. Enhance User Gate into the Dedicated "Gmail PDF Sending Protocol" Modal
    old_gate_modal = r'<!-- ==================== USER VERIFICATION GATE MODAL \(PRE-PDF DOWNLOAD\) ==================== -->[\s\S]*?<!-- ==================== ADMIN SHIELD'
    
    new_gmail_modal = '''<!-- ==================== CLIENT GMAIL PDF DISPATCH PROTOCOL MODAL ==================== -->
<div class="fixed inset-0 bg-black/85 backdrop-blur-md z-50 hidden items-center justify-center p-4 no-print" id="userVerificationGateModal">
  <div class="holo-card max-w-lg w-full rounded-3xl p-6 sm:p-8 space-y-5 relative border border-amber-500/50 shadow-2xl shadow-amber-950/70 font-sans">
    
    <!-- Modal Header -->
    <div class="flex items-start justify-between border-b border-amber-500/25 pb-4">
      <div class="flex items-center space-x-3.5">
        <span class="text-3xl text-amber-400">✉️📜</span>
        <div>
          <h3 class="text-base sm:text-lg font-bold text-white flex items-center gap-2 font-mono">
            <span>CLINICAL DOSSIER GMAIL PROTOCOL</span>
          </h3>
          <span class="text-[11px] font-mono text-amber-300/90 uppercase tracking-widest">Secure PDF Generation &amp; Dispatch Protocol</span>
        </div>
      </div>
      <button class="w-8 h-8 rounded-lg bg-slate-900 border border-slate-700 hover:border-amber-400 text-slate-400 hover:text-white flex items-center justify-center text-sm font-mono transition" onclick="SecurityAdminEngine.closeUserVerificationModal()">✕</button>
    </div>

    <!-- Description -->
    <p class="text-xs text-slate-300 leading-relaxed font-mono">
      Your 3-Page Arcane Willow Assessment Dossier has been calculated. To generate your cryptographically sealed PDF and register your certificate, please enter your Gmail address:
    </p>

    <!-- Gmail Input Form -->
    <div class="space-y-3 font-mono text-xs">
      <div>
        <label class="block text-amber-300 text-[11px] font-bold mb-1.5 flex items-center justify-between">
          <span>ENTER YOUR GMAIL ADDRESS:</span>
          <span class="text-[10px] text-slate-400 font-normal">Required for official PDF seal</span>
        </label>
        <div class="relative">
          <input type="email" id="gateUserEmail" placeholder="your.name@gmail.com" class="w-full bg-slate-950 border border-slate-700 focus:border-amber-400 rounded-xl px-4 py-3 text-white text-sm outline-none transition placeholder-slate-600">
        </div>
      </div>

      <!-- Quick Helper Tag for Gmail -->
      <div class="flex items-center gap-2 pt-1 text-[11px]">
        <span class="text-slate-400">Quick append:</span>
        <button type="button" class="px-2 py-0.5 rounded bg-amber-950/70 border border-amber-500/40 text-amber-300 text-[10px] hover:bg-amber-900 transition" onclick="let input = document.getElementById('gateUserEmail'); if(!input.value.includes('@')) input.value += '@gmail.com';">
          + @gmail.com
        </button>
      </div>

      <!-- Consent & Dispatch Options -->
      <div class="p-3.5 rounded-xl bg-black/60 border border-amber-500/30 text-[11px] text-slate-300 space-y-2">
        <label class="flex items-start gap-2.5 cursor-pointer">
          <input type="checkbox" id="chkSendCopy" checked class="mt-0.5 rounded bg-slate-900 border-slate-700 text-amber-400 focus:ring-amber-400">
          <span class="leading-snug">
            <strong class="text-white block">Email Dispatch Protocol:</strong>
            Transmit a verified PDF certificate copy and verification hash to this Gmail address.
          </span>
        </label>
        <div class="text-[10px] text-emerald-400 flex items-center gap-1.5 border-t border-slate-800 pt-1.5">
          <span>🔒</span> <span>100% Privacy Compliance: Zero password storage. Only your verified email ID is securely recorded in the clinical registry.</span>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="pt-4 border-t border-amber-500/20 flex items-center justify-end gap-3">
      <button class="px-4 py-2.5 rounded-xl border border-slate-700 text-slate-400 text-xs font-mono hover:text-white transition" onclick="SecurityAdminEngine.closeUserVerificationModal()">
        Cancel
      </button>
      <button class="px-6 py-3 rounded-xl bg-gradient-to-r from-amber-400 via-yellow-400 to-amber-500 text-black font-extrabold text-xs font-mono tracking-wider transition shadow-lg shadow-amber-500/30 hover:brightness-110 active:scale-95 flex items-center gap-2" onclick="SecurityAdminEngine.confirmUserVerification()">
        <span>✦ CONFIRM GMAIL &amp; GENERATE DOSSIER</span>
      </button>
    </div>
  </div>
</div>
<!-- ==================== CLIENT MODE SPECIFICATION COMPLETE ==================== -->
'''

    # If old gate modal was found, replace it
    if '<!-- ==================== USER VERIFICATION GATE MODAL (PRE-PDF DOWNLOAD) ==================== -->' in html:
        # Search using string index
        m_start = html.find('<!-- ==================== USER VERIFICATION GATE MODAL (PRE-PDF DOWNLOAD) ==================== -->')
        m_end = html.find('</body>', m_start)
        html = html[:m_start] + new_gmail_modal + '\n</body>' + html[m_end + 7:]
        print("Replaced with dedicated Client Gmail Protocol Modal.")

    # Also add a client indicator script at end
    client_script = '''
<script>
  window.IS_CLIENT_PORTAL = true;
  console.log("NeuroMetric Client Portal Active: Admin controls locked & hidden.");
</script>
'''
    html = html.replace('</body>', client_script + '\n</body>')

    with open('client.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("SUCCESS: client.html created cleanly!")

if __name__ == '__main__':
    create_client()
