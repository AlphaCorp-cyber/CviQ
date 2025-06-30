
"""
Minimalist CV Template
Clean and simple design focusing on content
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
        """Setup minimal custom styles"""
        # Simple name style
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=26,
            spaceAfter=8,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica'
        ))
        
        # Minimal contact style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            spaceAfter=16,
            textColor=colors.HexColor('#666666')
        ))
        
        # Simple section headings
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceBefore=16,
            spaceAfter=6,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=colors.HexColor('#CCCCCC'),
            borderPadding=0
        ))
        
        # Clean job title
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceBefore=6,
            spaceAfter=1,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#333333')
        ))
        
        # Simple organization
        self.styles.add(ParagraphStyle(
            name='Organization',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=1,
            fontName='Helvetica',
            textColor=colors.HexColor('#666666')
        ))
        
        # Minimal date style
        self.styles.add(ParagraphStyle(
            name='DateStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=3,
            textColor=colors.HexColor('#999999')
        ))
        
        # Clean description
        self.styles.add(ParagraphStyle(
            name='Description',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#333333'),
            leading=12
        ))
    
    def generate(self, cv_data, filepath):
        """Generate minimal CV"""
        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=30*mm,
                leftMargin=30*mm,
                topMargin=25*mm,
                bottomMargin=25*mm
            )
            
            story = []
            
            # Header
            story.extend(self._create_header(cv_data))
            
            # Summary
            if cv_data.get('summary'):
                story.extend(self._create_summary_section(cv_data['summary']))
            
            # Experience
            if cv_data.get('experience'):
                story.extend(self._create_experience_section(cv_data['experience']))
            
            # Education
            if cv_data.get('education'):
                story.extend(self._create_education_section(cv_data['education']))
            
            # Skills
            if cv_data.get('skills'):
                story.extend(self._create_skills_section(cv_data['skills']))
            
            doc.build(story)
            logging.info(f"Template4 CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating Template4 CV: {str(e)}")
            return False
    
    def _create_header(self, cv_data):
        """Create minimal header"""
        elements = []
        
        # Name
        name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
        elements.append(name)
        
        # Contact info - one line
        contact_parts = []
        if cv_data.get('email'):
            contact_parts.append(cv_data['email'])
        if cv_data.get('phone'):
            contact_parts.append(cv_data['phone'])
        if cv_data.get('address'):
            contact_parts.append(cv_data['address'])
        
        if contact_parts:
            contact_text = " | ".join(contact_parts)
            contact = Paragraph(contact_text, self.styles['ContactInfo'])
            elements.append(contact)
        
        return elements
    
    def _create_summary_section(self, summary):
        """Create simple summary"""
        elements = []
        heading = Paragraph("Summary", self.styles['SectionHeading'])
        elements.append(heading)
        summary_para = Paragraph(summary, self.styles['Description'])
        elements.append(summary_para)
        return elements
    
    def _create_experience_section(self, experience_list):
        """Create clean experience section"""
        elements = []
        heading = Paragraph("Experience", self.styles['SectionHeading'])
        elements.append(heading)
        
        for exp in experience_list:
            exp_elements = self._parse_experience_entry(exp)
            elements.extend(exp_elements)
        
        return elements
    
    def _parse_experience_entry(self, experience_text):
        """Parse experience with minimal formatting"""
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
        
        # Find duration and description
        for line in lines[1:]:
            if any(keyword in line.lower() for keyword in ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                          'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
                                                          '20', '19', 'present', 'current', '-']):
                elements.append(Paragraph(line, self.styles['DateStyle']))
            else:
                elements.append(Paragraph(line, self.styles['Description']))
        
        return elements
    
    def _create_education_section(self, education_list):
        """Create simple education section"""
        elements = []
        heading = Paragraph("Education", self.styles['SectionHeading'])
        elements.append(heading)
        
        for edu in education_list:
            elements.append(Paragraph(edu, self.styles['Description']))
        
        return elements
    
    def _create_skills_section(self, skills_list):
        """Create minimal skills section"""
        elements = []
        heading = Paragraph("Skills", self.styles['SectionHeading'])
        elements.append(heading)
        
        if isinstance(skills_list, list):
            skills_text = ", ".join(skills_list)
        else:
            skills_text = str(skills_list)
        
        skills_para = Paragraph(skills_text, self.styles['Description'])
        elements.append(skills_para)
        
        return elements
