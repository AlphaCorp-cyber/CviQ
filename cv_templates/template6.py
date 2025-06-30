"""
Modern Sidebar CV Template
Dark sidebar with contact info and skills, white main area with experience and education
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
                'sidebar': colors.HexColor('#2C3E50'),
                'accent': colors.HexColor('#3498DB'),
                'text_light': colors.white,
                'text_dark': colors.HexColor('#2C3E50'),
                'main_bg': colors.white
            },
            'green': {
                'sidebar': colors.HexColor('#27AE60'),
                'accent': colors.HexColor('#2ECC71'),
                'text_light': colors.white,
                'text_dark': colors.HexColor('#27AE60'),
                'main_bg': colors.white
            },
            'red': {
                'sidebar': colors.HexColor('#C0392B'),
                'accent': colors.HexColor('#E74C3C'),
                'text_light': colors.white,
                'text_dark': colors.HexColor('#C0392B'),
                'main_bg': colors.white
            },
            'purple': {
                'sidebar': colors.HexColor('#7D3C98'),
                'accent': colors.HexColor('#9B59B6'),
                'text_light': colors.white,
                'text_dark': colors.HexColor('#7D3C98'),
                'main_bg': colors.white
            },
            'orange': {
                'sidebar': colors.HexColor('#D35400'),
                'accent': colors.HexColor('#E67E22'),
                'text_light': colors.white,
                'text_dark': colors.HexColor('#D35400'),
                'main_bg': colors.white
            },
            'navy': {
                'sidebar': colors.HexColor('#2C3E50'),
                'accent': colors.HexColor('#34495E'),
                'text_light': colors.white,
                'text_dark': colors.HexColor('#2C3E50'),
                'main_bg': colors.white
            }
        }
        
    def setup_custom_styles(self, color_scheme='blue'):
        """Setup sidebar CV styles with dynamic colors"""
        self.colors = self.color_schemes.get(color_scheme, self.color_schemes['blue'])
        
        # Sidebar styles (white text on dark background)
        self.styles.add(ParagraphStyle(
            name='SidebarName',
            parent=self.styles['Normal'],
            fontSize=24,
            fontName='Helvetica-Bold',
            textColor=self.colors['text_light'],
            alignment=TA_CENTER,
            spaceAfter=5,
            spaceBefore=15
        ))
        
        self.styles.add(ParagraphStyle(
            name='SidebarTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName='Helvetica',
            textColor=self.colors['text_light'],
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='SidebarHeading',
            parent=self.styles['Normal'],
            fontSize=14,
            fontName='Helvetica-Bold',
            textColor=self.colors['text_light'],
            alignment=TA_LEFT,
            spaceBefore=15,
            spaceAfter=8
        ))
        
        self.styles.add(ParagraphStyle(
            name='SidebarText',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            textColor=self.colors['text_light'],
            alignment=TA_LEFT,
            spaceAfter=6,
            leading=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='SidebarContact',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            textColor=self.colors['text_light'],
            alignment=TA_LEFT,
            spaceAfter=4
        ))
        
        # Main area styles (dark text on white background)
        self.styles.add(ParagraphStyle(
            name='MainHeading',
            parent=self.styles['Normal'],
            fontSize=18,
            fontName='Helvetica-Bold',
            textColor=self.colors['text_dark'],
            alignment=TA_LEFT,
            spaceBefore=25,
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            fontName='Helvetica-Bold',
            textColor=self.colors['text_dark'],
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=3
        ))
        
        self.styles.add(ParagraphStyle(
            name='Organization',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName='Helvetica',
            textColor=self.colors['accent'],
            alignment=TA_LEFT,
            spaceAfter=3
        ))
        
        self.styles.add(ParagraphStyle(
            name='DateRange',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            textColor=colors.HexColor('#666666'),
            alignment=TA_LEFT,
            spaceAfter=6
        ))
        
        self.styles.add(ParagraphStyle(
            name='Description',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            textColor=colors.HexColor('#333333'),
            alignment=TA_LEFT,
            spaceAfter=8,
            leading=14,
            leftIndent=15
        ))

    def generate(self, cv_data, filepath, color_scheme='blue'):
        """Generate sidebar CV with dark left sidebar and white right main area"""
        try:
            self.setup_custom_styles(color_scheme)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=0,
                leftMargin=0,
                topMargin=0,
                bottomMargin=0
            )
            
            story = []
            
            # Get page dimensions
            page_width = A4[0]
            sidebar_width = page_width * 0.35  # 35% for sidebar
            main_width = page_width * 0.65    # 65% for main content
            
            # Create sidebar content (dark background)
            sidebar_content = self._create_sidebar_content(cv_data)
            
            # Create main content (white background)
            main_content = self._create_main_content(cv_data)
            
            # Create the two-column table
            table_data = [[sidebar_content, main_content]]
            
            table = Table(table_data, colWidths=[sidebar_width, main_width])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), self.colors['sidebar']),  # Dark sidebar
                ('BACKGROUND', (1, 0), (1, 0), self.colors['main_bg']),  # White main
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (0, 0), 20),  # Sidebar padding
                ('RIGHTPADDING', (0, 0), (0, 0), 15),
                ('LEFTPADDING', (1, 0), (1, 0), 25),  # Main area padding
                ('RIGHTPADDING', (1, 0), (1, 0), 25),
                ('TOPPADDING', (0, 0), (-1, -1), 25),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 25),
            ]))
            
            story.append(table)
            doc.build(story)
            
            logging.info(f"Sidebar CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating sidebar CV: {str(e)}")
            return False

    def _create_sidebar_content(self, cv_data):
        """Create dark sidebar with photo, contact info, skills"""
        content = []
        
        # Profile photo if available
        if cv_data.get('profile_photo') and os.path.exists(cv_data['profile_photo']):
            try:
                img = Image(cv_data['profile_photo'], width=100, height=100)
                content.append(img)
                content.append(Spacer(1, 15))
            except:
                pass
        
        # Name and title in sidebar
        content.append(Paragraph(cv_data.get('full_name', 'Your Name'), self.styles['SidebarName']))
        content.append(Paragraph("PROFESSIONAL", self.styles['SidebarTitle']))
        
        # Contact information
        content.append(Paragraph("CONTACT", self.styles['SidebarHeading']))
        if cv_data.get('phone'):
            content.append(Paragraph(f"📞 {cv_data['phone']}", self.styles['SidebarContact']))
        if cv_data.get('email'):
            content.append(Paragraph(f"✉ {cv_data['email']}", self.styles['SidebarContact']))
        if cv_data.get('address'):
            content.append(Paragraph(f"📍 {cv_data['address']}", self.styles['SidebarContact']))
        
        # About/Summary section
        if cv_data.get('summary'):
            content.append(Paragraph("ABOUT", self.styles['SidebarHeading']))
            content.append(Paragraph(cv_data['summary'], self.styles['SidebarText']))
        
        # Skills section
        if cv_data.get('skills'):
            content.append(Paragraph("SKILLS", self.styles['SidebarHeading']))
            try:
                skills_data = json.loads(cv_data['skills']) if isinstance(cv_data['skills'], str) else cv_data['skills']
                if isinstance(skills_data, list):
                    for skill in skills_data:
                        content.append(Paragraph(f"• {skill}", self.styles['SidebarText']))
                else:
                    content.append(Paragraph(str(skills_data), self.styles['SidebarText']))
            except:
                content.append(Paragraph(str(cv_data['skills']), self.styles['SidebarText']))
        
        # Languages section
        content.append(Paragraph("LANGUAGES", self.styles['SidebarHeading']))
        content.append(Paragraph("• English", self.styles['SidebarText']))
        content.append(Paragraph("• French", self.styles['SidebarText']))
        
        return content

    def _create_main_content(self, cv_data):
        """Create white main content area with experience and education"""
        content = []
        
        # Add some top spacing
        content.append(Spacer(1, 20))
        
        # Work Experience
        if cv_data.get('experience'):
            content.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['MainHeading']))
            content.extend(self._create_experience_section(cv_data['experience']))
        
        # Education
        if cv_data.get('education'):
            content.append(Paragraph("EDUCATION", self.styles['MainHeading']))
            content.extend(self._create_education_section(cv_data['education']))
        
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