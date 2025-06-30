
"""
Creative Modern CV Template
Colorful and modern design for creative professionals
"""

import json
import logging
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

class TemplateGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup custom paragraph styles for this template"""
        # Header name style - creative and bold
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=32,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#E74C3C'),
            fontName='Helvetica-Bold'
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.HexColor('#34495E')
        ))
        
        # Section heading style - colorful
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#3498DB'),
            borderPadding=8
        ))
        
        # Job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=13,
            spaceBefore=8,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#E74C3C')
        ))
        
        # Organization style
        self.styles.add(ParagraphStyle(
            name='Organization',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=2,
            fontName='Helvetica-Oblique',
            textColor=colors.HexColor('#27AE60')
        ))
        
        # Date style
        self.styles.add(ParagraphStyle(
            name='DateStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            textColor=colors.HexColor('#F39C12'),
            fontName='Helvetica-Bold'
        ))
        
        # Description style
        self.styles.add(ParagraphStyle(
            name='Description',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#2C3E50')
        ))
    
    def generate(self, cv_data, filepath):
        """Generate CV PDF using this template"""
        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=20*mm,
                leftMargin=20*mm,
                topMargin=20*mm,
                bottomMargin=20*mm
            )
            
            story = []
            
            # Header section
            story.extend(self._create_header(cv_data))
            
            # Professional summary
            if cv_data.get('summary'):
                story.extend(self._create_summary_section(cv_data['summary']))
            
            # Work experience
            if cv_data.get('experience'):
                story.extend(self._create_experience_section(cv_data['experience']))
            
            # Education
            if cv_data.get('education'):
                story.extend(self._create_education_section(cv_data['education']))
            
            # Skills
            if cv_data.get('skills'):
                story.extend(self._create_skills_section(cv_data['skills']))
            
            # Build PDF
            doc.build(story)
            logging.info(f"Template3 CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating Template3 CV: {str(e)}")
            return False
    
    def _create_header(self, cv_data):
        """Create colorful header section"""
        elements = []
        
        # Name with colorful background
        name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
        elements.append(name)
        
        # Contact information with icons
        contact_parts = []
        if cv_data.get('email'):
            contact_parts.append(f"✉ {cv_data['email']}")
        if cv_data.get('phone'):
            contact_parts.append(f"☎ {cv_data['phone']}")
        if cv_data.get('address'):
            contact_parts.append(f"⌂ {cv_data['address']}")
        
        if contact_parts:
            contact_text = " • ".join(contact_parts)
            contact = Paragraph(contact_text, self.styles['ContactInfo'])
            elements.append(contact)
        
        return elements
    
    def _create_summary_section(self, summary):
        """Create summary section"""
        elements = []
        heading = Paragraph("ABOUT ME", self.styles['SectionHeading'])
        elements.append(heading)
        summary_para = Paragraph(summary, self.styles['Description'])
        elements.append(summary_para)
        return elements
    
    def _create_experience_section(self, experience_list):
        """Create experience section"""
        elements = []
        heading = Paragraph("EXPERIENCE", self.styles['SectionHeading'])
        elements.append(heading)
        
        for exp in experience_list:
            exp_elements = self._parse_experience_entry(exp)
            elements.extend(exp_elements)
        
        return elements
    
    def _parse_experience_entry(self, experience_text):
        """Parse experience entry"""
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
        duration = ""
        description_lines = []
        
        for line in lines[1:]:
            if any(keyword in line.lower() for keyword in ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                          'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
                                                          '20', '19', 'present', 'current', '-']):
                if not duration:
                    duration = line
                else:
                    description_lines.append(line)
            else:
                description_lines.append(line)
        
        if duration:
            elements.append(Paragraph(duration, self.styles['DateStyle']))
        
        if description_lines:
            description_text = ' '.join(description_lines)
            elements.append(Paragraph(description_text, self.styles['Description']))
        
        return elements
    
    def _create_education_section(self, education_list):
        """Create education section"""
        elements = []
        heading = Paragraph("EDUCATION", self.styles['SectionHeading'])
        elements.append(heading)
        
        for edu in education_list:
            edu_elements = self._parse_education_entry(edu)
            elements.extend(edu_elements)
        
        return elements
    
    def _parse_education_entry(self, education_text):
        """Parse education entry"""
        elements = []
        lines = [line.strip() for line in education_text.split('\n') if line.strip()]
        
        if not lines:
            return elements
        
        first_line = lines[0]
        if ' at ' in first_line:
            parts = first_line.split(' at ', 1)
            degree = parts[0].strip()
            institution = parts[1].strip()
        elif ' from ' in first_line:
            parts = first_line.split(' from ', 1)
            degree = parts[0].strip()
            institution = parts[1].strip()
        else:
            degree = first_line
            institution = ""
        
        elements.append(Paragraph(degree, self.styles['JobTitle']))
        if institution:
            elements.append(Paragraph(institution, self.styles['Organization']))
        
        return elements
    
    def _create_skills_section(self, skills_list):
        """Create colorful skills section"""
        elements = []
        heading = Paragraph("SKILLS", self.styles['SectionHeading'])
        elements.append(heading)
        
        if isinstance(skills_list, list):
            # Create colorful skill tags
            skills_text = ""
            for skill in skills_list:
                skills_text += f"<b>{skill}</b> • "
            skills_text = skills_text.rstrip(" • ")
            
            skills_para = Paragraph(skills_text, self.styles['Description'])
            elements.append(skills_para)
        else:
            skills_para = Paragraph(str(skills_list), self.styles['Description'])
            elements.append(skills_para)
        
        return elements
