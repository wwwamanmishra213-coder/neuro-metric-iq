import asyncio
import os
from playwright.async_api import async_playwright

async def verify_security_pipeline():
    print("Verifying Security & Admin Protocol in Browser...", flush=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            accept_downloads=True,
            viewport={'width': 1440, 'height': 900}
        )
        page = await context.new_page()

        fpath = os.path.abspath('index.html').replace('\\', '/')
        await page.goto(f'file:///{fpath}', wait_until='networkidle')
        await page.wait_for_timeout(1000)

        # 1. Test Admin Shield 2FA Modal
        print("Testing Admin Shield 2FA Button...", flush=True)
        await page.click('#headerAdminShieldBtn')
        await page.wait_for_timeout(500)
        assert await page.is_visible('#adminPortalModal'), "Admin modal not visible"

        # Fill 6-digit TOTP code
        await page.fill('#adminTotpInput', '842910')
        await page.click('button:has-text("Verify 2FA")')
        await page.wait_for_timeout(500)

        # Capture screenshot of unlocked admin console
        out_admin = 'C:/Users/wwwam/.gemini/antigravity/brain/5d55040c-837b-4663-8bf0-2dfb1696f87e/verified_admin_2fa_portal.png'
        await page.screenshot(path=out_admin)
        print("Saved Admin 2FA portal screenshot to:", out_admin)

        # Close Admin Modal
        await page.click('#adminPortalModal button:has-text("✕")')
        await page.wait_for_timeout(300)

        # 2. Test User Verification Gate before PDF Download
        print("Testing User Verification Gate before PDF Download...", flush=True)
        # Clear any stored user
        await page.evaluate('() => localStorage.removeItem("neurometric_current_user")')
        
        # Trigger exportClinicalPDF
        await page.evaluate('() => window.exportClinicalPDF()')
        await page.wait_for_timeout(500)

        # Verify Gate Modal is shown
        gate_visible = await page.is_visible('#userVerificationGateModal')
        print(f"User Gate Modal visible: {gate_visible}", flush=True)
        assert gate_visible, "User verification gate modal not shown"

        # Capture screenshot of User Verification Gate
        out_gate = 'C:/Users/wwwam/.gemini/antigravity/brain/5d55040c-837b-4663-8bf0-2dfb1696f87e/verified_user_gate_modal.png'
        await page.screenshot(path=out_gate)
        print("Saved User Gate modal screenshot to:", out_gate)

        # Fill candidate email and confirm
        await page.fill('#gateUserEmail', 'dr.wright@neuro-research.org')
        
        async with page.expect_download(timeout=60000) as download_info:
            await page.click('button:has-text("Seal & Generate PDF")')

        download = await download_info.value
        filename = download.suggested_filename
        print(f"Downloaded PDF via User Gate: {filename}", flush=True)

        # Check Audit Log in browser
        audit_log = await page.evaluate('() => window.SecurityAdminEngine.getAuditLog()')
        print(f"Total Audit Log Entries: {len(audit_log)}", flush=True)
        assert len(audit_log) > 0, "Audit log empty"
        print(f"Latest Candidate in Log: {audit_log[0]['email']} ({audit_log[0]['userId']})", flush=True)

        await browser.close()
        print("\nALL SECURITY & AUDIT PIPELINE VERIFICATIONS PASSED!", flush=True)

if __name__ == '__main__':
    asyncio.run(verify_security_pipeline())
