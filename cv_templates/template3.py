
"""
Premium Executive CV Template
Sophisticated and elegant design for executive professionals
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
        """Setup premium paragraph styles for this template"""
        # Premium header name style - elegant and sophisticated
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=28,
            spaceAfter=4,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#1A237E'),
            fontName='Helvetica-Bold',
            leftIndent=30*mm
        ))
        
        # Professional title style
        self.styles.add(ParagraphStyle(
            name='ProfessionalTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=8,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#3949AB'),
            fontName='Helvetica-Oblique',
            leftIndent=30*mm
        ))
        
        # Contact info style - clean and minimal
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            spaceAfter=25,
            textColor=colors.HexColor('#37474F'),
            leftIndent=30*mm
        ))
        
        # Premium section heading style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=25,
            spaceAfter=12,
            textColor=colors.HexColor('#1A237E'),
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=colors.HexColor('#E8EAF6'),
            borderPadding=0,
            leftIndent=0,
            borderRadius=0
        ))
        
        # Executive job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=10,
            spaceAfter=3,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1A237E')
        ))
        
        # Premium organization style
        self.styles.add(ParagraphStyle(
            name='Organization',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=2,
            fontName='Helvetica',
            textColor=colors.HexColor('#3949AB')
        ))
        
        # Elegant date style
        self.styles.add(ParagraphStyle(
            name='DateStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=colors.HexColor('#607D8B'),
            fontName='Helvetica-Oblique'
        ))
        
        # Premium description style
        self.styles.add(ParagraphStyle(
            name='Description',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#263238'),
            leading=14
        ))
        
        # Executive summary style
        self.styles.add(ParagraphStyle(
            name='ExecutiveSummary',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=15,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#263238'),
            leading=16,
            firstLineIndent=0
        ))
        
        # Skills highlight style
        self.styles.add(ParagraphStyle(
            name='SkillsHighlight',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            textColor=colors.HexColor('#1A237E'),
            fontName='Helvetica-Bold'
        ))
    
    def generate(self, cv_data, filepath):
        """Generate premium executive CV PDF"""
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
            
            # Add premium header with sidebar design
            story.extend(self._create_premium_header(cv_data))
            
            # Add elegant divider
            story.append(self._create_elegant_divider())
            
            # Executive summary
            if cv_data.get('summary'):
                story.extend(self._create_executive_summary(cv_data['summary']))
            
            # Professional experience
            if cv_data.get('experience'):
                story.extend(self._create_premium_experience_section(cv_data['experience']))
            
            # Education & qualifications
            if cv_data.get('education'):
                story.extend(self._create_education_section(cv_data['education']))
            
            # Core competencies
            if cv_data.get('skills'):
                story.extend(self._create_premium_skills_section(cv_data['skills']))
            
            # Build PDF
            doc.build(story)
            logging.info(f"Premium Template3 CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating Premium Template3 CV: {str(e)}")
            return False
    
    def _create_premium_header(self, cv_data):
        """Create sophisticated header with sidebar accent"""
        elements = []
        
        # Name
        name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
        elements.append(name)
        
        # Professional title
        title = Paragraph("EXECUTIVE PROFESSIONAL", self.styles['ProfessionalTitle'])
        elements.append(title)
        
        # Contact information
        contact_parts = []
        if cv_data.get('email'):
            contact_parts.append(f"Email: {cv_data['email']}")
        if cv_data.get('phone'):
            contact_parts.append(f"Phone: {cv_data['phone']}")
        if cv_data.get('address'):
            contact_parts.append(f"Address: {cv_data['address']}")
        
        if contact_parts:
            contact_text = " | ".join(contact_parts)
            contact = Paragraph(contact_text, self.styles['ContactInfo'])
            elements.append(contact)
        
        # Add elegant divider
        elements.append(HRFlowable(width="100%", thickness=3, lineCap='round', 
                                 color=colors.HexColor('#1A237E'), spaceBefore=10, spaceAfter=20))
        
        return elements
    
    def _create_elegant_divider(self):
        """Create an elegant section divider"""
        return HRFlowable(width="100%", thickness=1, lineCap='round', 
                         color=colors.HexColor('#E8EAF6'), spaceBefore=10, spaceAfter=10)
    
    def _create_executive_summary(self, summary):
        """Create executive summary section"""
        elements = []
        heading = Paragraph("EXECUTIVE SUMMARY", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Add elegant underline
        elements.append(HRFlowable(width="30%", thickness=2, lineCap='round', 
                                 color=colors.HexColor('#3949AB'), spaceBefore=2, spaceAfter=12))
        
        summary_para = Paragraph(summary, self.styles['ExecutiveSummary'])
        elements.append(summary_para)
        return elements
    
    def _create_premium_experience_section(self, experience_list):
        """Create premium experience section"""
        elements = []
        heading = Paragraph("PROFESSIONAL EXPERIENCE", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Add elegant underline
        elements.append(HRFlowable(width="30%", thickness=2, lineCap='round', 
                                 color=colors.HexColor('#3949AB'), spaceBefore=2, spaceAfter=15))
        
        for exp in experience_list:
            exp_elements = self._parse_premium_experience_entry(exp)
            
            # Wrap each experience in a keep-together block
            if exp_elements:
                keep_together = KeepTogether(exp_elements)
                elements.append(keep_together)
                elements.append(Spacer(1, 15))
        
        return elements
    
    def _parse_premium_experience_entry(self, experience_text):
        """Parse experience entry with premium formatting"""
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
        
        # Create job title and company in a table for better alignment
        job_data = []
        if company:
            job_content = f"""
            <para fontSize="12" fontName="Helvetica-Bold" textColor="#1A237E">
            {job_title}
            </para>
            <para fontSize="11" textColor="#3949AB" spaceAfter="2">
            {company}
            </para>
            """
        else:
            job_content = f"""
            <para fontSize="12" fontName="Helvetica-Bold" textColor="#1A237E">
            {job_title}
            </para>
            """
        
        job_data.append([Paragraph(job_content, self.styles['Normal'])])
        
        job_table = Table(job_data, colWidths=[16*cm])
        job_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FAFAFA')),
            ('LINEABOVE', (0, 0), (-1, -1), 1, colors.HexColor('#E8EAF6')),
        ]))
        
        elements.append(job_table)
        
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
        """Create premium education section"""
        elements = []
        heading = Paragraph("EDUCATION & QUALIFICATIONS", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Add elegant underline
        elements.append(HRFlowable(width="30%", thickness=2, lineCap='round', 
                                 color=colors.HexColor('#3949AB'), spaceBefore=2, spaceAfter=15))
        
        for edu in education_list:
            edu_elements = self._parse_premium_education_entry(edu)
            elements.extend(edu_elements)
        
        return elements
    
    def _parse_premium_education_entry(self, education_text):
        """Parse education entry with premium formatting"""
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
        
        # Create education table for consistent formatting
        edu_data = []
        if institution:
            edu_content = f"""
            <para fontSize="11" fontName="Helvetica-Bold" textColor="#1A237E">
            {degree}
            </para>
            <para fontSize="10" textColor="#3949AB">
            {institution}
            </para>
            """
        else:
            edu_content = f"""
            <para fontSize="11" fontName="Helvetica-Bold" textColor="#1A237E">
            {degree}
            </para>
            """
        
        edu_data.append([Paragraph(edu_content, self.styles['Normal'])])
        
        edu_table = Table(edu_data, colWidths=[16*cm])
        edu_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(edu_table)
        
        return elements
    
    def _create_premium_skills_section(self, skills_list):
        """Create premium skills section with sophisticated layout"""
        elements = []
        heading = Paragraph("CORE COMPETENCIES", self.styles['SectionHeading'])
        elements.append(heading)
        
        # Add elegant underline
        elements.append(HRFlowable(width="30%", thickness=2, lineCap='round', 
                                 color=colors.HexColor('#3949AB'), spaceBefore=2, spaceAfter=15))
        
        if isinstance(skills_list, list):
            # Create skills in a professional grid layout
            skills_data = []
            skills_per_row = 3
            
            for i in range(0, len(skills_list), skills_per_row):
                row_skills = skills_list[i:i+skills_per_row]
                skill_cells = []
                
                for skill in row_skills:
                    skill_content = f"""
                    <para fontSize="10" fontName="Helvetica-Bold" textColor="#1A237E">
                    • {skill}
                    </para>
                    """
                    skill_cells.append(Paragraph(skill_content, self.styles['Normal']))
                
                # Fill empty cells if needed
                while len(skill_cells) < skills_per_row:
                    skill_cells.append(Paragraph("", self.styles['Normal']))
                
                skills_data.append(skill_cells)
            
            skills_table = Table(skills_data, colWidths=[5.3*cm, 5.3*cm, 5.3*cm])
            skills_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            
            elements.append(skills_table)
        else:
            skills_para = Paragraph(str(skills_list), self.styles['Description'])
            elements.append(skills_para)
        
        return elements
