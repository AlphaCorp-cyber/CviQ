
"""
Academic CV Template
Designed for researchers, professors, and academic professionals
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
        """Setup academic-focused styles"""
        # Academic header
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#4A148C'),
            fontName='Helvetica-Bold'
        ))
        
        # Academic title
        self.styles.add(ParagraphStyle(
            name='AcademicTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=4,
            textColor=colors.HexColor('#6A1B9A'),
            fontName='Helvetica-Oblique'
        ))
        
        # Contact info
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.HexColor('#424242')
        ))
        
        # Academic section headings
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=8,
            textColor=colors.HexColor('#4A148C'),
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=colors.HexColor('#4A148C'),
            borderPadding=0
        ))
        
        # Position title
        self.styles.add(ParagraphStyle(
            name='Position',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=8,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#4A148C')
        ))
        
        # Institution
        self.styles.add(ParagraphStyle(
            name='Institution',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=2,
            fontName='Helvetica-Oblique',
            textColor=colors.HexColor('#6A1B9A')
        ))
        
        # Academic dates
        self.styles.add(ParagraphStyle(
            name='AcademicDate',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            textColor=colors.HexColor('#757575'),
            alignment=TA_RIGHT
        ))
        
        # Publication style
        self.styles.add(ParagraphStyle(
            name='Publication',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#212121'),
            leftIndent=10,
            hangingIndent=10
        ))
    
    def generate(self, cv_data, filepath):
        """Generate academic CV"""
        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=25*mm,
                leftMargin=25*mm,
                topMargin=25*mm,
                bottomMargin=25*mm
            )
            
            story = []
            
            # Header
            story.extend(self._create_header(cv_data))
            
            # Research interests/summary
            if cv_data.get('summary'):
                story.extend(self._create_summary_section(cv_data['summary']))
            
            # Academic positions
            if cv_data.get('experience'):
                story.extend(self._create_experience_section(cv_data['experience']))
            
            # Education
            if cv_data.get('education'):
                story.extend(self._create_education_section(cv_data['education']))
            
            # Research areas/skills
            if cv_data.get('skills'):
                story.extend(self._create_skills_section(cv_data['skills']))
            
            doc.build(story)
            logging.info(f"Template7 CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating Template7 CV: {str(e)}")
            return False
    
    def _create_header(self, cv_data):
        """Create academic header"""
        elements = []
        
        # Name
        name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
        elements.append(name)
        
        # Academic title (if applicable)
        title = Paragraph("Ph.D. Candidate / Researcher", self.styles['AcademicTitle'])
        elements.append(title)
        
        # Contact info
        contact_parts = []
        if cv_data.get('email'):
            contact_parts.append(cv_data['email'])
        if cv_data.get('phone'):
            contact_parts.append(cv_data['phone'])
        if cv_data.get('address'):
            contact_parts.append(cv_data['address'])
        
        if contact_parts:
            contact_text = " • ".join(contact_parts)
            contact = Paragraph(contact_text, self.styles['ContactInfo'])
            elements.append(contact)
        
        return elements
    
    def _create_summary_section(self, summary):
        """Create research interests section"""
        elements = []
        heading = Paragraph("RESEARCH INTERESTS", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Add underline
        underline = Paragraph("_" * 50, self.styles['SectionHeading'])
        elements.append(underline)
        elements.append(Spacer(1, 6))
        
        summary_para = Paragraph(summary, self.styles['Publication'])
        elements.append(summary_para)
        return elements
    
    def _create_experience_section(self, experience_list):
        """Create academic positions section"""
        elements = []
        heading = Paragraph("ACADEMIC POSITIONS", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Add underline
        underline = Paragraph("_" * 50, self.styles['SectionHeading'])
        elements.append(underline)
        elements.append(Spacer(1, 6))
        
        for exp in experience_list:
            exp_elements = self._parse_experience_entry(exp)
            elements.extend(exp_elements)
        
        return elements
    
    def _parse_experience_entry(self, experience_text):
        """Parse academic position entry"""
        elements = []
        lines = [line.strip() for line in experience_text.split('\n') if line.strip()]
        
        if not lines:
            return elements
        
        first_line = lines[0]
        if ' at ' in first_line:
            parts = first_line.split(' at ', 1)
            position = parts[0].strip()
            institution = parts[1].strip()
        else:
            position = first_line
            institution = ""
        
        # Create table for position and dates
        position_data = []
        dates = ""
        
        # Find dates in subsequent lines
        for line in lines[1:]:
            if any(keyword in line.lower() for keyword in ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                          'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
                                                          '20', '19', 'present', 'current', '-']):
                dates = line
                break
        
        if dates:
            position_table = Table([[position, dates]], colWidths=[12*cm, 5*cm])
            position_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, 0), 12),
                ('FONTNAME', (1, 0), (1, 0), 'Helvetica'),
                ('FONTSIZE', (1, 0), (1, 0), 10),
                ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#4A148C')),
                ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#757575')),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            elements.append(position_table)
        else:
            elements.append(Paragraph(position, self.styles['Position']))
        
        if institution:
            elements.append(Paragraph(institution, self.styles['Institution']))
        
        # Add description if any
        description_lines = [line for line in lines[1:] if not any(keyword in line.lower() for keyword in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', '20', '19', 'present', 'current', '-'])]
        
        if description_lines:
            description_text = ' '.join(description_lines)
            elements.append(Paragraph(description_text, self.styles['Publication']))
        
        elements.append(Spacer(1, 8))
        return elements
    
    def _create_education_section(self, education_list):
        """Create academic education section"""
        elements = []
        heading = Paragraph("EDUCATION", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Add underline
        underline = Paragraph("_" * 50, self.styles['SectionHeading'])
        elements.append(underline)
        elements.append(Spacer(1, 6))
        
        for edu in education_list:
            edu_elements = self._parse_education_entry(edu)
            elements.extend(edu_elements)
        
        return elements
    
    def _parse_education_entry(self, education_text):
        """Parse academic education entry"""
        elements = []
        lines = [line.strip() for line in education_text.split('\n') if line.strip()]
        
        if not lines:
            return elements
        
        first_line = lines[0]
        if ' at ' in first_line or ' from ' in first_line:
            parts = first_line.split(' at ' if ' at ' in first_line else ' from ', 1)
            degree = parts[0].strip()
            institution = parts[1].strip()
        else:
            degree = first_line
            institution = ""
        
        # Find year
        year = ""
        for line in lines[1:]:
            if any(keyword in line for keyword in ['20', '19']) and len(line) < 20:
                year = line
                break
        
        if year:
            edu_table = Table([[degree, year]], colWidths=[12*cm, 5*cm])
            edu_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, 0), 12),
                ('FONTNAME', (1, 0), (1, 0), 'Helvetica'),
                ('FONTSIZE', (1, 0), (1, 0), 10),
                ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#4A148C')),
                ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#757575')),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            elements.append(edu_table)
        else:
            elements.append(Paragraph(degree, self.styles['Position']))
        
        if institution:
            elements.append(Paragraph(institution, self.styles['Institution']))
        
        elements.append(Spacer(1, 6))
        return elements
    
    def _create_skills_section(self, skills_list):
        """Create research areas section"""
        elements = []
        heading = Paragraph("RESEARCH AREAS & COMPETENCIES", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Add underline
        underline = Paragraph("_" * 50, self.styles['SectionHeading'])
        elements.append(underline)
        elements.append(Spacer(1, 6))
        
        if isinstance(skills_list, list):
            for skill in skills_list:
                skill_para = Paragraph(f"• {skill}", self.styles['Publication'])
                elements.append(skill_para)
        else:
            skills_para = Paragraph(str(skills_list), self.styles['Publication'])
            elements.append(skills_para)
        
        return elements
