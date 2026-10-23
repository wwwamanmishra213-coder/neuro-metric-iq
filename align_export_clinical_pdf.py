def align_pdf_export():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    idx_start = html.find('const willowSvgOverlay = `')
    assert idx_start != -1, "willowSvgOverlay start not found"
    idx_end = html.find('`;', idx_start)
    assert idx_end != -1, "willowSvgOverlay end not found"

    new_svg_logic = '''// Dynamic Vector Border Protocol Integration (ISO 216 A4 Master Protocol)
      const getBorderSvg = (designId) => {
        if (window.PdfBorderProtocol && window.PdfBorderProtocol.generateSvg) {
          return window.PdfBorderProtocol.generateSvg(designId, 'portrait');
        }
        return '';
      };
      const borderFolio1 = getBorderSvg('sacred_mandala');
      const borderFolio2 = getBorderSvg('arcane_willow');
      const borderFolio3 = getBorderSvg('art_deco_chevron');'''

    html = html[:idx_start] + new_svg_logic + html[idx_end + 2:]
    print("Replaced static willowSvgOverlay with dynamic getBorderSvg calls.")

    assert html.count('${willowSvgOverlay}') == 3, f"Expected 3 occurrences, got {html.count('${willowSvgOverlay}')}"
    
    html = html.replace('${willowSvgOverlay}', '${borderFolio1}', 1)
    html = html.replace('${willowSvgOverlay}', '${borderFolio2}', 1)
    html = html.replace('${willowSvgOverlay}', '${borderFolio3}', 1)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("SUCCESS: index.html exportClinicalPDF fully aligned with Deluxe Master Protocol!")

if __name__ == '__main__':
    align_pdf_export()
