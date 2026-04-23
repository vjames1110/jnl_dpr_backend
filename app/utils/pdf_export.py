from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_tmt_pdf(data):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Heading3'],
        alignment=TA_CENTER
    )

    meta_style = ParagraphStyle(
        'Meta',
        parent=styles['Normal'],
        alignment=TA_LEFT,
        fontSize=9
    )

    elements = []

    # Header
    elements.append(Paragraph("Jhajharia Nirman Limited", title_style))
    elements.append(Paragraph("TMT Purchase Tracking Report", subtitle_style))
    elements.append(Spacer(1, 6))

    elements.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            meta_style
        )
    )

    elements.append(Spacer(1, 12))

    # Table Header
    table_data = [[
        "Sr",
        "Site Code",
        "Site Name",
        "PO Qty",
        "Supplied",
        "Balance",
        "Supply %",
        "Status",
        "PM Comment",
        "Director Remarks"
    ]]

    # Rows
    for d in data:
        table_data.append([
            d.get("serial"),
            d.get("site_code"),
            d.get("site_name"),
            d.get("po_qty"),
            d.get("supplied"),
            d.get("balance"),
            f"{d.get('supply_percent', 0)}%",
            d.get("pm_remarks"),
            d.get("pm_comment"),
            d.get("director_remarks")
        ])

    table = Table(table_data, repeatRows=1)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1661BE")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("FONTSIZE", (0, 1), (-1, -1), 8),

        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.whitesmoke, colors.transparent])

    ]))

    elements.append(table)

    doc.build(elements)

    buffer.seek(0)

    return buffer