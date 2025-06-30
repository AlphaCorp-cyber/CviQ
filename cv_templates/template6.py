
"""
Sales Professional CV Template
Designed for sales and business development professionals
"""

import json
import logging
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

class TemplateGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup sales-focused styles"""
        # Professional sales header
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=28,
            spaceAfter=8,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1B5E20'),
            fontName='Helvetica-Bold'
        ))
        
        # Business contact style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_CENTER,
            spaceAfter=18,
            textColor=colors.HexColor('#424242')
        ))
        
        # Achievement-focused sections
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=18,
            spaceAfter=10,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#388E3C'),
            borderPadding=8,
            alignment=TA_CENTER
        ))
        
        # Results-focused job title
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=13,
            spaceBefore=10,
            spaceAfter=3,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1B5E20')
        ))
        
        # Company style
        self.styles.add(ParagraphStyle(
            name='Organization',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=2,
            fontName='Helvetica-Oblique',
            textColor=colors.HexColor('#2E7D32')
        ))
        
        # Achievement-focused description
        self.styles.add(ParagraphStyle(
            name='Achievement',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#1B5E20'),
            leftIndent=15,
            fontName='Helvetica-Bold'
        ))
        
        # Regular description
        self.styles.add(ParagraphStyle(
            name='Description',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#212121')
        ))
    
    def generate(self, cv_data, filepath):
        """Generate sales-focused CV"""
        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=22*mm,
                leftMargin=22*mm,
                topMargin=20*mm,
                bottomMargin=20*mm
            )
            
            story = []
            
            # Header
            story.extend(self._create_header(cv_data))
            
            # Value proposition
            if cv_data.get('summary'):
                story.extend(self._create_summary_section(cv_data['summary']))
            
            # Sales experience
            if cv_data.get('experience'):
                story.extend(self._create_experience_section(cv_data['experience']))
            
            # Education
            if cv_data.get('education'):
                story.extend(self._create_education_section(cv_data['education']))
            
            # Core competencies
            if cv_data.get('skills'):
                story.extend(self._create_skills_section(cv_data['skills']))
            
            doc.build(story)
            logging.info(f"Template6 CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating Template6 CV: {str(e)}")
            return False
    
    def _create_header(self, cv_data):
        """Create professional sales header"""
        elements = []
        
        # Name
        name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
        elements.append(name)
        
        # Professional tagline
        tagline = Paragraph("SALES PROFESSIONAL", self.styles['ContactInfo'])
        elements.append(tagline)
        
        # Contact info
        contact_parts = []
        if cv_data.get('phone'):
            contact_parts.append(f"📱 {cv_data['phone']}")
        if cv_data.get('email'):
            contact_parts.append(f"📧 {cv_data['email']}")
        if cv_data.get('address'):
            contact_parts.append(f"📍 {cv_data['address']}")
        
        if contact_parts:
            contact_text = " | ".join(contact_parts)
            contact = Paragraph(contact_text, self.styles['ContactInfo'])
            elements.append(contact)
        
        return elements
    
    def _create_summary_section(self, summary):
        """Create value proposition section"""
        elements = []
        heading = Paragraph("VALUE PROPOSITION", self.styles['SectionHeading'])
        elements.append(heading)
        summary_para = Paragraph(summary, self.styles['Description'])
        elements.append(summary_para)
        return elements
    
    def _create_experience_section(self, experience_list):
        """Create achievement-focused experience"""
        elements = []
        heading = Paragraph("SALES ACHIEVEMENTS", self.styles['SectionHeading'])
        elements.append(heading)
        
        for exp in experience_list:
            exp_elements = self._parse_experience_entry(exp)
            elements.extend(exp_elements)
        
        return elements
    
    def _parse_experience_entry(self, experience_text):
        """Parse with achievement focus"""
        elements = []
        lines = [line.strip() for line in experience_text.split('\n') if line.strip()]
        
        if not lines:
            return elements
        
        first_line = lines[0]
        if ' at ' in first_line:
            parts = first_line.split(' at ', 1)
            job_title = parts[0].strip()
            company = parts[1].strip()
        else:
            job_title = first_line
            company = ""
        
        elements.append(Paragraph(job_title, self.styles['JobTitle']))
        if company:
            elements.append(Paragraph(company, self.styles['Organization']))
        
        # Highlight achievements with numbers/percentages
        for line in lines[1:]:
            # Check if line contains achievements (numbers, percentages, etc.)
            if any(indicator in line for indicator in ['%', '$', 'million', 'thousand', 'increased', 'achieved', 'exceeded', 'generated']):
                achievement_text = f"★ {line}"
                elements.append(Paragraph(achievement_text, self.styles['Achievement']))
            elif any(keyword in line.lower() for keyword in ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                            'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
                                                            '20', '19', 'present', 'current', '-']):
                # Date formatting
                date_text = f"📅 {line}"
                elements.append(Paragraph(date_text, self.styles['Description']))
            else:
                elements.append(Paragraph(line, self.styles['Description']))
        
        elements.append(Spacer(1, 8))
        return elements
    
    def _create_education_section(self, education_list):
        """Create education section"""
        elements = []
        heading = Paragraph("EDUCATION & CERTIFICATIONS", self.styles['SectionHeading'])
        elements.append(heading)
        
        for edu in education_list:
            edu_para = Paragraph(f"🎓 {edu}", self.styles['Description'])
            elements.append(edu_para)
        
        return elements
    
    def _create_skills_section(self, skills_list):
        """Create core competencies section"""
        elements = []
        heading = Paragraph("CORE COMPETENCIES", self.styles['SectionHeading'])
        elements.append(heading)
        
        if isinstance(skills_list, list):
            # Create table for better presentation
            skills_rows = []
            for i in range(0, len(skills_list), 2):
                row = []
                row.append(f"✓ {skills_list[i]}" if i < len(skills_list) else "")
                row.append(f"✓ {skills_list[i+1]}" if i+1 < len(skills_list) else "")
                skills_rows.append(row)
            
            if skills_rows:
                skills_table = Table(skills_rows, colWidths=[8.5*cm, 8.5*cm])
                skills_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1B5E20')),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 3),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ]))
                elements.append(skills_table)
        else:
            skills_para = Paragraph(f"✓ {str(skills_list)}", self.styles['Description'])
            elements.append(skills_para)
        
        return elements
