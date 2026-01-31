import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.units import cm

class Generator:
    @staticmethod
    def generate_pdf(data):
        """Generates a professional A4 PDF with a two-column layout."""
        output_dir = "resume_output"
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        pdf_path = os.path.join(output_dir, "resume.pdf")

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1*cm,
            bottomMargin=1*cm
        )
        
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'NameStyle', parent=styles['Heading1'], fontSize=24, 
            textColor=colors.HexColor("#2C3E50"), spaceAfter=2
        )
        subtitle_style = ParagraphStyle(
            'SubStyle', parent=styles['Normal'], fontSize=12, 
            textColor=colors.HexColor("#7F8C8D"), spaceAfter=10
        )
        section_header = ParagraphStyle(
            'SectionHeader', parent=styles['Heading2'], fontSize=14, 
            textColor=colors.HexColor("#2980B9"), spaceBefore=10, spaceAfter=5
        )
        body_text = ParagraphStyle(
            'Body', parent=styles['Normal'], fontSize=10, 
            leading=12, alignment=0
        )
        sidebar_text = ParagraphStyle(
            'Sidebar', parent=styles['Normal'], fontSize=9, 
            textColor=colors.whitesmoke, leading=11
        )

        elements = []

        elements.append(Paragraph(data.get("name", "Applicant").upper(), title_style))
        elements.append(Paragraph(data.get("title", ""), subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#BDC3C7"), spaceAfter=15))

        
        sidebar_items = []
        sidebar_items.append(Paragraph("<b>CONTACT</b>", sidebar_text))
        sidebar_items.append(Spacer(1, 0.2*cm))
        sidebar_items.append(Paragraph(data.get("email", ""), sidebar_text))
        sidebar_items.append(Paragraph(data.get("phone", ""), sidebar_text))
        sidebar_items.append(Paragraph(data.get("location", ""), sidebar_text))
        
        if "custom_sections" in data:
            for section in data["custom_sections"]:
                sidebar_items.append(Spacer(1, 0.5*cm))
                sidebar_items.append(Paragraph(f"<b>{section['title'].upper()}</b>", sidebar_text))
                sidebar_items.append(Spacer(1, 0.2*cm))
                content_bullets = section['content'].replace('\n', '<br/>')
                sidebar_items.append(Paragraph(content_bullets, sidebar_text))

        main_items = []
        
        if data.get("summary"):
            main_items.append(Paragraph("<b>PROFESSIONAL SUMMARY</b>", section_header))
            main_items.append(Paragraph(data["summary"], body_text))

        if data.get("experience"):
            main_items.append(Paragraph("<b>WORK EXPERIENCE</b>", section_header))
            for exp in data["experience"]:
                header = f"<b>{exp['position']}</b> | {exp['company']}"
                dates = f"<i>{exp['start_date']} — {exp['end_date']}</i>"
                main_items.append(Paragraph(header, body_text))
                main_items.append(Paragraph(dates, body_text))
                main_items.append(Paragraph(exp.get("highlights", "").replace('\n', '<br/>'), body_text))
                main_items.append(Spacer(1, 0.3*cm))

        if data.get("education"):
            main_items.append(Paragraph("<b>EDUCATION</b>", section_header))
            for edu in data["education"]:
                edu_line = f"<b>{edu['degree']}</b>, {edu['institution']}"
                main_items.append(Paragraph(edu_line, body_text))
                main_items.append(Paragraph(f"<i>{edu['start_date']} — {edu['end_date']}</i>", body_text))
                main_items.append(Spacer(1, 0.2*cm))

        col_widths = [5.5*cm, 13.5*cm]
        layout_table = Table([[sidebar_items, main_items]], colWidths=col_widths)
        layout_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#2C3E50")), # Dark Sidebar
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ]))

        elements.append(layout_table)
        
        try:
            doc.build(elements)
            return pdf_path, None
        except Exception as e:
            return None, str(e)