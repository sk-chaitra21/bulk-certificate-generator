from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


OUTPUT_DIR = Path("generated_certificates")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_certificate(
    certificate_id: str,
    recipient_name: str,
    event_name: str,
    issue_date: str,
) -> str:
    file_path = OUTPUT_DIR / f"{certificate_id}.pdf"

    pdf = canvas.Canvas(str(file_path), pagesize=A4)
    width, height = A4

    # Certificate title
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        width / 2,
        height - 180,
        "CERTIFICATE OF PARTICIPATION",
    )

    # Main text
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        height - 260,
        "This certificate is proudly presented to",
    )

    # Recipient name
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(
        width / 2,
        height - 320,
        recipient_name,
    )

    # Event
    pdf.setFont("Helvetica", 15)
    pdf.drawCentredString(
        width / 2,
        height - 380,
        f"for participating in {event_name}",
    )

    # Date
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(
        width / 2,
        height - 450,
        f"Issue Date: {issue_date}",
    )

    pdf.save()

    return str(file_path)