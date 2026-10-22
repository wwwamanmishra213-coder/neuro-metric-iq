"""
PROJECT: ARCANE WILLOW CODEX
Design Configuration and Styling Tokens for ReportLab PDF Generation
"""

from reportlab.lib import colors
from reportlab.lib.units import mm, inch

# ==================== PAGE DIMENSIONS (A4 PORTRAIT) ====================
PAGE_WIDTH = 210 * mm
PAGE_HEIGHT = 297 * mm

# Safe Margin Boundary: 22mm top/bottom, 20mm sides
MARGIN_TOP = 22 * mm
MARGIN_BOTTOM = 20 * mm
MARGIN_LEFT = 20 * mm
MARGIN_RIGHT = 20 * mm

USABLE_WIDTH = PAGE_WIDTH - (MARGIN_LEFT + MARGIN_RIGHT)
USABLE_HEIGHT = PAGE_HEIGHT - (MARGIN_TOP + MARGIN_BOTTOM)

# ==================== COLOR PALETTE (EXACT CSS MATCH) ====================
COLOR_OBSIDIAN = colors.HexColor('#0B0A0C')
COLOR_CHARCOAL = colors.HexColor('#15131A')
COLOR_ANTIQUE_GOLD = colors.HexColor('#C6A15B')
COLOR_BRIGHT_GOLD = colors.HexColor('#E8CB83')
COLOR_BRONZE = colors.HexColor('#72512D')
COLOR_PARCHMENT = colors.HexColor('#E9E0CC')
COLOR_MUTED_SILVER = colors.HexColor('#9A9AA5')
COLOR_BODY_TEXT = colors.HexColor('#E8E0D2')
COLOR_CYAN_ACCENT = colors.HexColor('#38BDF8')
COLOR_RUBY_ACCENT = colors.HexColor('#F43F5E')
COLOR_EMERALD_ACCENT = colors.HexColor('#34D399')

# ==================== TYPOGRAPHY FALLBACK STACK ====================
# Standard ReportLab built-in Type-1 core fonts:
# 'Times-Roman', 'Times-Bold', 'Times-Italic', 'Helvetica', 'Helvetica-Bold', 'Courier'
FONT_DISPLAY = 'Times-Bold'
FONT_HEADING = 'Times-Bold'
FONT_BODY = 'Times-Roman'
FONT_BODY_ITALIC = 'Times-Italic'
FONT_TECH = 'Helvetica'
FONT_TECH_BOLD = 'Helvetica-Bold'
FONT_MATH = 'Times-Italic'
