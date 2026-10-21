import json
import os
import time
from playwright.sync_api import sync_playwright

output_dir = "test_screenshots"
os.makedirs(output_dir, exist_ok=True)

test_audit_data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()
    
    url = "file:///c:/Users/wwwam/Downloads/how%20to%20calculate%20iq/index.html"
    print(f"Loading {url}...")
    page.goto(url, wait_until='domcontentloaded')
    page.wait_for_timeout(1000)
    
    # Helper to capture state
    def capture(name, filename, action_description):
        path = os.path.join(output_dir, filename)
        page.screenshot(path=path)
        
        # Audit active headings and buttons
        headings = page.evaluate("Array.from(document.querySelectorAll('h1, h2, h3, h4')).filter(el => el.offsetParent !== null).map(el => el.innerText.trim())")
        visible_buttons = page.evaluate("Array.from(document.querySelectorAll('button')).filter(el => el.offsetParent !== null).map(el => el.innerText.trim().replace(/\\n/g, ' ')).filter(t => t.length > 0).slice(0, 10)")
        active_screen = page.evaluate("Array.from(document.querySelectorAll('section')).filter(el => !el.classList.contains('hidden')).map(el => el.id)")
        
        info = {
            "test_name": name,
            "filename": filename,
            "action": action_description,
            "active_screen": active_screen,
            "visible_headings": headings,
            "sample_buttons": visible_buttons
        }
        test_audit_data.append(info)
        print(f"[CAPTURED] {name} -> {filename}")
        print(f"  Screen: {active_screen} | Headings: {headings[:3]}")

    # 1. Landing Hub
    capture("Landing Dashboard Hub", "01_landing_hub.png", "Initial page load")
    
    # 2. CHC Subtest 1: Fluid Matrix (Gf)
    page.evaluate("AssessmentController.launch('iq')")
    page.wait_for_timeout(600)
    capture("CHC 01: Fluid Matrix Reasoning (Gf)", "02_fluid_matrix_gf.png", "Launched IQ Battery (Subtest 0)")
    
    # 3. CHC Subtest 2: Spatial Memory Corsi (Gwm)
    page.evaluate("app.loadSubtest(1)")
    page.wait_for_timeout(600)
    capture("CHC 02: Spatial Working Memory Corsi (Gwm)", "03_spatial_memory_gwm.png", "Loaded Corsi Block Span (Subtest 1)")
    
    # 4. CHC Subtest 3: Quantitative Induction (Gq)
    page.evaluate("app.loadSubtest(2)")
    page.wait_for_timeout(600)
    capture("CHC 03: Quantitative Induction (Gq)", "04_quantitative_gq.png", "Loaded Quantitative Series (Subtest 2)")
    
    # 5. CHC Subtest 4: Processing Speed (Gs)
    page.evaluate("app.loadSubtest(3)")
    page.wait_for_timeout(600)
    capture("CHC 04: Symbolic Processing Speed (Gs)", "05_processing_speed_gs.png", "Loaded Symbolic Processing Speed (Subtest 3)")
    
    # 6. Memory Recognition (DMTS)
    page.evaluate("AssessmentController.launch('memory')")
    page.wait_for_timeout(500)
    capture("Memory Recognition (DMTS) - Phase 1 Encoding", "06a_memory_dmts_phase1.png", "Launched Memory DMTS (Target Encoding)")
    
    # Wait for Probe Phase (2.5s encode + 1.2s mask)
    page.wait_for_timeout(3800)
    capture("Memory Recognition (DMTS) - Phase 3 Discrimination", "06b_memory_dmts_phase3.png", "DMTS Discrimination Phase (4 Choice Cards in viewport)")
    
    # 7. Neuroplasticity Tracker (Dual N-Back)
    page.evaluate("AssessmentController.launch('neuroplasticity')")
    page.wait_for_timeout(600)
    capture("Neuroplasticity Tracker (Dual N-Back)", "07_neuroplasticity_nback.png", "Launched Dual N-Back 3x3 Grid Tracker")
    
    # 8. Personality & Dark Triad Screener
    page.evaluate("AssessmentController.launch('darktriad')")
    page.wait_for_timeout(600)
    capture("Personality & Dark Triad Screener", "08_personality_darktriad.png", "Launched Dark Triad & Big Five Screener")
    
    # 9. Multiple Intelligences Inventory
    page.evaluate("AssessmentController.launch('multi_intelligence')")
    page.wait_for_timeout(600)
    capture("Howard Gardner Multiple Intelligences", "09_multiple_intelligences.png", "Launched Gardner 8-Factor Screener")
    
    # 10. Clinical Screener: ADHD (ASRS v1.1)
    page.evaluate("AssessmentController.launchClinical('adhd')")
    page.wait_for_timeout(600)
    capture("Clinical: ADHD Screener (ASRS v1.1)", "10_clinical_screener_adhd.png", "Launched WHO ASRS v1.1 Screener")
    
    # 11. Clinical Screener: OCD (OCI-R)
    page.evaluate("AssessmentController.launchClinical('ocd')")
    page.wait_for_timeout(600)
    capture("Clinical: OCD Inventory (OCI-R)", "11_clinical_screener_ocd.png", "Launched OCI-R Obsessive-Compulsive Screener")
    
    # 12. Clinical Screener: Schizotypy (SPQ-B)
    page.evaluate("AssessmentController.launchClinical('schizotypy')")
    page.wait_for_timeout(600)
    capture("Clinical: Schizotypal Screener (SPQ-B)", "12_clinical_screener_schizotypy.png", "Launched SPQ-B Screener")

    # 13. Clinical Dossier & Results Screen
    page.evaluate("app.generateFinalClinicalReport()")
    page.wait_for_timeout(800)
    capture("Final Clinical Dossier & Comprehensive Report", "13_final_clinical_report.png", "Generated Final Dossier with Bell Curve, Solved Problems & Routines")

    browser.close()

with open("test_audit_summary.json", "w", encoding="utf-8") as f:
    json.dump(test_audit_data, f, indent=2)

print("\nAll 13 real test states captured and audited successfully!")
