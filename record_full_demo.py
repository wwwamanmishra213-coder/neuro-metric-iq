import os
from playwright.sync_api import sync_playwright

video_dir = os.path.abspath("test_videos")
os.makedirs(video_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={'width': 1280, 'height': 800},
        record_video_dir=video_dir,
        record_video_size={'width': 1280, 'height': 800}
    )
    page = context.new_page()

    url = "file:///c:/Users/wwwam/Downloads/how%20to%20calculate%20iq/index.html"
    print(f"Loading {url}...")
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(1000)

    # 1. Open the ChatGPT-style slide-out sidebar via the header button
    print("Opening sidebar drawer...")
    sidebar_toggle = page.locator("button[title*='Assessment Battery Drawer']")
    sidebar_toggle.click()
    page.wait_for_timeout(600)

    # 2. Click Memory Recognition (DMTS) Launch button inside the sidebar
    print("Clicking 'Launch Test' for Visual Memory Recognition (DMTS)...")
    dmts_btn = page.locator("aside#chatgptSidebar button[onclick*='memory']").first
    dmts_btn.click()
    page.wait_for_timeout(1000)

    # Phase 1: Target Matrix
    print("DMTS Phase 1 active...")
    page.wait_for_timeout(1800)

    # Phase 2: Mask Buffer
    print("DMTS Phase 2 Mask Buffer active...")
    page.wait_for_timeout(1600)

    # Phase 3: Discrimination Phase
    print("DMTS Phase 3 Discrimination active...")
    # Click Option B
    page.locator("#memoryProbeGrid .matrix-holo-tile").nth(1).click()
    page.wait_for_timeout(1000)

    # Exit back to Landing
    print("Exiting DMTS to Landing...")
    page.locator("#screenMemory button:has-text('Exit')").click()
    page.wait_for_timeout(800)

    # 3. Open Sidebar again
    print("Opening sidebar drawer again...")
    sidebar_toggle.click()
    page.wait_for_timeout(600)

    # 4. Click Neuroplasticity Tracker (Dual N-Back) Launch button inside the sidebar
    print("Clicking 'Launch Test' for Neuroplasticity Tracker (Dual N-Back)...")
    nback_btn = page.locator("aside#chatgptSidebar button[onclick*='neuroplasticity']").first
    nback_btn.click()
    page.wait_for_timeout(1000)

    # Step 1 Encoding Buffer
    print("N-Back Step 1 Encoding...")
    page.wait_for_timeout(800)
    # Advance via Spacebar
    print("Pressing Space to advance to Step 2...")
    page.keyboard.press("Space")
    page.wait_for_timeout(800)

    # Advance via Spacebar to Step 3
    print("Pressing Space to advance to Step 3 (Active)...")
    page.keyboard.press("Space")
    page.wait_for_timeout(1000)

    # Respond on Step 3 with key 'A'
    print("Pressing 'A' for Position Match on Step 3...")
    page.keyboard.press("a")
    page.wait_for_timeout(1000)

    # Exit back to menu
    print("Exiting N-Back to Landing...")
    page.locator("#screenNeuroplasticity button:has-text('Exit')").click()
    page.wait_for_timeout(1000)

    video_path = page.video.path()
    context.close()
    browser.close()

    final_video = os.path.join(video_dir, "NEURO_METRIC_FULL_DEMO_WALKTHROUGH.webm")
    if os.path.exists(final_video):
        os.remove(final_video)
    os.rename(video_path, final_video)
    print(f"Recorded full walkthrough video successfully: {final_video} ({os.path.getsize(final_video)} bytes)")
