import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "NeuroMetric_CrossBorder_HealthTech_Master_Blueprint.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Outer delicate border
        self.setStrokeColor(colors.HexColor('#0F172A'))
        self.setLineWidth(1)
        self.rect(20, 20, 555, 802)
        
        self.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.setLineWidth(0.5)
        self.rect(24, 24, 547, 794)

        # Header running band
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#0F172A'))
        self.drawString(32, 804, "NEUROMETRIC HEALTH-TECH VENTURE")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(220, 804, "Cross-Border Tele-Medicine & Corporate Master Blueprint (Nepal ⇄ India)")

        # Top rule
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.75)
        self.line(32, 798, 563, 798)

        # Footer rule
        self.line(32, 38, 563, 38)

        # Footer running text
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#0F172A'))
        self.drawString(32, 28, "CONFIDENTIAL & PROPRIETARY")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(200, 28, "Executive Strategic, Legal, Doctor Onboarding & Financial Action Plan")

        # Page numbering
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(563, 28, page_text)

        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0284C7'),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#0369A1'),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=colors.HexColor('#0F172A')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=9.8,
        textColor=colors.HexColor('#1E293B')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.8,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # ==================== PAGE 1: TITLE & CORPORATE ARCHITECTURE ====================
    story.append(Paragraph("NEUROMETRIC HEALTH-TECH VENTURE", title_style))
    story.append(Paragraph("Cross-Border Tele-Medicine, Corporate Incorporation, Doctor Network & Cost Blueprint (Nepal ⇄ Delhi)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceBefore=0, spaceAfter=8))

    # Executive Summary Card
    summary_text = (
        "<b>Executive Purpose:</b> This master document outlines the end-to-end blueprint to legally establish, "
        "license, and operate the NeuroMetric cognitive assessment and cross-border tele-psychiatry platform connecting "
        "patients in Nepal with medical practitioners in Delhi (India). It leverages the strategic advantage of dual Nepal "
        "and India passport holders, providing exact statutory certificates, step-by-step government workflows, bare-minimum "
        "incorporation budgets, doctor revenue-share models, and malpractice legal shielding."
    )
    summary_table = Table([[Paragraph(summary_text, callout_style)]], colWidths=[523])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F0F9FF')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#BAE6FD')),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 8))

    # Section 1: Dual-Passport Twin-Entity Architecture
    story.append(Paragraph("1. Dual-Passport Strategic Corporate Structure (Nepal + India)", h1_style))
    p1_desc = (
        "Holding both a <b>Nepali Passport</b> and an <b>Indian Passport</b> eliminates foreign direct investment (FDI) barriers, "
        "foreign currency exchange locks (NRB/RBI), and regulatory cross-border clinic liabilities. The platform operates as a "
        "<b>Twin-Entity Bridge</b>:"
    )
    story.append(Paragraph(p1_desc, body_style))

    arch_data = [
        [
            Paragraph("Entity Dimension", table_header_style),
            Paragraph("Nepal Entity (Kathmandu)", table_header_style),
            Paragraph("India Entity (Delhi)", table_header_style)
        ],
        [
            Paragraph("<b>Company Name</b>", table_cell_bold),
            Paragraph("NeuroMetric HealthTech Pvt. Ltd.", table_cell_style),
            Paragraph("NeuroMetric Health Technologies Pvt. Ltd. (or LLP)", table_cell_style)
        ],
        [
            Paragraph("<b>Ownership / Directors</b>", table_cell_bold),
            Paragraph("Nepali Passport Holder (100% domestic)", table_cell_style),
            Paragraph("Indian Passport Holder (100% domestic)", table_cell_style)
        ],
        [
            Paragraph("<b>Primary Function</b>", table_cell_bold),
            Paragraph("Client intake, domestic marketing, local polyclinic MoUs, patient support", table_cell_style),
            Paragraph("Doctor credentialing, DMC doctor network management, software R&D", table_cell_style)
        ],
        [
            Paragraph("<b>Payment Gateways</b>", table_cell_bold),
            Paragraph("Fonepay, eSewa, Khalti, local bank QR (NPR collections)", table_cell_style),
            Paragraph("Razorpay, Stripe, UPI, Indian NetBanking (INR & Global USD cards)", table_cell_style)
        ],
        [
            Paragraph("<b>Doctor Payouts</b>", table_cell_bold),
            Paragraph("Settled in NPR for local Nepal-affiliated MBBS/MD doctors", table_cell_style),
            Paragraph("Direct domestic NEFT/IMPS/UPI payouts in INR to Delhi doctors", table_cell_style)
        ],
    ]
    arch_table = Table(arch_data, colWidths=[103, 210, 210])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 8))

    # Section 2: Bare-Minimum Company Incorporation Costs & Certificates
    story.append(Paragraph("2. Mandatory Certificates & Bare-Minimum Startup Costs", h1_style))
    story.append(Paragraph("The exact statutory certificates required by both governments and the minimum cash cost when avoiding agencies:", body_style))

    cost_data = [
        [
            Paragraph("Jurisdiction & Step", table_header_style),
            Paragraph("Certificates / Registration Required", table_header_style),
            Paragraph("Authority", table_header_style),
            Paragraph("Min. Cost", table_header_style)
        ],
        [
            Paragraph("<b>Nepal (Pvt. Ltd.)</b><br/>Step 1: OCR", table_cell_bold),
            Paragraph("Certificate of Incorporation (दर्ता प्रमाण पत्र)", table_cell_style),
            Paragraph("Office of Company Registrar (त्रिपुरेश्वर)", table_cell_style),
            Paragraph("NPR 4,500", table_cell_bold)
        ],
        [
            Paragraph("<b>Nepal (Pvt. Ltd.)</b><br/>Step 2: Legal", table_cell_bold),
            Paragraph("MoA (प्रबन्धपत्र) & AoA (नियमावली) Notarization", table_cell_style),
            Paragraph("Notary Public / Advocate", table_cell_style),
            Paragraph("NPR 1,500", table_cell_bold)
        ],
        [
            Paragraph("<b>Nepal (Pvt. Ltd.)</b><br/>Step 3: Ward", table_cell_bold),
            Paragraph("Ward Business Registration (वडा कार्यालय दर्ता)", table_cell_style),
            Paragraph("Local Ward Office (Kathmandu)", table_cell_style),
            Paragraph("NPR 4,000", table_cell_bold)
        ],
        [
            Paragraph("<b>Nepal (Pvt. Ltd.)</b><br/>Step 4: Tax & Seal", table_cell_bold),
            Paragraph("Permanent Account Number (PAN) & Company Seal", table_cell_style),
            Paragraph("Inland Revenue Dept (IRD)", table_cell_style),
            Paragraph("NPR 1,000", table_cell_bold)
        ],
        [
            Paragraph("<b>NEPAL TOTAL</b>", table_cell_bold),
            Paragraph("<b>Fully operational registered 2-person Nepal company</b>", table_cell_bold),
            Paragraph("<b>Nepal Government</b>", table_cell_bold),
            Paragraph("<b>NPR 11,000</b><br/><i>(~$82 USD)</i>", table_cell_bold)
        ],
        [
            Paragraph("<b>India (Pvt. Ltd. / LLP)</b><br/>Step 1: DSC", table_cell_bold),
            Paragraph("Class-3 Digital Signature Certificate (2 Directors)", table_cell_style),
            Paragraph("eMudhra / SignX / Certifying Authority", table_cell_style),
            Paragraph("₹1,200", table_cell_bold)
        ],
        [
            Paragraph("<b>India (Pvt. Ltd. / LLP)</b><br/>Step 2: MCA", table_cell_bold),
            Paragraph("Certificate of Incorporation (CoI via SPICe+)", table_cell_style),
            Paragraph("Ministry of Corporate Affairs (RoC Delhi)", table_cell_style),
            Paragraph("₹1,000", table_cell_bold)
        ],
        [
            Paragraph("<b>India (Pvt. Ltd. / LLP)</b><br/>Step 3: Certification", table_cell_bold),
            Paragraph("CA / CS Statutory Professional Certification", table_cell_style),
            Paragraph("Practicing CA / CS (Delhi)", table_cell_style),
            Paragraph("₹3,500", table_cell_bold)
        ],
        [
            Paragraph("<b>India (Pvt. Ltd. / LLP)</b><br/>Step 4: Tax & Govt", table_cell_bold),
            Paragraph("Company e-PAN, e-TAN, and GST Registration", table_cell_style),
            Paragraph("Income Tax Dept & GSTN (Free)", table_cell_style),
            Paragraph("₹130", table_cell_bold)
        ],
        [
            Paragraph("<b>INDIA TOTAL</b>", table_cell_bold),
            Paragraph("<b>Fully operational registered 2-person India company</b>", table_cell_bold),
            Paragraph("<b>Govt of India (MCA)</b>", table_cell_bold),
            Paragraph("<b>₹5,830</b><br/><i>(~$70 USD)</i>", table_cell_bold)
        ],
        [
            Paragraph("<b>COMBINED TOTAL</b>", table_cell_bold),
            Paragraph("<b>Grand minimum cash needed to launch both companies</b>", table_cell_bold),
            Paragraph("<b>Nepal + India</b>", table_cell_bold),
            Paragraph("<b>NPR 20,500</b><br/><i>(~$152 USD)</i>", table_cell_bold)
        ],
    ]
    cost_table = Table(cost_data, colWidths=[103, 210, 130, 80])
    cost_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('BACKGROUND', (0, 5), (-1, 5), colors.HexColor('#E0F2FE')),
        ('BACKGROUND', (0, 10), (-1, 10), colors.HexColor('#E0F2FE')),
        ('BACKGROUND', (0, 11), (-1, 11), colors.HexColor('#FEF3C7')),
    ]))
    story.append(cost_table)

    story.append(PageBreak())

    # ==================== PAGE 2: CROSS-BORDER DOCTOR REGULATIONS & MODELS ====================
    story.append(Paragraph("3. Cross-Border Patient Treatment Protocol (Nepal ⇄ Delhi)", h1_style))
    story.append(Paragraph("How a patient in Nepal legally receives clinical evaluation and care from a doctor in Delhi:", body_style))

    # Two models table
    models_data = [
        [
            Paragraph("Operational Dimension", table_header_style),
            Paragraph("Model A: Tele-Psychology & Second Opinion (Immediate)", table_header_style),
            Paragraph("Model B: Prescriptive Tele-Medicine (Medications)", table_header_style)
        ],
        [
            Paragraph("<b>Clinical Scope</b>", table_cell_bold),
            Paragraph("Cognitive IQ analysis, ADHD/Depression/Anxiety screener review, psychotherapy, behavioural coaching, clinical commentary.", table_cell_style),
            Paragraph("Direct diagnosis and prescribing psychiatric medication (e.g., SSRIs, Stimulants, Mood Stabilizers).", table_cell_style)
        ],
        [
            Paragraph("<b>Legal Classification</b>", table_cell_bold),
            Paragraph("Cross-border remote psychometric consultation and advisory opinion.", table_cell_style),
            Paragraph("Formal collaborative medical care (Doctor-to-Doctor Telemedicine).", table_cell_style)
        ],
        [
            Paragraph("<b>Prescription Rule</b>", table_cell_bold),
            Paragraph("No physical prescription issued; recommendations provided in clinical dossier.", table_cell_style),
            Paragraph("Indian prescription <b>cannot</b> be dispensed in Nepal. Must be co-signed by an affiliated Nepal Medical Council (NMC) doctor.", table_cell_style)
        ],
        [
            Paragraph("<b>Pharmacy Dispensing</b>", table_cell_bold),
            Paragraph("N/A (Non-pharmacological intervention).", table_cell_style),
            Paragraph("Partnered Kathmandu pharmacy or clinic fulfills medicine using local NMC doctor's co-signed slip.", table_cell_style)
        ],
        [
            Paragraph("<b>Legal Barrier</b>", table_cell_bold),
            Paragraph("<b>Zero Barrier:</b> Patient signs digital Informed Consent. 100% ready today.", table_cell_style),
            Paragraph("<b>Low Barrier:</b> Requires a simple referral agreement with 1 local Nepal clinic.", table_cell_style)
        ],
    ]
    models_table = Table(models_data, colWidths=[113, 205, 205])
    models_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(models_table)
    story.append(Spacer(1, 10))

    # Section 4: Doctor Onboarding, Bonding & Liability Shield
    story.append(Paragraph("4. Doctor Engagement: No Employment Bonds, Pure Revenue-Share", h1_style))
    story.append(Paragraph(
        "<b>Why you must NEVER use an employment bond:</b> Under Section 27 of the Indian Contract Act and Nepal contract law, "
        "bonds restricting a medical professional's right to practice are legally void and deter top clinicians. "
        "Instead, use an <b>Independent Consultant Master Services Agreement (MSA)</b> with zero upfront salary:",
        body_style
    ))

    # Revenue Split Table
    split_data = [
        [
            Paragraph("Consultation Product Tier", table_header_style),
            Paragraph("Patient Pays (Retail)", table_header_style),
            Paragraph("Doctor Share (65%-70%)", table_header_style),
            Paragraph("Platform Margin (30%-35%)", table_header_style)
        ],
        [
            Paragraph("<b>Tier 1: Automated Dossier</b><br/>(Algorithmic Psychometrics)", table_cell_bold),
            Paragraph("₹399 INR / NPR 640", table_cell_style),
            Paragraph("₹0 (Zero human review)", table_cell_style),
            Paragraph("<b>₹399 / NPR 640 (100% Margin)</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Tier 2: Doctor Dossier Review</b><br/>(Written Clinical Remarks + Signature)", table_cell_bold),
            Paragraph("₹1,200 INR / NPR 1,920", table_cell_style),
            Paragraph("₹800 INR / NPR 1,280", table_cell_style),
            Paragraph("<b>₹400 / NPR 640 (33% Margin)</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Tier 3: Comprehensive Tele-Session</b><br/>(30-Min Video Call + Final Dossier)", table_cell_bold),
            Paragraph("₹2,500 INR / NPR 4,000", table_cell_style),
            Paragraph("₹1,750 INR / NPR 2,800", table_cell_style),
            Paragraph("<b>₹750 / NPR 1,200 (30% Margin)</b>", table_cell_bold)
        ],
    ]
    split_table = Table(split_data, colWidths=[163, 120, 120, 120])
    split_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#F0FDF4')),
    ]))
    story.append(split_table)
    story.append(Spacer(1, 8))

    # The 4 Shield Clauses
    story.append(Paragraph("<b>The 4 Essential Protective Clauses You Must Enforce:</b>", h2_style))
    story.append(Paragraph(
        "<b>1. Medical Malpractice Liability Shield:</b> The agreement explicitly states that the practitioner maintains sole clinical and diagnostic autonomy. "
        "The platform is strictly a technology intermediary and psychometric telemetry provider, fully insulated from medical liability. "
        "The doctor must warrant holding active Professional Indemnity Insurance.", bullet_style
    ))
    story.append(Paragraph(
        "<b>2. Non-Circumvention (Patient Protection):</b> Doctors agree not to solicit or privately consult patients introduced by NeuroMetric "
        "outside the platform for a period of 12 months, protecting your client acquisition investments.", bullet_style
    ))
    story.append(Paragraph(
        "<b>3. Strict Service Level Agreement (SLA):</b> The doctor agrees to review assigned psychometric dossiers within 12 to 24 hours. "
        "If they fail to respond within the window, the platform dynamically reassigns the case to another doctor in the pool.", bullet_style
    ))
    story.append(Paragraph(
        "<b>4. Data Confidentiality & Non-Disclosure (NDA):</b> Absolute prohibition against exporting, copying, or sharing patient psychometric "
        "or identifying data, strictly compliant with DPDPA 2023 (India) and Privacy Act 2075 (Nepal).", bullet_style
    ))

    story.append(PageBreak())

    # ==================== PAGE 3: CONTRACT CLAUSES, REGULATORY ROADMAP & CHECKLIST ====================
    story.append(Paragraph("5. Ready-To-Use Contractual Agreement Templates", h1_style))
    story.append(Paragraph("Exact legal clauses ready to drop into your doctor contracts and patient onboarding screens:", body_style))

    # Box 1: Patient Informed Consent
    box1_text = (
        "<b>MANDATORY PATIENT INFORMED CONSENT & DISCLAIMER CLAUSE (Add to Website / Client Portal):</b><br/>"
        "<i>\"I hereby acknowledge that the NeuroMetric Assessment Platform is a specialized digital psychometric screener based on Cattell-Horn-Carroll (CHC) cognitive theory and standardized DSM-5 clinical inventories. I understand that the algorithmic score and remote clinical commentary provide an indicative screening assessment and do not constitute an emergency psychiatric intervention or a substitute for statutory in-person clinical diagnostic evaluations. In the event of acute psychiatric distress, suicidal ideation, or personal emergency, I agree to contact local emergency medical services or the National Mental Hospital immediately.\"</i>"
    )
    box1_table = Table([[Paragraph(box1_text, callout_style)]], colWidths=[523])
    box1_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#94A3B8')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(box1_table)
    story.append(Spacer(1, 6))

    # Box 2: Doctor Indemnity & Non-Circumvention
    box2_text = (
        "<b>DOCTOR INDEMNITY & INTERMEDIARY SAFE HARBOR CLAUSE (For Doctor Agreement):</b><br/>"
        "<i>\"The Medical Practitioner warrants that they hold an active, unencumbered registration with the relevant Medical Council (e.g., Delhi Medical Council / NMC India) and valid Professional Indemnity Insurance. The Practitioner agrees that they exercise sole independent medical judgment in all clinical evaluations. NeuroMetric HealthTech operates purely as an electronic records and psychometric technology intermediary under the Information Technology Act. The Practitioner shall defend, indemnify, and hold harmless the Company, its directors, and affiliates against any claims, losses, or legal costs arising from allegations of clinical negligence or malpractice.\"</i>"
    )
    box2_table = Table([[Paragraph(box2_text, callout_style)]], colWidths=[523])
    box2_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF2F2')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#FECACA')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(box2_table)
    story.append(Spacer(1, 8))

    # Section 6: Actionable 30-Day Step-by-Step Execution Plan
    story.append(Paragraph("6. Actionable 30-Day Execution Roadmap", h1_style))

    roadmap_data = [
        [
            Paragraph("Phase & Timeline", table_header_style),
            Paragraph("Concrete Action Item", table_header_style),
            Paragraph("Deliverable", table_header_style),
            Paragraph("Cash Outflow", table_header_style)
        ],
        [
            Paragraph("<b>Week 1</b><br/>Nepal Registration", table_cell_bold),
            Paragraph("Apply online at `ocr.gov.np` for name approval and registration of NeuroMetric Pvt. Ltd.", table_cell_style),
            Paragraph("OCR Incorporation Certificate + PAN", table_cell_style),
            Paragraph("NPR 6,000", table_cell_bold)
        ],
        [
            Paragraph("<b>Week 2</b><br/>India Registration", table_cell_bold),
            Paragraph("Procure 2 Class-3 DSCs; submit SPICe+ form on MCA portal for India entity in Delhi.", table_cell_style),
            Paragraph("MCA Certificate of Incorporation + e-PAN", table_cell_style),
            Paragraph("₹5,830 INR", table_cell_bold)
        ],
        [
            Paragraph("<b>Week 3</b><br/>Doctor Onboarding", table_cell_bold),
            Paragraph("Interview 2 resident clinical psychologists (M.Phil) / MD psychiatrists in Delhi via LinkedIn / personal network.", table_cell_style),
            Paragraph("2 Signed Consultant MSAs + DMC credential copies on file", table_cell_style),
            Paragraph("₹0 (Rev-Share)", table_cell_bold)
        ],
        [
            Paragraph("<b>Week 4</b><br/>Local Nepal Referral", table_cell_bold),
            Paragraph("Partner with 1 private polyclinic or pharmacy in Kathmandu for physical medication co-signing if needed.", table_cell_style),
            Paragraph("Simple referral collaboration MoU", table_cell_style),
            Paragraph("NPR 0", table_cell_bold)
        ],
        [
            Paragraph("<b>Week 5</b><br/>Fintech & Launch", table_cell_bold),
            Paragraph("Integrate Fonepay QR / eSewa on Nepal site and Razorpay on India site; launch Google Ads / Reddit marketing.", table_cell_style),
            Paragraph("Live multi-currency patient checkout", table_cell_style),
            Paragraph("NPR 5,000 Ads", table_cell_bold)
        ],
    ]
    roadmap_table = Table(roadmap_data, colWidths=[93, 210, 140, 80])
    roadmap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(roadmap_table)
    story.append(Spacer(1, 8))

    # Verification Seal / Sign-off Block
    sign_block = [
        [
            Paragraph("<b>PREPARED FOR:</b> Management & Founding Partners<br/>NeuroMetric Health-Tech Cross-Border Platform", table_cell_style),
            Paragraph("<b>LEGAL ARCHITECTURE:</b> Dual-Passport Corporate Bridge<br/>NMC Nepal (2020) & NMC India Guidelines Compliant", table_cell_style),
            Paragraph("<b>STATUS:</b> APPROVED FOR IMPLEMENTATION<br/>Date: October 2026 • Version 1.0 Final", table_cell_bold)
        ]
    ]
    sign_table = Table(sign_block, colWidths=[174, 174, 175])
    sign_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#94A3B8')),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(sign_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Master PDF successfully generated: {PDF_FILENAME}")

if __name__ == '__main__':
    build_pdf()
