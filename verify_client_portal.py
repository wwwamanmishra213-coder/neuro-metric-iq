import asyncio
import os
from playwright.async_api import async_playwright

async def verify_client():
    print("Testing Client Portal & Gmail PDF Protocol...", flush=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            accept_downloads=True,
            viewport={'width': 1440, 'height': 900}
        )
        page = await context.new_page()

        fpath = os.path.abspath('client.html').replace('\\', '/')
        await page.goto(f'file:///{fpath}', wait_until='networkidle')
        await page.wait_for_timeout(1000)

        # 1. Verify NO admin elements exist for client
        admin_btn = await page.query_selector('#headerAdminShieldBtn')
        admin_modal = await page.query_selector('#adminPortalModal')
        print(f"Admin Button present: {admin_btn is not None}", flush=True)
        print(f"Admin Modal present: {admin_modal is not None}", flush=True)
        assert admin_btn is None, "Admin button should NOT be in client.html"
        assert admin_modal is None, "Admin modal should NOT be in client.html"

        # 2. Trigger PDF export without user session
        print("Triggering PDF export to test Gmail Protocol Modal...", flush=True)
        await page.evaluate('() => localStorage.removeItem("neurometric_current_user")')
        await page.evaluate('() => window.exportClinicalPDF()')
        await page.wait_for_timeout(500)

        # 3. Verify Gmail Protocol Modal is visible
        modal_visible = await page.is_visible('#userVerificationGateModal')
        print(f"Gmail Protocol Modal visible: {modal_visible}", flush=True)
        assert modal_visible, "Gmail protocol modal not displayed"

        # 4. Fill in Gmail
        await page.fill('#gateUserEmail', 'candidate.client@gmail.com')

        # Screenshot of the Gmail Protocol Modal
        out_img = 'C:/Users/wwwam/.gemini/antigravity/brain/5d55040c-837b-4663-8bf0-2dfb1696f87e/client_gmail_protocol_preview.png'
        await page.screenshot(path=out_img)
        print("Saved Client Gmail Protocol screenshot to:", out_img, flush=True)

        # 5. Confirm and download PDF
        print("Confirming Gmail and generating PDF...", flush=True)
        async with page.expect_download(timeout=60000) as download_info:
            await page.click('button:has-text("CONFIRM GMAIL & GENERATE DOSSIER")')

        download = await download_info.value
        filename = download.suggested_filename
        print(f"Client Downloaded PDF: {filename}", flush=True)
        assert filename.endswith('.pdf'), "Downloaded file is not a PDF"

        await browser.close()
        print("\nALL CLIENT PORTAL VERIFICATIONS PASSED!", flush=True)

if __name__ == '__main__':
    asyncio.run(verify_client())
