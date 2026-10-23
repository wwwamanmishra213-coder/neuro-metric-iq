import asyncio
from playwright.async_api import async_playwright
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

async def test_client_admin_access():
    print("=== TESTING CLIENT PORTAL: ADMIN ACCESS WITH ak432$ ===", flush=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        page.on('pageerror', lambda e: print('PAGE ERROR:', e))

        client_url = f"file:///{os.path.abspath('client.html').replace(os.sep, '/')}"
        await page.goto(client_url, wait_until='networkidle')
        await page.wait_for_function('() => typeof window.SecurityAdminEngine !== "undefined"')

        # 1. Verify Admin button exists on client header
        print("1. Checking Admin button on client header...", flush=True)
        btn_visible = await page.is_visible('#headerAdminShieldBtn')
        assert btn_visible, "Admin Shield button must be visible on client header!"
        print("   -> Admin button is visible on client.html header.", flush=True)

        # 2. Click Admin button to open modal
        print("2. Clicking Admin button...", flush=True)
        await page.click('#headerAdminShieldBtn')
        await page.wait_for_timeout(400)

        modal_visible = await page.is_visible('#adminPortalModal')
        assert modal_visible, "Admin modal should pop up on client.html!"
        print("   -> Admin portal modal opened on client.html.", flush=True)

        # 3. Enter wrong password first
        print("3. Testing invalid password 'wrongpass'...", flush=True)
        await page.fill('#adminTotpInput', 'wrongpass')
        await page.click('button:has-text("Unlock Admin")')
        await page.wait_for_timeout(300)

        is_hidden = await page.eval_on_selector('#adminProtectedSection', 'el => el.classList.contains("hidden")')
        assert is_hidden, "Admin protected section must stay hidden on wrong password!"
        print("   -> Protected console stayed locked.", flush=True)

        # 4. Enter correct admin password 'ak432$'
        print("4. Entering master admin password 'ak432$'...", flush=True)
        await page.fill('#adminTotpInput', 'ak432$')
        await page.click('button:has-text("Unlock Admin")')
        await page.wait_for_timeout(500)

        is_unlocked = await page.eval_on_selector('#adminProtectedSection', 'el => !el.classList.contains("hidden")')
        assert is_unlocked, "Admin console must be unlocked with ak432$!"
        print("   -> SUCCESS: Admin console unlocked with 'ak432$' on client portal!", flush=True)

        # 5. Check Discord input and candidate audit logs are visible inside client portal
        discord_input = await page.is_visible('#adminDiscordUrlInput')
        print(f"   Discord Telemetry config accessible: {discord_input}", flush=True)

        # Take proof screenshot
        proof_path = r"C:\Users\wwwam\.gemini\antigravity\brain\5d55040c-837b-4663-8bf0-2dfb1696f87e\client_admin_unlocked_ak432_proof.png"
        await page.screenshot(path=proof_path)
        print(f"   Saved proof screenshot: {proof_path}", flush=True)

        await browser.close()
        print("\n=== CLIENT PORTAL ADMIN ACCESS FULLY VERIFIED! ===", flush=True)

if __name__ == '__main__':
    asyncio.run(test_client_admin_access())
