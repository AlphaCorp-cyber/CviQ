import os
import json
import logging
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from app import app
import cv_templates

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CVTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2C3E50')
        ))
        
        # Section heading style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=12,
            spaceAfter=6,
            textColor=colors.HexColor('#34495E'),
            borderWidth=1,
            borderColor=colors.HexColor('#3498DB'),
            borderPadding=3
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=12
        ))
    
    def generate_cv(self, user, cv_data, template):
        """Generate CV PDF using specified template"""
        try:
            # Create filename
            safe_name = "".join(c for c in cv_data['full_name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"CV_{safe_name}_{timestamp}.pdf"
            filepath = os.path.join(app.config['CV_FOLDER'], filename)
            
            # Get template generator
            template_module = getattr(cv_templates, template.template_file.replace('.py', ''))
            generator_class = getattr(template_module, 'TemplateGenerator')
            
            # Generate PDF
            generator = generator_class()
            success = generator.generate(cv_data, filepath)
            
            if success:
                logging.info(f"CV generated successfully: {filepath}")
                return filepath
            else:
                logging.error("Failed to generate CV")
                return None
                
        except Exception as e:
            logging.error(f"Error generating CV: {str(e)}")
            return None
    
    def create_basic_cv(self, cv_data, filepath):
        """Create a basic CV using ReportLab directly"""
        try:
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            
            # Title
            title = Paragraph(cv_data['full_name'], self.styles['CVTitle'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Contact information
            contact_info = f"""
            📧 {cv_data['email']} | 📱 {cv_data['phone']}<br/>
            🏠 {cv_data['address']}
            """
            contact = Paragraph(contact_info, self.styles['ContactInfo'])
            story.append(contact)
            story.append(Spacer(1, 20))
            
            # Professional Summary
            if cv_data['summary']:
                story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeading']))
                story.append(Paragraph(cv_data['summary'], self.styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Work Experience
            if cv_data['experience']:
                story.append(Paragraph("WORK EXPERIENCE", self.styles['SectionHeading']))
                for exp in cv_data['experience']:
                    story.append(Paragraph(f"• {exp}", self.styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Education
            if cv_data['education']:
                story.append(Paragraph("EDUCATION", self.styles['SectionHeading']))
                for edu in cv_data['education']:
                    story.append(Paragraph(f"• {edu}", self.styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Skills
            if cv_data['skills']:
                story.append(Paragraph("SKILLS", self.styles['SectionHeading']))
                skills_text = " • ".join(cv_data['skills'])
                story.append(Paragraph(skills_text, self.styles['Normal']))
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            logging.error(f"Error creating basic CV: {str(e)}")
            return False
