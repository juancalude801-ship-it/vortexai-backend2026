from io import BytesIO
from reportlab.pdfgen import canvas

def build_contract_pdf(deal_summary: dict) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf)
    c.setFont("Helvetica", 12)

    y = 800
    c.drawString(50, y, "VortexAI Wholesale Contract Summary (MVP)")
    y -= 30

    for k, v in deal_summary.items():
        c.drawString(50, y, f"{k}: {v}")
        y -= 18
        if y < 60:
            c.showPage()
            y = 800

    c.showPage()
    c.save()
    return buf.getvalue()
