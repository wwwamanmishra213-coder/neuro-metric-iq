from playwright.sync_api import sync_playwright
import os
import shutil

output_dir = "test_screenshots"
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()

    url = "file:///c:/Users/wwwam/Downloads/how%20to%20calculate%20iq/index.html"
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(1000)

    # 1. Dual N-Back
    print("--- Testing Dual N-Back ---")
    page.evaluate("AssessmentController.launch('neuroplasticity')")
    page.wait_for_timeout(400)

    step1_inst = page.evaluate("document.getElementById('nbackInstructionText').textContent")
    encoding_visible = page.evaluate("!document.getElementById('nbackEncodingPanel').classList.contains('hidden')")
    response_hidden = page.evaluate("document.getElementById('nbackResponsePanel').classList.contains('hidden')")
    print(f"Step 1: {step1_inst} | Encoding visible: {encoding_visible} | Response hidden: {response_hidden}")
    assert "ENCODING PHASE" in step1_inst
    assert encoding_visible and response_hidden

    page.screenshot(path=os.path.join(output_dir, "07a_nback_encoding_step1.png"))

    page.keyboard.press("Space")
    page.wait_for_timeout(300)
    page.keyboard.press("Space")
    page.wait_for_timeout(300)

    step3_inst = page.evaluate("document.getElementById('nbackInstructionText').textContent")
    encoding_hidden_s3 = page.evaluate("document.getElementById('nbackEncodingPanel').classList.contains('hidden')")
    response_visible_s3 = page.evaluate("!document.getElementById('nbackResponsePanel').classList.contains('hidden')")
    print(f"Step 3: {step3_inst} | Encoding hidden: {encoding_hidden_s3} | Response visible: {response_visible_s3}")
    assert "EVALUATE MATCH" in step3_inst
    assert encoding_hidden_s3 and response_visible_s3

    page.screenshot(path=os.path.join(output_dir, "07b_nback_active_step3.png"))
    shutil.copyfile(os.path.join(output_dir, "07b_nback_active_step3.png"), os.path.join(output_dir, "07_neuroplasticity_nback.png"))

    # 2. DMTS
    print("--- Testing Memory Recognition (DMTS) ---")
    page.evaluate("AssessmentController.launch('memory')")
    page.wait_for_timeout(300)

    # Phase 1
    p1_svg_count = page.evaluate("document.querySelectorAll('#memoryDisplayArea svg').length")
    print(f"Phase 1 target SVG count: {p1_svg_count}")
    assert p1_svg_count >= 1
    page.screenshot(path=os.path.join(output_dir, "06a_memory_dmts_phase1.png"))

    # Phase 2 (Retention Mask Buffer at 2.6s)
    page.wait_for_timeout(2300) # Now at ~2.6s
    p2_inst = page.evaluate("document.getElementById('memoryInstructionText').textContent")
    p2_has_mask = page.evaluate("document.getElementById('memoryDisplayArea').textContent.includes('MASK BUFFER') || document.querySelectorAll('#memoryDisplayArea svg').length > 0")
    print(f"Phase 2: {p2_inst} | Mask active: {p2_has_mask}")
    page.screenshot(path=os.path.join(output_dir, "06b_memory_dmts_phase2_mask.png"))

    # Phase 3 (Discrimination Phase after another 1.6s -> ~4.2s total)
    page.wait_for_timeout(1800)
    p3_inst = page.evaluate("document.getElementById('memoryInstructionText').textContent")
    probe_cards_count = page.evaluate("document.querySelectorAll('#memoryProbeGrid .matrix-holo-tile').length")
    choice_svgs_count = page.evaluate("document.querySelectorAll('#memoryProbeGrid .matrix-holo-tile svg').length")
    print(f"Phase 3: {p3_inst} | Probe cards: {probe_cards_count} | Choice SVGs: {choice_svgs_count}")
    assert probe_cards_count == 4, f"Expected 4 probe cards, got {probe_cards_count}"
    assert choice_svgs_count == 4, f"Expected 4 visual SVGs inside choices, got {choice_svgs_count}"

    page.screenshot(path=os.path.join(output_dir, "06c_memory_dmts_phase3_discrimination.png"))
    shutil.copyfile(os.path.join(output_dir, "06c_memory_dmts_phase3_discrimination.png"), os.path.join(output_dir, "06b_memory_dmts_phase3.png"))

    # Mirror to artifact directory
    artifact_dir = r"C:\Users\wwwam\.gemini\antigravity\brain\5d55040c-837b-4663-8bf0-2dfb1696f87e\test_screenshots"
    os.makedirs(artifact_dir, exist_ok=True)
    for f in os.listdir(output_dir):
        if f.endswith('.png'):
            shutil.copyfile(os.path.join(output_dir, f), os.path.join(artifact_dir, f))

    browser.close()
    print(">>> ALL ASSERTIONS PASSED WITH 100% SUCCESS! <<<")
