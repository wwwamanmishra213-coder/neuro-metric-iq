import asyncio
import os
import pymupdf # PyMuPDF
from playwright.async_api import async_playwright
from build_deluxe_html import get_deluxe_html

async def main():
    print("=== GENERATING IMMACULATE A4 VECTOR DOSSIER (DELUXE EDITION) ===", flush=True)

    candidate_data = {
        'email': 'aman20770101@gmail.com',
        'name': 'Aman Mishra',
        'fsiq': 138,
        'gai': 141,
        'percentile': 99.4,
        'date': 'OCTOBER 23, 2026',
        'cert_id': 'NM-2026-FSIQ-9942A',
        'status': 'VERIFIED ADULT N=2,200 (σ=15)',
        'factors': {
            'fluid': {'score': 142, 'percentile': 99.7},
            'workingMemory': {'score': 130, 'percentile': 97.7},
            'quantitative': {'score': 136, 'percentile': 99.2},
            'speed': {'score': 125, 'percentile': 95.0}
        },
        'telemetry': {
            'opticalStability': '95.4%',
            'saccadicLatency': '142 ms',
            'blinkRate': '14.2 /min',
            'dominantExpression': 'Focused / Analytical (68%)',
            'exprFocus': '68%',
            'exprStrain': '14%',
            'exprSatisfaction': '10%',
            'exprPerplexity': '8%',
            'facialTension': 'Low (16.2%)',
            'vocalPitch': '124.8 Hz',
            'vocalJitter': '0.38%',
            'affectiveStress': '18.4% (Nominal Baseline)',
            'status': 'WEBRTC LOCAL VOLATILE STREAM'
        },
        'reaction_time': '208ms',
        'inhibitory_braking': '50%',
        'commission_errors': '0',
        'responses': {
            'track_rage': "Integrity violations evoke an acute focus rather than impulsive hostility.",
            'track_mask': "Maintains high analytical discipline under evaluative cognitive load."
        }
    }

    html_content = get_deluxe_html(candidate_data)
    render_html_path = os.path.abspath('deluxe_exact_render.html')
    with open(render_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Written render HTML to: {render_html_path}", flush=True)

    dest_paths = [
        r"C:\Users\wwwam\Downloads\NeuroMetric_Clinical_Master_Dossier_Deluxe_A4.pdf",
        r"C:\Users\wwwam\Downloads\NeuroMetric_Arcane_Willow_Clinical_Dossier.pdf",
        os.path.abspath("NeuroMetric_Clinical_Master_Dossier_Deluxe_A4.pdf"),
        os.path.abspath("NeuroMetric_Arcane_Willow_Clinical_Dossier.pdf")
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1200, 'height': 1600})
        await page.goto(f"file:///{render_html_path.replace(os.sep, '/')}", wait_until='networkidle')
        await page.wait_for_timeout(1000)

        # Generate primary vector PDF
        primary_pdf = dest_paths[0]
        await page.pdf(
            path=primary_pdf,
            format='A4',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        )
        await browser.close()

    print(f"Primary Vector PDF created: {primary_pdf} ({os.path.getsize(primary_pdf)} bytes)", flush=True)

    # Copy to all target destinations
    with open(primary_pdf, 'rb') as f:
        pdf_bytes = f.read()

    for path in dest_paths[1:]:
        with open(path, 'wb') as f:
            f.write(pdf_bytes)
        print(f"Synchronized PDF destination: {path} ({len(pdf_bytes)} bytes)", flush=True)

    # Render High-Resolution Proof Previews using PyMuPDF
    doc = pymupdf.open(primary_pdf)
    artifact_dir = r"C:\Users\wwwam\.gemini\antigravity\brain\5d55040c-837b-4663-8bf0-2dfb1696f87e"
    print(f"Total Pages in Master Dossier: {len(doc)}", flush=True)

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        img_path = os.path.join(artifact_dir, f"deluxe_perfect_p{i+1}.png")
        pix.save(img_path)
        print(f"Rendered Folio {i+1} Preview: {img_path} ({pix.width}x{pix.height})", flush=True)

    print("=== VECTOR PDF GENERATION & MULTI-PAGE PROOFS READY ===", flush=True)

if __name__ == '__main__':
    asyncio.run(main())
