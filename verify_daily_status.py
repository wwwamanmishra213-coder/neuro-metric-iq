import asyncio
from playwright.async_api import async_playwright
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

async def test_daily_status_and_alarm():
    print("=== TESTING DAILY STATUS MANAGING TAB & PUSH ALARM PROTOCOL ===", flush=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        page.on('pageerror', lambda e: print('PAGE ERROR:', e))

        client_url = f"file:///{os.path.abspath('client.html').replace(os.sep, '/')}"
        await page.goto(client_url, wait_until='networkidle')
        await page.wait_for_function('() => typeof window.DailyStatusEngine !== "undefined"')

        # 1. Verify Header Button
        print("1. Checking Daily Status Header Button...", flush=True)
        btn_visible = await page.is_visible('#headerDailyStatusBtn')
        assert btn_visible, "Daily Status Header button must be visible!"
        print("   -> Header button verified.", flush=True)

        # 2. Click to open modal
        print("2. Opening Daily Status Manager modal...", flush=True)
        await page.click('#headerDailyStatusBtn')
        await page.wait_for_timeout(500)

        modal_visible = await page.is_visible('#dailyStatusModal')
        assert modal_visible, "Daily Status modal must open!"
        print("   -> Daily Status & Alarm modal opened successfully.", flush=True)

        # 3. Save a Daily Status log
        print("3. Logging daily status metrics (Energy 8, Focus 9, Sleep 8h)...", flush=True)
        await page.evaluate('''() => {
            const e = document.getElementById('statusEnergyRange');
            const f = document.getElementById('statusFocusRange');
            const s = document.getElementById('statusSleepHours');
            if (e) e.value = '8';
            if (f) f.value = '9';
            if (s) s.value = '8.0';
            DailyStatusEngine.saveDailyStatus();
        }''')
        await page.wait_for_timeout(400)

        # Verify toast and table row
        toast_text = await page.text_content('#nmDailyToast')
        print(f"   Toast notification: '{toast_text.strip()}'", flush=True)
        history_rows = await page.eval_on_selector_all('#dailyStatusHistoryBody tr', 'rows => rows.length')
        assert history_rows >= 1, "History table must display saved status!"
        print(f"   Saved history rows count: {history_rows}", flush=True)

        # 4. Set Alarm Protocol
        print("4. Configuring Daily Alarm Protocol (Time: 08:30)...", flush=True)
        await page.evaluate('''() => {
            const t = document.getElementById('alarmTimeInput');
            const toggle = document.getElementById('alarmEnableToggle');
            if (t) t.value = '08:30';
            if (toggle) toggle.checked = true;
            DailyStatusEngine.setAlarm();
        }''')
        await page.wait_for_timeout(500)

        alarm_pill = await page.text_content('#dailyAlarmHeaderPill')
        print(f"   Header Alarm Pill Updated: '{alarm_pill.strip()}'", flush=True)
        assert '08:30' in alarm_pill, f"Header pill should reflect scheduled alarm time, got: {alarm_pill}"

        # 5. Trigger synthetic alarm banner & chime
        print("5. Triggering Alarm Protocol Alert Banner...", flush=True)
        await page.evaluate('''() => {
            DailyStatusEngine.triggerAlarmAlert({ time: '08:30', label: 'Morning Cognitive Testing Protocol' });
        }''')
        await page.wait_for_timeout(500)

        banner_visible = await page.is_visible('#nmActiveAlarmBanner')
        assert banner_visible, "Active Alarm banner must be displayed!"
        print("   -> Alarm notification banner popped up successfully!", flush=True)

        # Capture proof screenshot
        proof_path = r"C:\Users\wwwam\.gemini\antigravity\brain\5d55040c-837b-4663-8bf0-2dfb1696f87e\daily_status_and_alarm_proof.png"
        await page.screenshot(path=proof_path)
        print(f"   Saved proof screenshot: {proof_path}", flush=True)

        await browser.close()
        print("\n=== DAILY STATUS TAB & ALARM PROTOCOL FULLY VERIFIED! ===", flush=True)

if __name__ == '__main__':
    asyncio.run(test_daily_status_and_alarm())
