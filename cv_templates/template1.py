"""
Modern Professional CV Template
Clean and modern design suitable for all industries
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
        """Setup custom paragraph styles for this template"""
        # Header name style
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=28,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2C3E50'),
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
        
        # Section heading style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#2980B9'),
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#2980B9'),
            borderPadding=5,
            backColor=colors.HexColor('#F8F9FA')
        ))
        
        # Job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=8,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#2C3E50')
        ))
        
        # Company/School style
        self.styles.add(ParagraphStyle(
            name='Organization',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=2,
            fontName='Helvetica-Oblique',
            textColor=colors.HexColor('#7F8C8D')
        ))
        
        # Date style
        self.styles.add(ParagraphStyle(
            name='DateStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            textColor=colors.HexColor('#95A5A6')
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
        
        # Skills style
        self.styles.add(ParagraphStyle(
            name='SkillsStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            textColor=colors.HexColor('#2C3E50')
        ))
    
    def generate(self, cv_data, filepath):
        """Generate CV PDF using this template"""
        try:
            # Create document
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
            logging.info(f"Template1 CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating Template1 CV: {str(e)}")
            return False
    
    def _create_header(self, cv_data):
        """Create header section with name and contact info"""
        elements = []
        
        # Name
        name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
        elements.append(name)
        
        # Contact information
        contact_parts = []
        
        if cv_data.get('email'):
            contact_parts.append(f"📧 {cv_data['email']}")
        
        if cv_data.get('phone'):
            contact_parts.append(f"📱 {cv_data['phone']}")
        
        if cv_data.get('address'):
            contact_parts.append(f"🏠 {cv_data['address']}")
        
        if contact_parts:
            contact_text = " | ".join(contact_parts)
            contact = Paragraph(contact_text, self.styles['ContactInfo'])
            elements.append(contact)
        
        return elements
    
    def _create_summary_section(self, summary):
        """Create professional summary section"""
        elements = []
        
        # Section heading
        heading = Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Summary text
        summary_para = Paragraph(summary, self.styles['Description'])
        elements.append(summary_para)
        
        return elements
    
    def _create_experience_section(self, experience_list):
        """Create work experience section"""
        elements = []
        
        # Section heading
        heading = Paragraph("WORK EXPERIENCE", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Parse and display each experience
        for exp in experience_list:
            exp_elements = self._parse_experience_entry(exp)
            elements.extend(exp_elements)
        
        return elements
    
    def _parse_experience_entry(self, experience_text):
        """Parse a single experience entry"""
        elements = []
        
        # Split the experience text into lines
        lines = [line.strip() for line in experience_text.split('\n') if line.strip()]
        
        if not lines:
            return elements
        
        # First line should contain job title and company
        first_line = lines[0]
        
        # Try to parse job title and company
        if ' at ' in first_line:
            parts = first_line.split(' at ', 1)
            job_title = parts[0].strip()
            company = parts[1].strip()
        else:
            job_title = first_line
            company = ""
        
        # Job title
        elements.append(Paragraph(job_title, self.styles['JobTitle']))
        
        # Company
        if company:
            elements.append(Paragraph(company, self.styles['Organization']))
        
        # Look for duration in subsequent lines
        duration = ""
        description_lines = []
        
        for line in lines[1:]:
            # Check if line looks like a date range
            if any(keyword in line.lower() for keyword in ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                          'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
                                                          '20', '19', 'present', 'current', '-']):
                if not duration:  # Only take the first date-like line
                    duration = line
                else:
                    description_lines.append(line)
            else:
                description_lines.append(line)
        
        # Duration
        if duration:
            elements.append(Paragraph(duration, self.styles['DateStyle']))
        
        # Description
        if description_lines:
            description_text = ' '.join(description_lines)
            elements.append(Paragraph(description_text, self.styles['Description']))
        
        return elements
    
    def _create_education_section(self, education_list):
        """Create education section"""
        elements = []
        
        # Section heading
        heading = Paragraph("EDUCATION", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Parse and display each education entry
        for edu in education_list:
            edu_elements = self._parse_education_entry(edu)
            elements.extend(edu_elements)
        
        return elements
    
    def _parse_education_entry(self, education_text):
        """Parse a single education entry"""
        elements = []
        
        # Split the education text into lines
        lines = [line.strip() for line in education_text.split('\n') if line.strip()]
        
        if not lines:
            return elements
        
        # First line should contain degree/qualification
        first_line = lines[0]
        
        # Try to parse degree and institution
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
        
        # Degree/Qualification
        elements.append(Paragraph(degree, self.styles['JobTitle']))
        
        # Institution
        if institution:
            elements.append(Paragraph(institution, self.styles['Organization']))
        
        # Look for year/duration and additional info
        year_info = ""
        additional_info = []
        
        for line in lines[1:]:
            # Check if line looks like a year
            if any(keyword in line for keyword in ['20', '19']) and len(line) < 20:
                if not year_info:
                    year_info = line
                else:
                    additional_info.append(line)
            else:
                additional_info.append(line)
        
        # Year
        if year_info:
            elements.append(Paragraph(year_info, self.styles['DateStyle']))
        
        # Additional info
        if additional_info:
            additional_text = ' '.join(additional_info)
            elements.append(Paragraph(additional_text, self.styles['Description']))
        
        return elements
    
    def _create_skills_section(self, skills_list):
        """Create skills section"""
        elements = []
        
        # Section heading
        heading = Paragraph("SKILLS", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Create skills display
        if isinstance(skills_list, list):
            # Group skills in rows of 3
            skills_rows = []
            for i in range(0, len(skills_list), 3):
                row_skills = skills_list[i:i+3]
                skills_rows.append(row_skills)
            
            # Create table for better layout
            table_data = []
            for row in skills_rows:
                # Pad row to have 3 columns
                while len(row) < 3:
                    row.append("")
                table_data.append([f"• {skill}" if skill else "" for skill in row])
            
            if table_data:
                skills_table = Table(table_data, colWidths=[6*cm, 6*cm, 6*cm])
                skills_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ]))
                elements.append(skills_table)
        else:
            # If skills is a string, display as paragraph
            skills_text = str(skills_list)
            elements.append(Paragraph(skills_text, self.styles['SkillsStyle']))
        
        return elements
