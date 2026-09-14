import io
import datetime
import random
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie

CHART_COLOR_HEXES = ["#059669", "#2563EB", "#D97706", "#7C3AED", "#DB2777", "#475569"]
CHART_COLORS = [colors.HexColor(c) for c in CHART_COLOR_HEXES]

# Display order + labels for the full metals table
METAL_ORDER = ["gold", "silver", "copper", "cobalt", "steel", "aluminum"]
METAL_LABELS = {
    "gold": "Gold",
    "silver": "Silver",
    "copper": "Copper",
    "cobalt": "Cobalt",
    "steel": "Steel",
    "aluminum": "Aluminum",
}


def generate_pie_chart_with_legend(materials_dict: dict) -> Drawing:
    d = Drawing(460, 150)
    if not materials_dict:
        materials_dict = {"General Component": 100}

    labels = list(materials_dict.keys())
    data = [float(v) for v in materials_dict.values()]

    # Draw Pie Chart
    pie = Pie()
    pie.x = 10
    pie.y = 5
    pie.width = 140
    pie.height = 140
    pie.data = data
    pie.sideLabels = 0

    for i in range(len(data)):
        c = CHART_COLORS[i % len(CHART_COLORS)]
        pie.slices[i].fillColor = c
        pie.slices[i].strokeColor = colors.white
        pie.slices[i].strokeWidth = 1.5

    d.add(pie)

    # Draw Legend on the right side
    legend_x = 180
    legend_y = 120
    for i, (label, val) in enumerate(materials_dict.items()):
        c = CHART_COLORS[i % len(CHART_COLORS)]
        current_y = legend_y - (i * 20)

        # Color Indicator Square
        d.add(Rect(legend_x, current_y, 10, 10, fillColor=c, strokeColor=None))

        # Text Label & Percentage
        text_str = f"{label}: {val}%"
        d.add(
            String(
                legend_x + 18,
                current_y + 1,
                text_str,
                fontName="Helvetica-Bold",
                fontSize=9,
                fillColor=colors.HexColor("#334155"),
            )
        )

    return d


def build_pdf_report(analysis_data: dict, input_weight: float = 1.0) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    primary = colors.HexColor("#0f172a")
    accent_emerald = colors.HexColor("#059669")
    dark_gray = colors.HexColor("#334155")
    light_bg = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#e2e8f0")

    # Typography Styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        textColor=primary,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    )
    meta_style = ParagraphStyle(
        "Meta",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=dark_gray,
        fontName="Helvetica",
        alignment=TA_CENTER,
    )
    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        textColor=accent_emerald,
        fontName="Helvetica-Bold",
        spaceAfter=6,
    )
    item_name_style = ParagraphStyle(
        "ItemName",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        textColor=primary,
        fontName="Helvetica-Bold",
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=dark_gray,
        fontName="Helvetica",
    )
    bold_body = ParagraphStyle(
        "BoldBody", parent=body_style, fontName="Helvetica-Bold", textColor=primary
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#64748b"),
        fontName="Helvetica-Oblique",
    )

    story = []

    # ---------------------------------------------------------------
    # Header
    # ---------------------------------------------------------------
    now = datetime.datetime.utcnow()
    audit_ref = f"#EW-{random.randint(100000, 999999)}"

    story.append(Paragraph("E-WASTE RECOVERY &amp; HAZARD AUDIT REPORT", title_style))
    story.append(Spacer(1, 4))
    story.append(
        Paragraph(
            f"Generated: {now.strftime('%B %d, %Y')} | {now.strftime('%H:%M')} UTC "
            f"&nbsp;&nbsp;|&nbsp;&nbsp; Audit Ref: {audit_ref}",
            meta_style,
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        HRFlowable(
            width="100%",
            thickness=1.5,
            color=accent_emerald,
            spaceBefore=0,
            spaceAfter=14,
        )
    )

    # ---------------------------------------------------------------
    # Detected Item block
    # ---------------------------------------------------------------
    display_name = analysis_data.get("display_name", "Unknown Device").title()
    category = analysis_data.get("category", "General Electronics").title()
    confidence = analysis_data.get("confidence", "N/A")

    story.append(Paragraph(f"DETECTED ITEM: {display_name}", item_name_style))
    story.append(
        Paragraph(
            f"<b>Category:</b> {category} &nbsp;&nbsp;&nbsp; "
            f"<b>Confidence:</b> {confidence} &nbsp;&nbsp;&nbsp; "
            f"<b>Input Mass:</b> {float(input_weight):.2f} kg",
            body_style,
        )
    )
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------------
    # Yield Stat Boxes (Gold / Copper / Market Value)
    # ---------------------------------------------------------------
    if analysis_data.get("is_ewaste", True):
        gold_g = analysis_data.get("gold_g", 0.0)
        copper_g = analysis_data.get("copper_g", 0.0)
        est_val = analysis_data.get("est_value_usd", "0.00")

        yield_data = [
            [
                Paragraph("<b>EST. GOLD YIELD</b>", body_style),
                Paragraph("<b>EST. COPPER YIELD</b>", body_style),
                Paragraph("<b>SCRAP MARKET VALUE</b>", body_style),
            ],
            [
                Paragraph(f"<font size=14 color='#D97706'><b>{gold_g} g</b></font>", body_style),
                Paragraph(f"<font size=14 color='#C2410C'><b>{copper_g} g</b></font>", body_style),
                Paragraph(f"<font size=14 color='#059669'><b>${est_val}</b></font>", body_style),
            ],
        ]
        yield_table = Table(yield_data, colWidths=[177, 177, 177])
        yield_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), light_bg),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("BOX", (0, 0), (-1, -1), 1, border_color),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        story.append(yield_table)
        story.append(Spacer(1, 16))

    # ---------------------------------------------------------------
    # Material Composition Breakdown (pie + legend)
    # ---------------------------------------------------------------
    materials = analysis_data.get("materials", {})
    story.append(Paragraph("Material Composition Breakdown", section_heading))
    pie_drawing = generate_pie_chart_with_legend(materials)
    story.append(pie_drawing)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------------
    # Recoverable Precious & Base Metal Yields (full metals table)
    # ---------------------------------------------------------------
    metals_g = analysis_data.get("metals_g") or analysis_data.get("metals_recovered_g") or {}

    metal_rows = [
        [
            Paragraph("<b>Metal Category</b>", body_style),
            Paragraph("<b>Estimated Yield (Grams)</b>", body_style),
            Paragraph("<b>Market Status</b>", body_style),
        ]
    ]
    for key in METAL_ORDER:
        val = metals_g.get(key, 0.0)
        if val and val > 0:
            metal_rows.append(
                [
                    Paragraph(METAL_LABELS[key], body_style),
                    Paragraph(f"{val} g", body_style),
                    Paragraph(
                        "<font color='#059669'><b>Recoverable</b></font>", body_style
                    ),
                ]
            )

    if len(metal_rows) > 1:
        metals_table = Table(metal_rows, colWidths=[177, 177, 177])
        metals_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
                    ("BACKGROUND", (0, 1), (-1, -1), light_bg),
                    ("BOX", (0, 0), (-1, -1), 1, border_color),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(
            KeepTogether(
                [
                    Paragraph("Recoverable Precious &amp; Base Metal Yields", section_heading),
                    metals_table,
                ]
            )
        )
        story.append(Spacer(1, 16))

    # ---------------------------------------------------------------
    # Hazard Rating & Disposal Protocol
    # ---------------------------------------------------------------
    hazard = analysis_data.get("hazard", "Non-Hazardous / Standard Handling")
    protocol = analysis_data.get(
        "protocol", "Dispose of at local certified recycling centers."
    )

    story.append(
        KeepTogether(
            [
                Paragraph("Hazard Rating &amp; Disposal Protocol", section_heading),
                Paragraph(
                    f"<b>Hazard Level:</b> <font color='#DC2626'><b>{hazard}</b></font>",
                    body_style,
                ),
                Spacer(1, 4),
                Paragraph(
                    f"<b>Actionable Disposal Protocol:</b> {protocol}", body_style
                ),
            ]
        )
    )
    story.append(Spacer(1, 18))

    # ---------------------------------------------------------------
    # Operational Valuation Methodology (disclaimer)
    # ---------------------------------------------------------------
    story.append(
        HRFlowable(
            width="100%",
            thickness=0.75,
            color=border_color,
            spaceBefore=0,
            spaceAfter=8,
        )
    )
    story.append(Paragraph("Operational Valuation Methodology", section_heading))
    story.append(
        Paragraph(
            "Disclaimer: This report was automatically rendered via raw assessment "
            "metrics. Scrap Market Value represents a theoretical maximum recovery "
            "yield based on spot metal indices and 100% extraction efficiency. "
            "Real-world yields depend on local facility capabilities and smelting "
            "losses. Mass entries scale valuation figures linearly.",
            disclaimer_style,
        )
    )

    doc.build(story)
    buffer.seek(0)
    return buffer