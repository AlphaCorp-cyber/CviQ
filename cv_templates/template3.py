"""
Contemporary Modern CV Template
Clean, professional layout with blue accents and excellent readability
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
                'primary': colors.HexColor('#1F2937'),
                'accent': colors.HexColor('#3B82F6'),
                'secondary': colors.HexColor('#6B7280'),
                'light_blue': colors.HexColor('#EFF6FF'),
                'border': colors.HexColor('#E5E7EB')
            },
            'green': {
                'primary': colors.HexColor('#1F2937'),
                'accent': colors.HexColor('#10B981'),
                'secondary': colors.HexColor('#6B7280'),
                'light_blue': colors.HexColor('#ECFDF5'),
                'border': colors.HexColor('#E5E7EB')
            },
            'red': {
                'primary': colors.HexColor('#1F2937'),
                'accent': colors.HexColor('#EF4444'),
                'secondary': colors.HexColor('#6B7280'),
                'light_blue': colors.HexColor('#FEF2F2'),
                'border': colors.HexColor('#E5E7EB')
            },
            'purple': {
                'primary': colors.HexColor('#1F2937'),
                'accent': colors.HexColor('#8B5CF6'),
                'secondary': colors.HexColor('#6B7280'),
                'light_blue': colors.HexColor('#F5F3FF'),
                'border': colors.HexColor('#E5E7EB')
            },
            'orange': {
                'primary': colors.HexColor('#1F2937'),
                'accent': colors.HexColor('#F59E0B'),
                'secondary': colors.HexColor('#6B7280'),
                'light_blue': colors.HexColor('#FFFBEB'),
                'border': colors.HexColor('#E5E7EB')
            },
            'navy': {
                'primary': colors.HexColor('#1F2937'),
                'accent': colors.HexColor('#1E40AF'),
                'secondary': colors.HexColor('#6B7280'),
                'light_blue': colors.HexColor('#EFF6FF'),
                'border': colors.HexColor('#E5E7EB')
            }
        }
        
    def setup_custom_styles(self, color_scheme='blue'):
        """Setup contemporary styles with clean typography"""
        self.colors = self.color_schemes.get(color_scheme, self.color_schemes['blue'])
        
        # Contemporary name style
        self.styles.add(ParagraphStyle(
            name='ContemporaryName',
            parent=self.styles['Normal'],
            fontSize=32,
            fontName='Helvetica-Bold',
            textColor=self.colors['primary'],
            alignment=TA_CENTER,
            spaceAfter=5,
            spaceBefore=20
        ))
        
        # Job title
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=16,
            fontName='Helvetica',
            textColor=self.colors['accent'],
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        # Contact info bar
        self.styles.add(ParagraphStyle(
            name='ContactBar',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            textColor=self.colors['secondary'],
            alignment=TA_CENTER,
            spaceAfter=25,
            backColor=self.colors['light_blue'],
            borderPadding=8
        ))
        
        # Section headings with contemporary style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Normal'],
            fontSize=16,
            fontName='Helvetica-Bold',
            textColor=self.colors['accent'],
            alignment=TA_LEFT,
            spaceBefore=25,
            spaceAfter=15,
            leftIndent=0
        ))
        
        # Professional summary
        self.styles.add(ParagraphStyle(
            name='Summary',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            textColor=self.colors['primary'],
            alignment=TA_JUSTIFY,
            spaceAfter=15,
            leading=16
        ))
        
        # Position title
        self.styles.add(ParagraphStyle(
            name='PositionTitle',
            parent=self.styles['Normal'],
            fontSize=13,
            fontName='Helvetica-Bold',
            textColor=self.colors['primary'],
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=3
        ))
        
        # Company name
        self.styles.add(ParagraphStyle(
            name='CompanyName',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName='Helvetica',
            textColor=self.colors['accent'],
            alignment=TA_LEFT,
            spaceAfter=3
        ))
        
        # Date range
        self.styles.add(ParagraphStyle(
            name='DateRange',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            textColor=self.colors['secondary'],
            alignment=TA_LEFT,
            spaceAfter=6
        ))
        
        # Description text
        self.styles.add(ParagraphStyle(
            name='Description',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            textColor=self.colors['primary'],
            alignment=TA_LEFT,
            spaceAfter=8,
            leading=14,
            leftIndent=15
        ))
        
        # Skills with contemporary formatting
        self.styles.add(ParagraphStyle(
            name='SkillCategory',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Bold',
            textColor=self.colors['primary'],
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=4
        ))
        
        self.styles.add(ParagraphStyle(
            name='SkillList',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            textColor=self.colors['secondary'],
            alignment=TA_LEFT,
            spaceAfter=6,
            leftIndent=10
        ))

    def generate(self, cv_data, filepath, color_scheme='blue'):
        """Generate contemporary CV"""
        try:
            self.setup_custom_styles(color_scheme)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=50,
                leftMargin=50,
                topMargin=50,
                bottomMargin=50
            )
            
            story = []
            
            # Header section
            header_content = self._create_contemporary_header(cv_data)
            story.extend(header_content)
            
            # Professional summary
            if cv_data.get('summary'):
                story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeading']))
                story.append(Paragraph(cv_data['summary'], self.styles['Summary']))
            
            # Professional experience
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
            logging.info(f"Contemporary CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating contemporary CV: {str(e)}")
            return False

    def _create_contemporary_header(self, cv_data):
        """Create contemporary header with photo and contact info"""
        content = []
        
        # Profile photo if available (centered)
        if cv_data.get('profile_photo') and os.path.exists(cv_data['profile_photo']):
            try:
                img = Image(cv_data['profile_photo'], width=80, height=80)
                photo_table = Table([[img]], colWidths=[80])
                photo_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                content.append(photo_table)
                content.append(Spacer(1, 10))
            except:
                pass
        
        # Name
        content.append(Paragraph(cv_data.get('full_name', 'Your Name'), self.styles['ContemporaryName']))
        
        # Job title
        content.append(Paragraph("PROFESSIONAL CONSULTANT", self.styles['JobTitle']))
        
        # Contact information bar
        contact_parts = []
        if cv_data.get('email'):
            contact_parts.append(f"Email: {cv_data['email']}")
        if cv_data.get('phone'):
            contact_parts.append(f"Phone: {cv_data['phone']}")
        if cv_data.get('address'):
            contact_parts.append(f"Address: {cv_data['address']}")
        
        if contact_parts:
            contact_text = " | ".join(contact_parts)
            content.append(Paragraph(contact_text, self.styles['ContactBar']))
        
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
            
            content.append(Paragraph(job_title, self.styles['PositionTitle']))
            content.append(Paragraph(company, self.styles['CompanyName']))
            content.append(Paragraph(period, self.styles['DateRange']))
            
            if description:
                # Format as bullet points if multiple lines
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
            
            content.append(Paragraph(degree, self.styles['PositionTitle']))
            content.append(Paragraph(institution, self.styles['CompanyName']))
            content.append(Paragraph(period, self.styles['DateRange']))
            
            if description:
                content.append(Paragraph(description, self.styles['Description']))
            
            content.append(Spacer(1, 8))
            
        except Exception as e:
            content.append(Paragraph(str(education_text), self.styles['Description']))
        
        return content

    def _create_skills_section(self, skills_data):
        """Create contemporary skills section"""
        content = []
        
        try:
            skills_list = json.loads(skills_data) if isinstance(skills_data, str) else skills_data
            if isinstance(skills_list, list):
                # Group skills for better presentation
                for i, skill in enumerate(skills_list):
                    content.append(Paragraph(f"• {skill}", self.styles['SkillList']))
            else:
                content.append(Paragraph(str(skills_data), self.styles['Description']))
        except:
            content.append(Paragraph(str(skills_data), self.styles['Description']))
        
        return content