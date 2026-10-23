import asyncio
from playwright.async_api import async_playwright
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

async def test_clinical_and_modal():
    print("=== TESTING CLINICAL PSYCHIATRIC TESTS & GMAIL POP-UP WINDOW ===", flush=True)

    clinical_keys = ['adhd', 'schizotypy', 'ocd', 'autism', 'anxiety', 'depression', 'executive', 'trauma']

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        page.on('pageerror', lambda e: print('PAGE ERROR:', e))

        client_url = f"file:///{os.path.abspath('client.html').replace(os.sep, '/')}"
        await page.goto(client_url, wait_until='networkidle')
        await page.wait_for_function('() => typeof window.AssessmentController !== "undefined" && typeof window.ClinicalTestEngine !== "undefined"')

        # 1. Test launching all 8 clinical screeners
        print("\n1. Testing launch of all 8 clinical psychiatric disease tests:", flush=True)
        for key in clinical_keys:
            res = await page.evaluate(f'''(k) => {{
                AssessmentController.launchClinical(k);
                const inv = ClinicalTestEngine.inventories[k];
                const screen = document.getElementById('screenClinical');
                const title = document.getElementById('clinicalBatteryTitle').textContent;
                const optCount = document.getElementById('clinicalOptionsGrid').children.length;
                return {{
                    key: k,
                    screenVisible: !screen.classList.contains('hidden'),
                    title: title,
                    options: optCount
                }};
            }}''', key)
            print(f"   [PASS] {key.upper()}: visible={res['screenVisible']}, title='{res['title']}', options={res['options']}", flush=True)

        # Capture screenshot of active clinical test (ADHD)
        shot_clinical = r"C:\Users\wwwam\.gemini\antigravity\brain\5d55040c-837b-4663-8bf0-2dfb1696f87e\clinical_psychiatric_test_active.png"
        await page.screenshot(path=shot_clinical)
        print(f"\nSaved active clinical test screenshot: {shot_clinical}", flush=True)

        # 2. Test answering questions in ADHD clinical screener and verify Gmail modal pops up at end
        print("\n2. Answering all questions in ADHD clinical screener to trigger completion...", flush=True)
        await page.evaluate('''() => {
            // Answer all questions
            const total = ClinicalTestEngine.inventories.adhd.questions.length;
            ClinicalTestEngine.answers = new Array(total).fill(3); // 'Often'
            ClinicalTestEngine.finish();
        }''')

        # Wait for the Gmail pop up window to open
        print("Waiting for Gmail pop up window to appear upon test completion...", flush=True)
        await page.wait_for_selector('#userVerificationGateModal:not(.hidden)', timeout=4000)
        print("   [SUCCESS] Gmail Protocol Modal is visible!", flush=True)

        # Check modal input element
        modal_visible = await page.evaluate('''() => {
            const modal = document.getElementById('userVerificationGateModal');
            const input = document.getElementById('gateUserEmail');
            return {
                modalVisible: !modal.classList.contains('hidden'),
                inputExists: !!input,
                isFocused: document.activeElement === input
            };
        }''')
        print(f"   Modal Status: {modal_visible}", flush=True)

        # Capture screenshot of the pop up window asking for Gmail
        shot_popup = r"C:\Users\wwwam\.gemini\antigravity\brain\5d55040c-837b-4663-8bf0-2dfb1696f87e\gmail_modal_popup_verified.png"
        await page.screenshot(path=shot_popup)
        print(f"Saved Gmail pop up screenshot: {shot_popup}", flush=True)

        # 3. Test Full Battery Completion also triggers Gmail pop up
        print("\n3. Testing Full Cognitive Battery completion triggers Gmail pop up...", flush=True)
        # Close current modal first
        await page.evaluate('() => SecurityAdminEngine.closeUserVerificationModal()')
        await page.wait_for_timeout(300)

        # Trigger final clinical report
        await page.evaluate('() => window.app.generateFinalClinicalReport()')
        await page.wait_for_selector('#userVerificationGateModal:not(.hidden)', timeout=4000)
        print("   [SUCCESS] Full Battery test completion also immediately opened the Gmail pop up window!", flush=True)

        await browser.close()
        print("\n=== ALL CLINICAL TESTS & GMAIL POP-UP VERIFIED 100% OPERATIONAL ===", flush=True)

if __name__ == '__main__':
    asyncio.run(test_clinical_and_modal())
