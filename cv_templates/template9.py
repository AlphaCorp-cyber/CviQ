
"""
Finance Professional CV Template
Designed for banking, finance, and investment professionals
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
        """Setup finance-focused styles"""
        # Professional finance header
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=26,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1565C0'),
            fontName='Helvetica-Bold'
        ))
        
        # Finance credentials
        self.styles.add(ParagraphStyle(
            name='FinanceTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=4,
            textColor=colors.HexColor('#1976D2'),
            fontName='Helvetica-Bold'
        ))
        
        # Contact info
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=18,
            textColor=colors.HexColor('#424242')
        ))
        
        # Finance section headings
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=18,
            spaceAfter=8,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#1976D2'),
            borderPadding=6
        ))
        
        # Position title
        self.styles.add(ParagraphStyle(
            name='Position',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=8,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1565C0')
        ))
        
        # Financial institution
        self.styles.add(ParagraphStyle(
            name='Institution',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=2,
            fontName='Helvetica',
            textColor=colors.HexColor('#424242')
        ))
        
        # Achievement with financial metrics
        self.styles.add(ParagraphStyle(
            name='FinancialAchievement',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#1565C0'),
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
        
        # Financial metrics table style
        self.styles.add(ParagraphStyle(
            name='Metrics',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=4,
            textColor=colors.HexColor('#1976D2'),
            fontName='Courier'
        ))
    
    def generate(self, cv_data, filepath):
        """Generate finance CV"""
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
            
            # Header
            story.extend(self._create_header(cv_data))
            
            # Executive summary
            if cv_data.get('summary'):
                story.extend(self._create_summary_section(cv_data['summary']))
            
            # Professional experience
            if cv_data.get('experience'):
                story.extend(self._create_experience_section(cv_data['experience']))
            
            # Education
            if cv_data.get('education'):
                story.extend(self._create_education_section(cv_data['education']))
            
            # Financial competencies
            if cv_data.get('skills'):
                story.extend(self._create_skills_section(cv_data['skills']))
            
            doc.build(story)
            logging.info(f"Template9 CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating Template9 CV: {str(e)}")
            return False
    
    def _create_header(self, cv_data):
        """Create finance professional header"""
        elements = []
        
        # Name
        name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
        elements.append(name)
        
        # Finance credentials
        title = Paragraph("CFA | Finance Professional", self.styles['FinanceTitle'])
        elements.append(title)
        
        # Contact info with finance symbols
        contact_parts = []
        if cv_data.get('phone'):
            contact_parts.append(f"📞 {cv_data['phone']}")
        if cv_data.get('email'):
            contact_parts.append(f"📧 {cv_data['email']}")
        if cv_data.get('address'):
            contact_parts.append(f"💼 {cv_data['address']}")
        
        if contact_parts:
            contact_text = " | ".join(contact_parts)
            contact = Paragraph(contact_text, self.styles['ContactInfo'])
            elements.append(contact)
        
        return elements
    
    def _create_summary_section(self, summary):
        """Create executive summary"""
        elements = []
        heading = Paragraph("EXECUTIVE SUMMARY", self.styles['SectionHeading'])
        elements.append(heading)
        summary_para = Paragraph(summary, self.styles['Description'])
        elements.append(summary_para)
        return elements
    
    def _create_experience_section(self, experience_list):
        """Create professional experience with financial focus"""
        elements = []
        heading = Paragraph("PROFESSIONAL EXPERIENCE", self.styles['SectionHeading'])
        elements.append(heading)
        
        for exp in experience_list:
            exp_elements = self._parse_experience_entry(exp)
            elements.extend(exp_elements)
        
        return elements
    
    def _parse_experience_entry(self, experience_text):
        """Parse with financial achievements focus"""
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
        
        elements.append(Paragraph(f"💼 {position}", self.styles['Position']))
        if institution:
            elements.append(Paragraph(institution, self.styles['Institution']))
        
        # Highlight financial achievements
        for line in lines[1:]:
            # Check for financial metrics
            if any(indicator in line for indicator in ['$', '%', 'million', 'billion', 'thousand', 'ROI', 'profit', 'revenue', 'portfolio', 'assets']):
                achievement_text = f"💰 {line}"
                elements.append(Paragraph(achievement_text, self.styles['FinancialAchievement']))
            elif any(keyword in line.lower() for keyword in ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                            'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
                                                            '20', '19', 'present', 'current', '-']):
                # Date formatting
                date_text = f"📅 {line}"
                elements.append(Paragraph(date_text, self.styles['Description']))
            else:
                elements.append(Paragraph(f"• {line}", self.styles['Description']))
        
        elements.append(Spacer(1, 8))
        return elements
    
    def _create_education_section(self, education_list):
        """Create education section"""
        elements = []
        heading = Paragraph("EDUCATION & CERTIFICATIONS", self.styles['SectionHeading'])
        elements.append(heading)
        
        for edu in education_list:
            edu_elements = self._parse_education_entry(edu)
            elements.extend(edu_elements)
        
        return elements
    
    def _parse_education_entry(self, education_text):
        """Parse education with finance focus"""
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
        
        elements.append(Paragraph(f"🎓 {degree}", self.styles['Position']))
        if institution:
            elements.append(Paragraph(institution, self.styles['Institution']))
        
        # Add additional details
        for line in lines[1:]:
            if any(keyword in line for keyword in ['20', '19']) and len(line) < 20:
                elements.append(Paragraph(f"📅 {line}", self.styles['Description']))
            else:
                elements.append(Paragraph(line, self.styles['Description']))
        
        elements.append(Spacer(1, 6))
        return elements
    
    def _create_skills_section(self, skills_list):
        """Create financial competencies section"""
        elements = []
        heading = Paragraph("CORE COMPETENCIES", self.styles['SectionHeading'])
        elements.append(heading)
        
        if isinstance(skills_list, list):
            # Categorize financial skills
            analytical = []
            software = []
            certifications = []
            markets = []
            
            for skill in skills_list:
                skill_lower = skill.lower()
                if any(cert in skill_lower for cert in ['cfa', 'frm', 'certification', 'certified', 'license']):
                    certifications.append(skill)
                elif any(analysis in skill_lower for analysis in ['analysis', 'modeling', 'valuation', 'research', 'risk']):
                    analytical.append(skill)
                elif any(soft in skill_lower for soft in ['excel', 'bloomberg', 'python', 'sql', 'tableau', 'sas']):
                    software.append(skill)
                elif any(market in skill_lower for market in ['equity', 'bond', 'derivatives', 'forex', 'commodities']):
                    markets.append(skill)
                else:
                    analytical.append(skill)
            
            # Create skills table
            skills_data = []
            
            if analytical:
                skills_data.append(['📊 Financial Analysis:', ' | '.join(analytical)])
            if software:
                skills_data.append(['💻 Technical Skills:', ' | '.join(software)])
            if markets:
                skills_data.append(['📈 Markets:', ' | '.join(markets)])
            if certifications:
                skills_data.append(['🏆 Certifications:', ' | '.join(certifications)])
            
            if skills_data:
                skills_table = Table(skills_data, colWidths=[4*cm, 13*cm])
                skills_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1565C0')),
                    ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#212121')),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ('TOPPADDING', (0, 0), (-1, -1), 3),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
                elements.append(skills_table)
        else:
            skills_para = Paragraph(f"💼 {str(skills_list)}", self.styles['Description'])
            elements.append(skills_para)
        
        return elements
