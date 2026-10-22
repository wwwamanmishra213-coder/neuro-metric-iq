"""
PROJECT: ARCANE WILLOW CODEX
Production-Ready Vector PDF Generation Engine using ReportLab
Creates a standalone, publication-quality A4 document with selectable text,
vector willow frames, and mathematical/scientific diagrams.
"""

import os
import math
from reportlab.lib import colors
from reportlab.lib.units import mm
pt = 1
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, Flowable, FrameBreak
)
from reportlab.graphics.shapes import Drawing, Rect, Circle, Ellipse, Line, Group, String

from design_config import (
    PAGE_WIDTH, PAGE_HEIGHT, MARGIN_LEFT, MARGIN_RIGHT, MARGIN_TOP, MARGIN_BOTTOM,
    USABLE_WIDTH, USABLE_HEIGHT,
    COLOR_OBSIDIAN, COLOR_CHARCOAL, COLOR_ANTIQUE_GOLD, COLOR_BRIGHT_GOLD,
    COLOR_BRONZE, COLOR_PARCHMENT, COLOR_MUTED_SILVER, COLOR_BODY_TEXT,
    COLOR_CYAN_ACCENT, COLOR_RUBY_ACCENT,
    FONT_DISPLAY, FONT_HEADING, FONT_BODY, FONT_BODY_ITALIC, FONT_TECH, FONT_TECH_BOLD, FONT_MATH
)


# ==========================================================================
# 1. VECTOR WILLOW FRAME & DECORATIVE BACKGROUND CANVAS RENDERER
# ==========================================================================
def draw_willow_background(canvas, doc):
    canvas.saveState()

    # 1. Base Obsidian Background
    canvas.setFillColor(COLOR_OBSIDIAN)
    canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    # 2. Outer & Inner Double Metallic-Gold Borders
    # Outer Border (28pt inset from edges)
    bx = 10 * mm
    by = 10 * mm
    bw = PAGE_WIDTH - 20 * mm
    bh = PAGE_HEIGHT - 20 * mm

    canvas.setStrokeColor(COLOR_ANTIQUE_GOLD)
    canvas.setLineWidth(1.2)
    canvas.rect(bx, by, bw, bh, fill=0, stroke=1)

    # Inner Fine Border (3mm further inside)
    ix = bx + 2.5 * mm
    iy = by + 2.5 * mm
    iw = bw - 5.0 * mm
    ih = bh - 5.0 * mm

    canvas.setStrokeColor(COLOR_BRIGHT_GOLD)
    canvas.setLineWidth(0.6)
    canvas.rect(ix, iy, iw, ih, fill=0, stroke=1)

    # 3. Corner Brackets & Sacred Geometry Nodes
    corners = [
        (ix, iy + ih, 1, -1),      # Top-Left
        (ix + iw, iy + ih, -1, -1), # Top-Right
        (ix, iy, 1, 1),             # Bottom-Left
        (ix + iw, iy, -1, 1)        # Bottom-Right
    ]

    for cx, cy, dx, dy in corners:
        canvas.setStrokeColor(COLOR_BRIGHT_GOLD)
        canvas.setLineWidth(1.4)
        p = canvas.beginPath()
        p.moveTo(cx, cy + dy * 12 * mm)
        p.lineTo(cx, cy)
        p.lineTo(cx + dx * 12 * mm, cy)
        canvas.drawPath(p, fill=0, stroke=1)

        # Luminous Gold Node
        canvas.setFillColor(COLOR_BRIGHT_GOLD)
        canvas.circle(cx, cy, 2.5, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.circle(cx, cy, 1.0, fill=1, stroke=0)

    # 4. Vector Willow Branches & Leaves
    # Helper to draw a single willow leaf with vein
    def draw_leaf(lx, ly, angle_deg, scale=1.0):
        canvas.saveState()
        canvas.translate(lx, ly)
        canvas.rotate(angle_deg)
        canvas.scale(scale, scale)

        canvas.setFillColor(COLOR_ANTIQUE_GOLD)
        canvas.setStrokeColor(COLOR_BRONZE)
        canvas.setLineWidth(0.4)

        # Lanceolate curved leaf path
        lp = canvas.beginPath()
        lp.moveTo(0, 0)
        lp.curveTo(3, -5, 4, -12, 0, -18)
        lp.curveTo(-4, -12, -3, -5, 0, 0)
        canvas.drawPath(lp, fill=1, stroke=1)

        # Central vein highlight
        canvas.setStrokeColor(COLOR_PARCHMENT)
        canvas.setLineWidth(0.3)
        canvas.line(0, -1, 0, -16)

        canvas.restoreState()

    # Top-Left Willow Branch
    canvas.setStrokeColor(COLOR_ANTIQUE_GOLD)
    canvas.setLineWidth(1.4)
    bp1 = canvas.beginPath()
    bp1.moveTo(ix, iy + ih)
    bp1.curveTo(ix + 15 * mm, iy + ih - 6 * mm, ix + 35 * mm, iy + ih - 4 * mm, ix + 55 * mm, iy + ih - 10 * mm)
    canvas.drawPath(bp1, fill=0, stroke=1)

    # Secondary cascading tendril
    canvas.setLineWidth(0.7)
    bp2 = canvas.beginPath()
    bp2.moveTo(ix + 15 * mm, iy + ih - 6 * mm)
    bp2.curveTo(ix + 18 * mm, iy + ih - 25 * mm, ix + 12 * mm, iy + ih - 45 * mm, ix + 14 * mm, iy + ih - 70 * mm)
    canvas.drawPath(bp2, fill=0, stroke=1)

    # Top-Left Leaves
    draw_leaf(ix + 15 * mm, iy + ih - 6 * mm, 45, 0.9)
    draw_leaf(ix + 28 * mm, iy + ih - 4 * mm, 25, 1.0)
    draw_leaf(ix + 42 * mm, iy + ih - 7 * mm, 15, 0.8)
    draw_leaf(ix + 54 * mm, iy + ih - 10 * mm, -10, 0.7)

    # Hanging leaves down the left margin
    draw_leaf(ix + 16 * mm, iy + ih - 22 * mm, 170, 0.85)
    draw_leaf(ix + 14 * mm, iy + ih - 38 * mm, 178, 0.95)
    draw_leaf(ix + 13 * mm, iy + ih - 54 * mm, 168, 0.8)
    draw_leaf(ix + 14 * mm, iy + ih - 70 * mm, 175, 0.75)

    # Top-Right Willow Branch
    canvas.setStrokeColor(COLOR_ANTIQUE_GOLD)
    canvas.setLineWidth(1.4)
    bp3 = canvas.beginPath()
    bp3.moveTo(ix + iw, iy + ih)
    bp3.curveTo(ix + iw - 15 * mm, iy + ih - 6 * mm, ix + iw - 35 * mm, iy + ih - 4 * mm, ix + iw - 55 * mm, iy + ih - 10 * mm)
    canvas.drawPath(bp3, fill=0, stroke=1)

    canvas.setLineWidth(0.7)
    bp4 = canvas.beginPath()
    bp4.moveTo(ix + iw - 15 * mm, iy + ih - 6 * mm)
    bp4.curveTo(ix + iw - 18 * mm, iy + ih - 25 * mm, ix + iw - 12 * mm, iy + ih - 45 * mm, ix + iw - 14 * mm, iy + ih - 70 * mm)
    canvas.drawPath(bp4, fill=0, stroke=1)

    draw_leaf(ix + iw - 15 * mm, iy + ih - 6 * mm, -45, 0.9)
    draw_leaf(ix + iw - 28 * mm, iy + ih - 4 * mm, -25, 1.0)
    draw_leaf(ix + iw - 42 * mm, iy + ih - 7 * mm, -15, 0.8)
    draw_leaf(ix + iw - 54 * mm, iy + ih - 10 * mm, 10, 0.7)

    draw_leaf(ix + iw - 16 * mm, iy + ih - 22 * mm, -170, 0.85)
    draw_leaf(ix + iw - 14 * mm, iy + ih - 38 * mm, -178, 0.95)
    draw_leaf(ix + iw - 13 * mm, iy + ih - 54 * mm, -168, 0.8)
    draw_leaf(ix + iw - 14 * mm, iy + ih - 70 * mm, -175, 0.75)

    # Bottom Branches
    draw_leaf(ix + 12 * mm, iy + 25 * mm, 10, 0.85)
    draw_leaf(ix + 14 * mm, iy + 45 * mm, -5, 0.8)
    draw_leaf(ix + iw - 12 * mm, iy + 25 * mm, -10, 0.85)
    draw_leaf(ix + iw - 14 * mm, iy + 45 * mm, 5, 0.8)

    # 5. Top Center Emblem (Mandala + Atom + Willow Leaf)
    emblem_x = PAGE_WIDTH / 2.0
    emblem_y = iy + ih
    canvas.setStrokeColor(COLOR_ANTIQUE_GOLD)
    canvas.setFillColor(COLOR_OBSIDIAN)
    canvas.circle(emblem_x, emblem_y, 4 * mm, fill=1, stroke=1)
    canvas.setFillColor(COLOR_BRIGHT_GOLD)
    canvas.circle(emblem_x, emblem_y, 1.2 * mm, fill=1, stroke=0)

    # 6. Running Header Line & Academic Typography
    header_y = PAGE_HEIGHT - 17 * mm
    canvas.setStrokeColor(COLOR_ANTIQUE_GOLD)
    canvas.setLineWidth(0.6)
    canvas.line(ix + 6 * mm, header_y, ix + iw - 6 * mm, header_y)

    canvas.setFont(FONT_DISPLAY, 7.5)
    canvas.setFillColor(COLOR_ANTIQUE_GOLD)
    canvas.drawString(ix + 6 * mm, header_y + 2.5 * mm, "THE ARCANE WILLOW CODEX")

    canvas.setFont(FONT_TECH, 7)
    canvas.setFillColor(COLOR_MUTED_SILVER)
    canvas.drawRightString(ix + iw - 6 * mm, header_y + 2.5 * mm, "FASCICULUS ASTRONOMICA · FOLIO II")

    # 7. Running Footer
    footer_y = 15 * mm
    canvas.setStrokeColor(COLOR_ANTIQUE_GOLD)
    canvas.setLineWidth(0.6)
    canvas.line(ix + 6 * mm, footer_y, ix + iw - 6 * mm, footer_y)

    canvas.setFont(FONT_TECH, 6.5)
    canvas.setFillColor(COLOR_MUTED_SILVER)
    canvas.drawString(ix + 6 * mm, footer_y - 3.5 * mm, "LIBER MECHANICA COELESTIS · VOL. I")

    canvas.setFont(FONT_DISPLAY, 7.5)
    canvas.setFillColor(COLOR_BRIGHT_GOLD)
    canvas.drawCentredString(PAGE_WIDTH / 2.0, footer_y - 3.5 * mm, "PAGE 14")

    canvas.setFont(FONT_TECH, 6.5)
    canvas.setFillColor(COLOR_MUTED_SILVER)
    canvas.drawRightString(ix + iw - 6 * mm, footer_y - 3.5 * mm, "ORDINE SALICIS ARCHIVUM")

    canvas.restoreState()


# ==========================================================================
# 2. ORIGINAL VECTOR SCIENTIFIC DIAGRAMS IN REPORTLAB
# ==========================================================================

class OrbitalDiagramFlowable(Flowable):
    """
    Scientific Diagram 1: Keplerian orbital mechanics with central mass M,
    orbiting body m, velocity and gravitational force vectors.
    """
    def __init__(self, width=220, height=130):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        canv = self.canv
        canv.saveState()

        # Diagram Card Background
        canv.setFillColor(COLOR_CHARCOAL)
        canv.setStrokeColor(COLOR_BRONZE)
        canv.setLineWidth(0.75)
        canv.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=1)

        # Coordinate axes & circular reference orbit
        ox, oy = self.width * 0.42, self.height * 0.50
        canv.setStrokeColor(COLOR_MUTED_SILVER)
        canv.setLineWidth(0.4)
        canv.circle(ox, oy, 40, fill=0, stroke=1)

        # Keplerian Ellipse (Centered at ox + 14, oy, a=56, b=38)
        canv.setStrokeColor(COLOR_ANTIQUE_GOLD)
        canv.setLineWidth(1.3)
        cx, cy = ox + 14, oy
        a, b = 58, 40
        # Draw ellipse via path
        p = canv.beginPath()
        for deg in range(0, 361, 5):
            rad = math.radians(deg)
            px = cx + a * math.cos(rad)
            py = cy + b * math.sin(rad)
            if deg == 0:
                p.moveTo(px, py)
            else:
                p.lineTo(px, py)
        canv.drawPath(p, fill=0, stroke=1)

        # Central Gravitating Body M at Focus (ox, oy)
        canv.setFillColor(COLOR_BRIGHT_GOLD)
        canv.circle(ox, oy, 8, fill=1, stroke=0)
        canv.setFillColor(colors.white)
        canv.circle(ox, oy, 4, fill=1, stroke=0)
        canv.setFont(FONT_DISPLAY, 7.5)
        canv.setFillColor(COLOR_BRIGHT_GOLD)
        canv.drawString(ox - 3, oy - 14, "M")

        # Orbiting Body m at theta = 60 deg
        bx = cx + a * math.cos(math.radians(55))
        by = cy + b * math.sin(math.radians(55))

        # Radius line r
        canv.setStrokeColor(COLOR_BRIGHT_GOLD)
        canv.setLineWidth(0.7)
        canv.line(ox, oy, bx, by)
        canv.setFont(FONT_BODY_ITALIC, 7)
        canv.drawString((ox + bx)/2 - 8, (oy + by)/2 + 2, "r")

        # Body m
        canv.setFillColor(COLOR_PARCHMENT)
        canv.circle(bx, by, 3.5, fill=1, stroke=0)
        canv.setFont(FONT_TECH_BOLD, 7)
        canv.setFillColor(COLOR_BODY_TEXT)
        canv.drawString(bx + 5, by - 2, "m")

        # Velocity Vector v (tangent ~ Cyan)
        canv.setStrokeColor(COLOR_CYAN_ACCENT)
        canv.setLineWidth(1.4)
        vx, vy = bx - 22, by + 12
        canv.line(bx, by, vx, vy)
        canv.setFont(FONT_TECH_BOLD, 6.5)
        canv.setFillColor(COLOR_CYAN_ACCENT)
        canv.drawString(vx - 6, vy + 2, "v")

        # Gravitational Force Vector F_g (Ruby ~ pointing to M)
        canv.setStrokeColor(COLOR_RUBY_ACCENT)
        canv.setLineWidth(1.4)
        fx = bx - (bx - ox) * 0.45
        fy = by - (by - oy) * 0.45
        canv.line(bx, by, fx, fy)
        canv.setFont(FONT_TECH_BOLD, 6.5)
        canv.setFillColor(COLOR_RUBY_ACCENT)
        canv.drawString(fx - 4, fy - 6, "Fg")

        # Caption Line at Bottom
        canv.setFont(FONT_TECH, 6)
        canv.setFillColor(COLOR_MUTED_SILVER)
        canv.drawString(8, 8, "Fig 2.1: Keplerian kinematics with vectors Fg and v.")

        canv.restoreState()


class SpacetimeDiagramFlowable(Flowable):
    """
    Scientific Diagram 2: General Relativistic spacetime metric curvature (g_μν)
    funnel and photon null geodesic deflection.
    """
    def __init__(self, width=220, height=115):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        canv = self.canv
        canv.saveState()

        # Card Background
        canv.setFillColor(COLOR_CHARCOAL)
        canv.setStrokeColor(COLOR_BRONZE)
        canv.setLineWidth(0.75)
        canv.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=1)

        # Curvature Funnel Coordinate Rings
        cx = self.width * 0.5
        levels = [
            (cx, 85, 95, 16, 0.4, COLOR_MUTED_SILVER),
            (cx, 72, 75, 13, 0.6, COLOR_ANTIQUE_GOLD),
            (cx, 58, 55, 10, 0.8, COLOR_ANTIQUE_GOLD),
            (cx, 44, 35, 7, 0.9, COLOR_BRIGHT_GOLD),
            (cx, 32, 18, 4, 1.2, COLOR_BRIGHT_GOLD),
        ]

        for lx, ly, rx, ry, lw, col in levels:
            canv.setStrokeColor(col)
            canv.setLineWidth(lw)
            p = canv.beginPath()
            for deg in range(0, 361, 10):
                rad = math.radians(deg)
                px = lx + rx * math.cos(rad)
                py = ly + ry * math.sin(rad)
                if deg == 0:
                    p.moveTo(px, py)
                else:
                    p.lineTo(px, py)
            canv.drawPath(p, fill=0, stroke=1)

        # Funnel Vertical Geodesic Warp Ribs
        canv.setStrokeColor(COLOR_ANTIQUE_GOLD)
        canv.setLineWidth(0.5)
        for offset_x in [-80, -50, -25, 25, 50, 80]:
            p = canv.beginPath()
            p.moveTo(cx + offset_x, 85)
            p.curveTo(cx + offset_x * 0.6, 65, cx + offset_x * 0.3, 45, cx + offset_x * 0.15, 32)
            canvas = canv.drawPath(p, fill=0, stroke=1)

        # Central Mass M in Potential Well
        canv.setFillColor(COLOR_BRIGHT_GOLD)
        canv.circle(cx, 32, 6, fill=1, stroke=0)
        canv.setFillColor(colors.white)
        canv.circle(cx, 32, 2.5, fill=1, stroke=0)
        canv.setFont(FONT_DISPLAY, 6.5)
        canv.setFillColor(COLOR_BRIGHT_GOLD)
        canv.drawString(cx - 3, 20, "M")

        # Deflected Light Ray (Photon Geodesic ~ Cyan)
        canv.setStrokeColor(COLOR_CYAN_ACCENT)
        canv.setLineWidth(1.3)
        lp = canv.beginPath()
        lp.moveTo(15, 96)
        lp.curveTo(cx - 30, 96, cx, 75, cx + 30, 96)
        lp.lineTo(self.width - 15, 96)
        canv.drawPath(lp, fill=0, stroke=1)

        canv.setFont(FONT_TECH_BOLD, 6)
        canv.setFillColor(COLOR_CYAN_ACCENT)
        canv.drawString(18, 101, "Photon Geodesic (Δθ = 4GM/c²b)")

        # Caption
        canv.setFont(FONT_TECH, 6)
        canv.setFillColor(COLOR_MUTED_SILVER)
        canv.drawString(8, 7, "Fig 2.2: Relativistic metric tensor warp g_μν around mass M.")

        canv.restoreState()


# ==========================================================================
# 3. BUILD PRODUCTION PDF DOCUMENT (TWO-COLUMN ACADEMIC CODEX)
# ==========================================================================

def build_codex_pdf(output_path=None):
    if output_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(base_dir, "output", "sample-codex.pdf")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    doc = BaseDocTemplate(
        output_path,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM
    )

    # Calculate Balanced Two-Column Frames
    content_top = PAGE_HEIGHT - 54 * mm
    content_height = content_top - 22 * mm
    col_gap = 5.5 * mm
    col_width = (USABLE_WIDTH - col_gap) / 2.0

    frame_left = Frame(
        MARGIN_LEFT, 22 * mm, col_width, content_height,
        id='col_left', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
    )
    frame_right = Frame(
        MARGIN_LEFT + col_width + col_gap, 22 * mm, col_width, content_height,
        id='col_right', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
    )

    page_template = PageTemplate(
        id='codex_page',
        frames=[frame_left, frame_right],
        onPage=draw_willow_background
    )
    doc.addPageTemplates([page_template])

    # 4. Academic Editorial Typography Styles
    styles = {
        'ChapterNum': ParagraphStyle(
            'ChapterNum',
            fontName=FONT_DISPLAY,
            fontSize=8,
            leading=10,
            textColor=COLOR_ANTIQUE_GOLD,
            alignment=1, # Center
            spaceAfter=2
        ),
        'ChapterTitle': ParagraphStyle(
            'ChapterTitle',
            fontName=FONT_DISPLAY,
            fontSize=15,
            leading=18,
            textColor=COLOR_BRIGHT_GOLD,
            alignment=1,
            spaceAfter=3
        ),
        'ChapterSubtitle': ParagraphStyle(
            'ChapterSubtitle',
            fontName=FONT_BODY_ITALIC,
            fontSize=9,
            leading=12,
            textColor=COLOR_PARCHMENT,
            alignment=1,
            spaceAfter=10
        ),
        'SectionHeader': ParagraphStyle(
            'SectionHeader',
            fontName=FONT_HEADING,
            fontSize=10,
            leading=13,
            textColor=COLOR_BRIGHT_GOLD,
            spaceBefore=6,
            spaceAfter=3,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body',
            fontName=FONT_BODY,
            fontSize=7.2,
            leading=10.2,
            textColor=COLOR_BODY_TEXT,
            alignment=4, # Justified
            spaceAfter=5
        ),
        'Epigraph': ParagraphStyle(
            'Epigraph',
            fontName=FONT_BODY_ITALIC,
            fontSize=7.2,
            leading=9.8,
            textColor=COLOR_PARCHMENT,
            spaceAfter=3
        ),
        'EpigraphCite': ParagraphStyle(
            'EpigraphCite',
            fontName=FONT_TECH,
            fontSize=5.8,
            leading=8,
            textColor=COLOR_ANTIQUE_GOLD,
            alignment=2 # Right
        ),
        'MathFormula': ParagraphStyle(
            'MathFormula',
            fontName=FONT_MATH,
            fontSize=9.5,
            leading=13,
            textColor=COLOR_BRIGHT_GOLD,
            alignment=1,
            spaceBefore=2,
            spaceAfter=2
        ),
        'MathNote': ParagraphStyle(
            'MathNote',
            fontName=FONT_TECH,
            fontSize=6,
            leading=8.5,
            textColor=COLOR_MUTED_SILVER,
            spaceAfter=4
        ),
        'AppBullet': ParagraphStyle(
            'AppBullet',
            fontName=FONT_TECH,
            fontSize=6.2,
            leading=8.8,
            textColor=COLOR_BODY_TEXT,
            spaceAfter=3
        )
    }

    story = []

    # ==================== LEFT COLUMN CONTENT ====================
    # Chapter Title Header (Top of Left Column flow)
    story.append(Paragraph("CHAPTER 02", styles['ChapterNum']))
    story.append(Paragraph("THE ORBITAL PRINCIPLE", styles['ChapterTitle']))
    story.append(Paragraph("✦ &nbsp; Gravity, Motion and the Harmony of Chaos &nbsp; ✦", styles['ChapterSubtitle']))

    # 2.1 Introduction
    story.append(Paragraph("<b>2.1 &nbsp; INTRODUCTION</b>", styles['SectionHeader']))
    story.append(Paragraph(
        "The equilibrium of celestial architecture rests upon an exquisite tension: the perpetual curvature "
        "of motion under the dominion of mutual attraction. When a celestial body traverses a gravitational field, "
        "its trajectory ceases to be rectilinear; space itself instructs the mass how to travel, whilst mass commands "
        "the geometry of space to bend. Rather than a static confinement, an orbit represents a dynamic state of "
        "perpetual free-fall, wherein forward momentum precisely balances gravitational descent.",
        styles['Body']
    ))

    # Epigraph Quotation Box
    epigraph_content = [
        [Paragraph("“When the celestial branches sway in the quiet of the void, each leaf tracks a path decreed not by whim, but by the immutable curvature of the unseen.”", styles['Epigraph'])],
        [Paragraph("— Archival Fragment IV, Order of the Golden Willow", styles['EpigraphCite'])]
    ]
    epigraph_table = Table(epigraph_content, colWidths=[col_width])
    epigraph_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_CHARCOAL),
        ('BOX', (0, 0), (-1, -1), 0.75, COLOR_BRONZE),
        ('LINELEFT', (0, 0), (0, -1), 2.0, COLOR_ANTIQUE_GOLD),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(epigraph_table)
    story.append(Spacer(1, 4))

    # 2.2 Mathematical Formulation
    story.append(Paragraph("<b>2.2 &nbsp; MATHEMATICAL FORMULATION</b>", styles['SectionHeader']))
    story.append(Paragraph(
        "Under classical Newtonian dynamics, the mutual gravitational attraction force <i>F</i> between two masses "
        "<i>m</i>₁ and <i>m</i>₂ separated by distance <i>r</i> follows the universal inverse-square law:",
        styles['Body']
    ))

    # Equation 1 Table
    eq1_data = [
        [Paragraph("<i>F</i> &nbsp; = &nbsp; <i>G · m₁ · m₂</i> &nbsp;/&nbsp; <i>r</i>²", styles['MathFormula'])],
        [Paragraph("Where <i>G</i> = 6.67430 × 10⁻¹¹ m³ · kg⁻¹ · s⁻² denotes the gravitational constant.", styles['MathNote'])]
    ]
    eq1_table = Table(eq1_data, colWidths=[col_width])
    eq1_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_CHARCOAL),
        ('BOX', (0, 0), (-1, -1), 0.5, COLOR_BRONZE),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(eq1_table)
    story.append(Spacer(1, 3))

    story.append(Paragraph(
        "For an orbiting body of mass <i>m</i> maintaining a stable circular trajectory of radius <i>r</i> around primary body <i>M</i>, "
        "equating gravitational force to centripetal acceleration yields the fundamental circular velocity:",
        styles['Body']
    ))

    # Equation 2 Table
    eq2_data = [
        [Paragraph("<i>v</i> &nbsp; = &nbsp; √( <i>G · M</i> &nbsp;/&nbsp; <i>r</i> )", styles['MathFormula'])],
        [Paragraph("<b>v</b>: orbital speed (m·s⁻¹) &nbsp;·&nbsp; <b>M</b>: central mass (kg) &nbsp;·&nbsp; <b>r</b>: orbital radius (m)", styles['MathNote'])]
    ]
    eq2_table = Table(eq2_data, colWidths=[col_width])
    eq2_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_CHARCOAL),
        ('BOX', (0, 0), (-1, -1), 0.5, COLOR_BRONZE),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(eq2_table)
    story.append(Spacer(1, 4))

    # Figure 2.2: Spacetime Diagram
    story.append(SpacetimeDiagramFlowable(width=col_width, height=98))

    # ==================== FRAME BREAK TO RIGHT COLUMN ====================
    story.append(FrameBreak())

    # Figure 2.1: Orbital Mechanics Diagram (Top of Right Column)
    story.append(OrbitalDiagramFlowable(width=col_width, height=110))
    story.append(Spacer(1, 4))

    # 2.3 Orbits and Stability
    story.append(Paragraph("<b>2.3 &nbsp; ORBITS AND STABILITY</b>", styles['SectionHeader']))
    story.append(Paragraph(
        "The morphological persistence of an orbit is dictated by conservation of specific mechanical energy "
        "(ε = <i>v</i>²/2 − <i>GM/r</i>) and specific angular momentum (<b>h</b> = <b>r</b> × <b>v</b>). "
        "In an idealized Keplerian two-body potential, trajectories form planar conic sections with eccentricity 0 ≤ <i>e</i> &lt; 1.",
        styles['Body']
    ))
    story.append(Paragraph(
        "Real-world astrophysical trajectories undergo continuous secular perturbations stemming from oblateness (<i>J₂</i> harmonic), "
        "relativistic pericenter precession, and multi-body gravitational resonances. Orbital integrity persists through resonance-locking "
        "and bounded phase-space libration.",
        styles['Body']
    ))

    # 2.4 Real-World Applications
    story.append(Paragraph("<b>2.4 &nbsp; REAL-WORLD APPLICATIONS</b>", styles['SectionHeader']))
    story.append(Paragraph(
        "The mathematical formalisms of celestial orbital dynamics govern foundational technologies across modern space science:",
        styles['Body']
    ))

    apps = [
        "<b>✦ Global Satellite Navigation:</b> Positioning constellations (GPS/Galileo) operating at MEO incorporating +38.6 μs/day General Relativistic clock corrections.",
        "<b>✦ Interplanetary Trajectory Design:</b> Hohmann coplanar transfer orbits, bi-elliptic maneuvers, and gravitational slingshot trajectories.",
        "<b>✦ Exoplanetary Discovery:</b> Precision Doppler spectroscopy measuring stellar reflex velocities and transit timing variations.",
        "<b>✦ Relativistic Gravitational Lensing:</b> Reconstruction of galactic dark matter distributions via photon geodesic deflection.",
        "<b>✦ Symplectic N-Body Integrations:</b> Multi-million-year secular stability modeling of chaotic planetary architectures."
    ]

    for app_item in apps:
        story.append(Paragraph(app_item, styles['AppBullet']))

    doc.build(story)
    print(f"SUCCESS: ReportLab PDF generated at: {os.path.abspath(output_path)}")
    print(f"File size: {os.path.getsize(output_path)} bytes")


if __name__ == '__main__':
    build_codex_pdf()
