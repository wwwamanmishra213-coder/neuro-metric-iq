import asyncio
from playwright.async_api import async_playwright
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

async def test_admin_password():
    print("=== TESTING ADMIN CORE PASSWORD: ak432$ ===", flush=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        page.on('pageerror', lambda e: print('PAGE ERROR:', e))

        admin_url = f"file:///{os.path.abspath('index.html').replace(os.sep, '/')}"
        await page.goto(admin_url, wait_until='networkidle')
        await page.wait_for_function('() => typeof window.SecurityAdminEngine !== "undefined"')

        # 1. Open Admin Portal Modal
        print("1. Opening Admin Portal Modal...", flush=True)
        await page.click('#headerAdminShieldBtn')
        await page.wait_for_timeout(500)

        modal_visible = await page.is_visible('#adminPortalModal')
        assert modal_visible, "Admin modal should be visible!"
        print("   -> Admin modal opened successfully.", flush=True)

        # 2. Test Invalid Password first
        print("2. Testing invalid password 'wrongpwd123'...", flush=True)
        await page.fill('#adminTotpInput', 'wrongpwd123')
        await page.click('button:has-text("Unlock Admin")')
        await page.wait_for_timeout(300)

        status_text = await page.text_content('#admin2FAStatus')
        print(f"   Status output on failure: '{status_text.strip()}'", flush=True)
        is_protected_hidden = await page.eval_on_selector('#adminProtectedSection', 'el => el.classList.contains("hidden")')
        assert is_protected_hidden, "Protected section must remain hidden on invalid password!"
        print("   -> Correct: Admin core remained locked.", flush=True)

        # 3. Test Valid Master Core Password: ak432$
        print("3. Testing Master Core Password 'ak432$'...", flush=True)
        await page.fill('#adminTotpInput', 'ak432$')
        await page.click('button:has-text("Unlock Admin")')
        await page.wait_for_timeout(500)

        status_success = await page.text_content('#admin2FAStatus')
        print(f"   Status output on success: '{status_success.strip()}'", flush=True)

        is_protected_visible = await page.eval_on_selector('#adminProtectedSection', 'el => !el.classList.contains("hidden")')
        assert is_protected_visible, "Protected admin console must be revealed upon correct password!"
        print("   -> CONFIRMED: Admin core unlocked with 'ak432$'!", flush=True)

        # 4. Check that Discord Webhook and Audit logs are accessible
        discord_input_visible = await page.is_visible('#adminDiscordUrlInput')
        print(f"   Discord Telemetry Console Visible: {discord_input_visible}", flush=True)

        # Take proof screenshot
        proof_path = r"C:\Users\wwwam\.gemini\antigravity\brain\5d55040c-837b-4663-8bf0-2dfb1696f87e\admin_password_unlocked_proof.png"
        await page.screenshot(path=proof_path)
        print(f"   Saved proof screenshot: {proof_path}", flush=True)

        await browser.close()
        print("\n=== ADMIN PASSWORD 'ak432$' FULLY VERIFIED! ===", flush=True)

if __name__ == '__main__':
    asyncio.run(test_admin_password())
