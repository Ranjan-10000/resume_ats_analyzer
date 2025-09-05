from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
from io import BytesIO

class ReportGenerator:
    """
    Generates a professional, multi-page PDF report from the analysis results
    using the reportlab library.
    """

    @staticmethod
    def generate_pdf_report(scores, final_score, feedback_report):
        """
        Creates the complete PDF report in memory.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('Title', parent=styles['h1'], alignment=TA_CENTER, fontSize=24, spaceAfter=20)
        subtitle_style = ParagraphStyle('Subtitle', parent=styles['h2'], alignment=TA_CENTER, fontSize=16, spaceAfter=10)
        heading_style = ParagraphStyle('Heading', parent=styles['h2'], fontSize=14, spaceAfter=10, spaceBefore=10)
        body_style = styles['BodyText']
        
        good_style = ParagraphStyle('Good', parent=styles['Normal'], textColor=HexColor('#2E7D32'), leftIndent=15)
        improve_style = ParagraphStyle('Improve', parent=styles['Normal'], textColor=HexColor('#C62828'), leftIndent=15)

        story = []

        # --- Page 1: Cover Page & Summary ---
        story.append(Paragraph("ATS Resume Analysis Report", title_style))
        story.append(Paragraph(f"Final Weighted ATS Score: {final_score:.2f}%", subtitle_style))
        story.append(Spacer(1, 24))

        # Add score summary table
        story.append(Paragraph("Score Summary", heading_style))
        for category, score in scores.items():
            story.append(Paragraph(f"• <b>{category}:</b> {score:.2f}%", body_style))
        
        story.append(PageBreak())

        # --- Page 2: Detailed Feedback Report ---
        story.append(Paragraph("Detailed Feedback Report", title_style))
        
        for category, feedback in feedback_report.items():
            story.append(Paragraph(category, heading_style))
            
            if feedback['good']:
                story.append(Paragraph("<b>✅ What you did well:</b>", body_style))
                for point in feedback['good']:
                    story.append(Paragraph(f"• {point}", good_style))
                story.append(Spacer(1, 12))

            if feedback['improve']:
                story.append(Paragraph("<b>💡 What you can improve:</b>", body_style))
                for point in feedback['improve']:
                    story.append(Paragraph(f"• {point}", improve_style))
                story.append(Spacer(1, 24))
        
        doc.build(story)
        
        buffer.seek(0)
        return buffer
