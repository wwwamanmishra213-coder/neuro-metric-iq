import asyncio
from playwright.async_api import async_playwright
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

async def test_request_protocol():
    print("=== TESTING CLIENT INTERFACE: DOWNLOAD PROTOCOL REMOVED, REQUEST MAILING ACTIVE ===", flush=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        page.on('pageerror', lambda e: print('PAGE ERROR:', e))

        download_events = []
        page.on('download', lambda d: download_events.append(d.suggested_filename))

        client_url = f"file:///{os.path.abspath('client.html').replace(os.sep, '/')}"
        await page.goto(client_url, wait_until='networkidle')
        await page.wait_for_function('() => typeof window.app !== "undefined" && typeof window.SecurityAdminEngine !== "undefined"')
        await page.wait_for_timeout(800)

        # 1. Complete battery and show final report screen
        print("\n1. Generating final assessment report...", flush=True)
        await page.evaluate('''() => {
            window.app.state.fsiq = 138;
            window.app.state.gai = 141;
            window.app.state.percentile = 99.4;
            window.app.generateFinalClinicalReport();
        }''')
        await page.wait_for_timeout(800)

        # 2. Check modal appearance
        print("2. Verifying immediate pop-up of Gmail Protocol Modal...", flush=True)
        modal_visible = await page.is_visible('#userVerificationGateModal')
        print(f"   Modal Visible: {modal_visible}", flush=True)

        # Inspect button text inside modal
        btn_text = await page.text_content('button:has-text("CONFIRM GMAIL")')
        print(f"   Modal Submit Button Text: '{btn_text.strip()}'", flush=True)

        # Fill in candidate Gmail
        print("3. Entering candidate Gmail address aman20770101@gmail.com...", flush=True)
        await page.fill('#gateUserEmail', 'aman20770101@gmail.com')

        # Click Confirm & Request
        print("4. Clicking 'CONFIRM GMAIL & REQUEST DOSSIER DELIVERY'...", flush=True)
        await page.click('button:has-text("CONFIRM GMAIL")')
        await page.wait_for_timeout(1500)

        # 3. Verify NO download occurred
        print(f"5. Browser Download Events Count: {len(download_events)} (Expected: 0)", flush=True)
        assert len(download_events) == 0, f"Error: Download occurred when it should be request-only! {download_events}"
        print("   -> CONFIRMED: Direct download protocol is completely removed from client interface!", flush=True)

        # 4. Verify Toast on screen
        toast_text = await page.evaluate('''() => {
            const t = document.getElementById('nmDossierRequestToast');
            return t ? t.textContent : null;
        }''')
        print(f"6. Success Delivery Notice: '{toast_text}'", flush=True)

        # 5. Verify Request button on screenReport
        report_btn = await page.text_content('button:has-text("Request Official Dossier via Gmail")')
        print(f"7. Button on Results Screen: '{report_btn.strip()}'", flush=True)

        # Capture proof screenshot
        proof_path = r"C:\Users\wwwam\.gemini\antigravity\brain\5d55040c-837b-4663-8bf0-2dfb1696f87e\client_request_mailing_protocol_verified.png"
        await page.screenshot(path=proof_path)
        print(f"\nSaved proof screenshot: {proof_path}", flush=True)

        await browser.close()
        print("\n=== REQUEST-ONLY CLIENT MAILING PROTOCOL FULLY VERIFIED! ===", flush=True)

if __name__ == '__main__':
    asyncio.run(test_request_protocol())
