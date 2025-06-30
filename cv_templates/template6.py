"""
Elegant Modern CV Template
Clean, sophisticated design with excellent typography and layout balance
"""

import json
import logging
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

class TemplateGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.color_schemes = {
            'blue': {
                'primary': colors.HexColor('#1E3A8A'),
                'secondary': colors.HexColor('#3B82F6'),
                'accent': colors.HexColor('#60A5FA'),
                'text': colors.HexColor('#1F2937'),
                'light_bg': colors.HexColor('#F8FAFC')
            },
            'green': {
                'primary': colors.HexColor('#065F46'),
                'secondary': colors.HexColor('#059669'),
                'accent': colors.HexColor('#34D399'),
                'text': colors.HexColor('#1F2937'),
                'light_bg': colors.HexColor('#F0FDF4')
            },
            'red': {
                'primary': colors.HexColor('#991B1B'),
                'secondary': colors.HexColor('#DC2626'),
                'accent': colors.HexColor('#F87171'),
                'text': colors.HexColor('#1F2937'),
                'light_bg': colors.HexColor('#FEF2F2')
            },
            'purple': {
                'primary': colors.HexColor('#6B21A8'),
                'secondary': colors.HexColor('#9333EA'),
                'accent': colors.HexColor('#C084FC'),
                'text': colors.HexColor('#1F2937'),
                'light_bg': colors.HexColor('#FAF5FF')
            },
            'orange': {
                'primary': colors.HexColor('#C2410C'),
                'secondary': colors.HexColor('#EA580C'),
                'accent': colors.HexColor('#FB923C'),
                'text': colors.HexColor('#1F2937'),
                'light_bg': colors.HexColor('#FFF7ED')
            },
            'navy': {
                'primary': colors.HexColor('#1E293B'),
                'secondary': colors.HexColor('#334155'),
                'accent': colors.HexColor('#64748B'),
                'text': colors.HexColor('#1F2937'),
                'light_bg': colors.HexColor('#F8FAFC')
            }
        }
        
    def setup_custom_styles(self, color_scheme='blue'):
        """Setup elegant modern styles with dynamic colors"""
        self.colors = self.color_schemes.get(color_scheme, self.color_schemes['blue'])
        
        # Elegant name style
        self.styles.add(ParagraphStyle(
            name='ElegantName',
            parent=self.styles['Normal'],
            fontSize=36,
            fontName='Helvetica-Bold',
            textColor=self.colors['primary'],
            alignment=TA_CENTER,
            spaceAfter=6,
            spaceBefore=20
        ))
        
        # Professional title
        self.styles.add(ParagraphStyle(
            name='ProfessionalTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            fontName='Helvetica',
            textColor=self.colors['secondary'],
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        # Contact info in elegant format
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            textColor=self.colors['text'],
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        
        # Section headings with elegant underline
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Normal'],
            fontSize=18,
            fontName='Helvetica-Bold',
            textColor=self.colors['primary'],
            alignment=TA_LEFT,
            spaceBefore=25,
            spaceAfter=15,
            borderWidth=1,
            borderColor=self.colors['accent'],
            borderPadding=5
        ))
        
        # Professional summary style
        self.styles.add(ParagraphStyle(
            name='Summary',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName='Helvetica',
            textColor=self.colors['text'],
            alignment=TA_JUSTIFY,
            spaceAfter=20,
            leading=18,
            backColor=self.colors['light_bg'],
            borderPadding=15
        ))
        
        # Job title
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            fontName='Helvetica-Bold',
            textColor=self.colors['primary'],
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=4
        ))
        
        # Company/Organization
        self.styles.add(ParagraphStyle(
            name='Organization',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName='Helvetica',
            textColor=self.colors['secondary'],
            alignment=TA_LEFT,
            spaceAfter=4
        ))
        
        # Date range
        self.styles.add(ParagraphStyle(
            name='DateRange',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            textColor=colors.HexColor('#6B7280'),
            alignment=TA_LEFT,
            spaceAfter=8
        ))
        
        # Description text
        self.styles.add(ParagraphStyle(
            name='Description',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            textColor=self.colors['text'],
            alignment=TA_LEFT,
            spaceAfter=12,
            leading=16,
            leftIndent=20
        ))
        
        # Skills list
        self.styles.add(ParagraphStyle(
            name='SkillItem',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            textColor=self.colors['text'],
            alignment=TA_LEFT,
            spaceAfter=6,
            leftIndent=15
        ))

    def generate(self, cv_data, filepath, color_scheme='blue'):
        """Generate elegant modern CV"""
        try:
            self.setup_custom_styles(color_scheme)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=50,
                leftMargin=50,
                topMargin=40,
                bottomMargin=40
            )
            
            story = []
            
            # Header with photo and name
            header_content = self._create_elegant_header(cv_data)
            story.extend(header_content)
            
            # Professional summary
            if cv_data.get('summary'):
                story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeading']))
                story.append(Paragraph(cv_data['summary'], self.styles['Summary']))
            
            # Work experience
            if cv_data.get('experience'):
                story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['SectionHeading']))
                story.extend(self._create_experience_section(cv_data['experience']))
            
            # Education
            if cv_data.get('education'):
                story.append(Paragraph("EDUCATION", self.styles['SectionHeading']))
                story.extend(self._create_education_section(cv_data['education']))
            
            # Skills
            if cv_data.get('skills'):
                story.append(Paragraph("CORE COMPETENCIES", self.styles['SectionHeading']))
                story.extend(self._create_skills_section(cv_data['skills']))
            
            doc.build(story)
            logging.info(f"Elegant modern CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating elegant modern CV: {str(e)}")
            return False

    def _create_elegant_header(self, cv_data):
        """Create elegant header with optional photo"""
        content = []
        
        # Profile photo if available
        if cv_data.get('profile_photo') and os.path.exists(cv_data['profile_photo']):
            try:
                # Create a table to center the photo
                img = Image(cv_data['profile_photo'], width=100, height=100)
                photo_table = Table([[img]], colWidths=[100])
                photo_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                content.append(photo_table)
                content.append(Spacer(1, 15))
            except:
                pass
        
        # Name
        content.append(Paragraph(cv_data.get('full_name', 'Your Name'), self.styles['ElegantName']))
        
        # Professional title (placeholder for now)
        content.append(Paragraph("PROFESSIONAL CONSULTANT", self.styles['ProfessionalTitle']))
        
        # Contact information in a line
        contact_parts = []
        if cv_data.get('email'):
            contact_parts.append(f"✉ {cv_data['email']}")
        if cv_data.get('phone'):
            contact_parts.append(f"📞 {cv_data['phone']}")
        if cv_data.get('address'):
            contact_parts.append(f"📍 {cv_data['address']}")
        
        if contact_parts:
            contact_text = " • ".join(contact_parts)
            content.append(Paragraph(contact_text, self.styles['ContactInfo']))
        
        return content

    def _create_experience_section(self, experience_data):
        """Create professional experience section"""
        content = []
        
        try:
            exp_data = json.loads(experience_data) if isinstance(experience_data, str) else experience_data
            if isinstance(exp_data, list):
                for exp in exp_data:
                    exp_content = self._parse_experience_entry(exp)
                    content.extend(exp_content)
            else:
                content.append(Paragraph(str(exp_data), self.styles['Description']))
        except:
            content.append(Paragraph(str(experience_data), self.styles['Description']))
        
        return content

    def _parse_experience_entry(self, experience_text):
        """Parse and format experience entry"""
        content = []
        
        try:
            if isinstance(experience_text, dict):
                job_title = experience_text.get('title', 'Position')
                company = experience_text.get('company', 'Company')
                period = experience_text.get('period', 'Period')
                description = experience_text.get('description', '')
            else:
                lines = str(experience_text).strip().split('\n')
                job_title = lines[0] if len(lines) > 0 else 'Position'
                company = lines[1] if len(lines) > 1 else 'Company'
                period = lines[2] if len(lines) > 2 else 'Period'
                description = '\n'.join(lines[3:]) if len(lines) > 3 else ''
            
            content.append(Paragraph(job_title, self.styles['JobTitle']))
            content.append(Paragraph(company, self.styles['Organization']))
            content.append(Paragraph(period, self.styles['DateRange']))
            
            if description:
                # Split description into bullet points if it contains multiple lines
                if '\n' in description or '•' in description:
                    desc_lines = description.replace('•', '').split('\n')
                    for line in desc_lines:
                        if line.strip():
                            content.append(Paragraph(f"• {line.strip()}", self.styles['Description']))
                else:
                    content.append(Paragraph(description, self.styles['Description']))
            
            content.append(Spacer(1, 8))
            
        except Exception as e:
            content.append(Paragraph(str(experience_text), self.styles['Description']))
        
        return content

    def _create_education_section(self, education_data):
        """Create education section"""
        content = []
        
        try:
            edu_data = json.loads(education_data) if isinstance(education_data, str) else education_data
            if isinstance(edu_data, list):
                for edu in edu_data:
                    edu_content = self._parse_education_entry(edu)
                    content.extend(edu_content)
            else:
                content.append(Paragraph(str(edu_data), self.styles['Description']))
        except:
            content.append(Paragraph(str(education_data), self.styles['Description']))
        
        return content

    def _parse_education_entry(self, education_text):
        """Parse and format education entry"""
        content = []
        
        try:
            if isinstance(education_text, dict):
                degree = education_text.get('degree', 'Degree')
                institution = education_text.get('institution', 'Institution')
                period = education_text.get('period', 'Period')
                description = education_text.get('description', '')
            else:
                lines = str(education_text).strip().split('\n')
                degree = lines[0] if len(lines) > 0 else 'Degree'
                institution = lines[1] if len(lines) > 1 else 'Institution'
                period = lines[2] if len(lines) > 2 else 'Period'
                description = '\n'.join(lines[3:]) if len(lines) > 3 else ''
            
            content.append(Paragraph(degree, self.styles['JobTitle']))
            content.append(Paragraph(institution, self.styles['Organization']))
            content.append(Paragraph(period, self.styles['DateRange']))
            
            if description:
                content.append(Paragraph(description, self.styles['Description']))
            
            content.append(Spacer(1, 8))
            
        except Exception as e:
            content.append(Paragraph(str(education_text), self.styles['Description']))
        
        return content

    def _create_skills_section(self, skills_data):
        """Create skills section"""
        content = []
        
        try:
            skills_list = json.loads(skills_data) if isinstance(skills_data, str) else skills_data
            if isinstance(skills_list, list):
                # Create a nice grid of skills
                skill_chunks = [skills_list[i:i+3] for i in range(0, len(skills_list), 3)]
                for chunk in skill_chunks:
                    skill_row = " • ".join(chunk)
                    content.append(Paragraph(f"• {skill_row}", self.styles['SkillItem']))
            else:
                content.append(Paragraph(str(skills_data), self.styles['Description']))
        except:
            content.append(Paragraph(str(skills_data), self.styles['Description']))
        
        return content