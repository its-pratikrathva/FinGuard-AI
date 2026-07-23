from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate


class ReportService:

    def generate_pdf(self, scan):

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        story = []

        story.append(Paragraph("<b>FinGuard AI Report</b>", styles["Title"]))

        story.append(Paragraph(f"<b>Scan ID:</b> {scan.id}", styles["BodyText"]))

        story.append(Paragraph(f"<b>Language:</b> {scan.language}", styles["BodyText"]))

        story.append(Paragraph(f"<b>Risk Score:</b> {scan.risk_score}", styles["BodyText"]))

        story.append(Paragraph(f"<b>Status:</b> {scan.status}", styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph("<b>Original Message</b>", styles["Heading2"]))
        story.append(Paragraph(scan.message, styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph("<b>Detected Keywords</b>", styles["Heading2"]))
        story.append(Paragraph(", ".join(scan.keywords), styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph("<b>Detected URLs</b>", styles["Heading2"]))
        story.append(Paragraph("<br/>".join(scan.urls), styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph("<b>AI Analysis</b>", styles["Heading2"]))
        story.append(Paragraph(scan.reason.replace("\n", "<br/>"), styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph("<b>Advice</b>", styles["Heading2"]))
        story.append(Paragraph(scan.advice, styles["BodyText"]))

        doc.build(story)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf