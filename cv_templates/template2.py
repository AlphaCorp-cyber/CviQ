"""
Executive Classic CV Template
Traditional professional layout for senior positions
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
        # Header name style - more traditional
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=8,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1B1B1B'),
            fontName='Helvetica-Bold'
        ))
        
        # Contact info style - more formal
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica'
        ))
        
        # Section heading style - classic underline
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=18,
            spaceAfter=8,
            textColor=colors.HexColor('#1B1B1B'),
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        ))
        
        # Job title style - more conservative
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=10,
            spaceAfter=3,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1B1B1B')
        ))
        
        # Company/School style
        self.styles.add(ParagraphStyle(
            name='Organization',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=2,
            fontName='Helvetica',
            textColor=colors.HexColor('#444444')
        ))
        
        # Date style - right aligned
        self.styles.add(ParagraphStyle(
            name='DateStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=5,
            textColor=colors.HexColor('#666666'),
            fontName='Helvetica-Oblique',
            alignment=TA_RIGHT
        ))
        
        # Description style - formal
        self.styles.add(ParagraphStyle(
            name='Description',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=10,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#2B2B2B'),
            leading=12
        ))
        
        # Skills style - bullet points
        self.styles.add(ParagraphStyle(
            name='SkillsStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=3,
            textColor=colors.HexColor('#2B2B2B'),
            leftIndent=15,
            bulletIndent=5
        ))
        
        # Summary style - italic
        self.styles.add(ParagraphStyle(
            name='SummaryStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#2B2B2B'),
            fontName='Helvetica-Oblique',
            leading=13
        ))
    
    def generate(self, cv_data, filepath):
        """Generate CV PDF using this template"""
        try:
            # Create document with more traditional margins
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=25*mm,
                leftMargin=25*mm,
                topMargin=25*mm,
                bottomMargin=25*mm
            )
            
            story = []
            
            # Header section
            story.extend(self._create_header(cv_data))
            
            # Add horizontal line after header
            story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.HexColor('#CCCCCC')))
            story.append(Spacer(1, 12))
            
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
            logging.info(f"Template2 CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating Template2 CV: {str(e)}")
            return False
    
    def _create_header(self, cv_data):
        """Create header section with name and contact info"""
        elements = []
        
        # Name
        name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
        elements.append(name)
        
        # Contact information in a more formal layout
        contact_parts = []
        
        if cv_data.get('address'):
            contact_parts.append(cv_data['address'])
        
        if cv_data.get('phone'):
            contact_parts.append(f"Tel: {cv_data['phone']}")
        
        if cv_data.get('email'):
            contact_parts.append(f"Email: {cv_data['email']}")
        
        if contact_parts:
            # Each contact item on a separate line for formal look
            for contact_item in contact_parts:
                contact = Paragraph(contact_item, self.styles['ContactInfo'])
                elements.append(contact)
        
        elements.append(Spacer(1, 10))
        
        return elements
    
    def _create_summary_section(self, summary):
        """Create professional summary section"""
        elements = []
        
        # Section heading with underline
        heading = Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeading'])
        elements.append(heading)
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CCCCCC')))
        elements.append(Spacer(1, 8))
        
        # Summary text in italics for classic look
        summary_para = Paragraph(summary, self.styles['SummaryStyle'])
        elements.append(summary_para)
        
        return elements
    
    def _create_experience_section(self, experience_list):
        """Create work experience section"""
        elements = []
        
        # Section heading with underline
        heading = Paragraph("PROFESSIONAL EXPERIENCE", self.styles['SectionHeading'])
        elements.append(heading)
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CCCCCC')))
        elements.append(Spacer(1, 8))
        
        # Parse and display each experience
        for exp in experience_list:
            exp_elements = self._parse_experience_entry(exp)
            elements.extend(exp_elements)
        
        return elements
    
    def _parse_experience_entry(self, experience_text):
        """Parse a single experience entry with formal layout"""
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
        
        # Create a table for job title and duration alignment
        if duration:
            job_table_data = [[job_title, duration]]
            job_table = Table(job_table_data, colWidths=[12*cm, 5*cm])
            job_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, 0), 12),
                ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Oblique'),
                ('FONTSIZE', (1, 0), (1, 0), 10),
                ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#1B1B1B')),
                ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#666666')),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            elements.append(job_table)
        else:
            # Just job title
            elements.append(Paragraph(job_title, self.styles['JobTitle']))
        
        # Company
        if company:
            elements.append(Paragraph(company, self.styles['Organization']))
        
        # Description with bullet points
        if description_lines:
            description_text = ' '.join(description_lines)
            # Split into sentences and create bullet points for better readability
            sentences = [s.strip() for s in description_text.split('.') if s.strip()]
            
            if len(sentences) > 1:
                # Multiple sentences - create bullet points
                for sentence in sentences[:3]:  # Limit to first 3 points
                    if sentence:
                        bullet_text = f"• {sentence.strip()}."
                        elements.append(Paragraph(bullet_text, self.styles['Description']))
            else:
                # Single sentence or paragraph
                elements.append(Paragraph(description_text, self.styles['Description']))
        
        # Add some space between entries
        elements.append(Spacer(1, 6))
        
        return elements
    
    def _create_education_section(self, education_list):
        """Create education section"""
        elements = []
        
        # Section heading with underline
        heading = Paragraph("EDUCATION", self.styles['SectionHeading'])
        elements.append(heading)
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CCCCCC')))
        elements.append(Spacer(1, 8))
        
        # Parse and display each education entry
        for edu in education_list:
            edu_elements = self._parse_education_entry(edu)
            elements.extend(edu_elements)
        
        return elements
    
    def _parse_education_entry(self, education_text):
        """Parse a single education entry with formal layout"""
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
        
        # Create a table for degree and year alignment
        if year_info:
            edu_table_data = [[degree, year_info]]
            edu_table = Table(edu_table_data, colWidths=[12*cm, 5*cm])
            edu_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, 0), 12),
                ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Oblique'),
                ('FONTSIZE', (1, 0), (1, 0), 10),
                ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#1B1B1B')),
                ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#666666')),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            elements.append(edu_table)
        else:
            # Just degree
            elements.append(Paragraph(degree, self.styles['JobTitle']))
        
        # Institution
        if institution:
            elements.append(Paragraph(institution, self.styles['Organization']))
        
        # Additional info
        if additional_info:
            additional_text = ' '.join(additional_info)
            elements.append(Paragraph(additional_text, self.styles['Description']))
        
        # Add some space between entries
        elements.append(Spacer(1, 6))
        
        return elements
    
    def _create_skills_section(self, skills_list):
        """Create skills section with classic bullet format"""
        elements = []
        
        # Section heading with underline
        heading = Paragraph("KEY COMPETENCIES", self.styles['SectionHeading'])
        elements.append(heading)
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CCCCCC')))
        elements.append(Spacer(1, 8))
        
        # Create skills display
        if isinstance(skills_list, list):
            # Display skills as bullet points in two columns
            skills_table_data = []
            
            # Group skills in pairs for two-column layout
            for i in range(0, len(skills_list), 2):
                left_skill = f"• {skills_list[i]}" if i < len(skills_list) else ""
                right_skill = f"• {skills_list[i+1]}" if i+1 < len(skills_list) else ""
                skills_table_data.append([left_skill, right_skill])
            
            if skills_table_data:
                skills_table = Table(skills_table_data, colWidths=[8.5*cm, 8.5*cm])
                skills_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2B2B2B')),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ]))
                elements.append(skills_table)
        else:
            # If skills is a string, display as paragraph with bullet points
            skills_text = str(skills_list)
            if ',' in skills_text:
                # Split by comma and create bullet points
                skill_items = [skill.strip() for skill in skills_text.split(',') if skill.strip()]
                for skill in skill_items:
                    bullet_text = f"• {skill}"
                    elements.append(Paragraph(bullet_text, self.styles['SkillsStyle']))
            else:
                elements.append(Paragraph(f"• {skills_text}", self.styles['SkillsStyle']))
        
        return elements
