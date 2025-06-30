"""
Modern Two-Column Professional CV Template
Dark sidebar with clean white main content area - inspired by contemporary designs
"""

import json
import logging
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Image, Flowable
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
                'text_dark': colors.HexColor('#2C3E50')
            },
            'green': {
                'sidebar': colors.HexColor('#27AE60'),
                'accent': colors.HexColor('#2ECC71'),
                'text_light': colors.white,
                'text_dark': colors.HexColor('#27AE60')
            },
            'red': {
                'sidebar': colors.HexColor('#C0392B'),
                'accent': colors.HexColor('#E74C3C'),
                'text_light': colors.white,
                'text_dark': colors.HexColor('#C0392B')
            },
            'purple': {
                'sidebar': colors.HexColor('#7D3C98'),
                'accent': colors.HexColor('#9B59B6'),
                'text_light': colors.white,
                'text_dark': colors.HexColor('#7D3C98')
            },
            'orange': {
                'sidebar': colors.HexColor('#D35400'),
                'accent': colors.HexColor('#E67E22'),
                'text_light': colors.white,
                'text_dark': colors.HexColor('#D35400')
            },
            'navy': {
                'sidebar': colors.HexColor('#2C3E50'),
                'accent': colors.HexColor('#34495E'),
                'text_light': colors.white,
                'text_dark': colors.HexColor('#2C3E50')
            }
        }
        
    def setup_custom_styles(self, color_scheme='blue'):
        """Setup modern two-column styles with dynamic colors"""
        self.colors = self.color_schemes.get(color_scheme, self.color_schemes['blue'])
        
        # Sidebar styles - light text on dark background
        self.styles.add(ParagraphStyle(
            name='SidebarName',
            parent=self.styles['Normal'],
            fontSize=28,
            fontName='Helvetica-Bold',
            textColor=self.colors['text_light'],
            alignment=TA_LEFT,
            spaceAfter=0
        ))
        
        self.styles.add(ParagraphStyle(
            name='SidebarTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            fontName='Helvetica',
            textColor=self.colors['text_light'],
            alignment=TA_LEFT,
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
            spaceAfter=8,
            leading=14
        ))
        
        self.styles.add(ParagraphStyle(
            name='SidebarContact',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            textColor=self.colors['text_light'],
            alignment=TA_LEFT,
            spaceAfter=6
        ))
        
        # Main content styles - dark text on white background
        self.styles.add(ParagraphStyle(
            name='MainName',
            parent=self.styles['Normal'],
            fontSize=36,
            fontName='Helvetica-Bold',
            textColor=self.colors['text_dark'],
            alignment=TA_LEFT,
            spaceAfter=0,
            spaceBefore=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Normal'],
            fontSize=16,
            fontName='Helvetica',
            textColor=colors.HexColor('#666666'),
            alignment=TA_LEFT,
            spaceAfter=25
        ))
        
        self.styles.add(ParagraphStyle(
            name='MainHeading',
            parent=self.styles['Normal'],
            fontSize=16,
            fontName='Helvetica-Bold',
            textColor=self.colors['text_dark'],
            alignment=TA_LEFT,
            spaceBefore=20,
            spaceAfter=10,
            borderWidth=0,
            borderColor=self.colors['accent'],
            borderPadding=0
        ))
        
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            fontName='Helvetica-Bold',
            textColor=self.colors['text_dark'],
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=2
        ))
        
        self.styles.add(ParagraphStyle(
            name='Organization',
            parent=self.styles['Normal'],
            fontSize=12,
            fontName='Helvetica',
            textColor=colors.HexColor('#666666'),
            alignment=TA_LEFT,
            spaceAfter=2
        ))
        
        self.styles.add(ParagraphStyle(
            name='DateStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            textColor=colors.HexColor('#888888'),
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
            leading=15
        ))

    def generate(self, cv_data, filepath, color_scheme='blue'):
        """Generate modern two-column CV"""
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
            
            # Create two-column layout using a table
            story = []
            
            # Get page dimensions
            page_width = A4[0]
            page_height = A4[1]
            sidebar_width = page_width * 0.35  # 35% for sidebar
            main_width = page_width * 0.65    # 65% for main content
            
            # Create sidebar content
            sidebar_content = self._create_sidebar_content(cv_data)
            
            # Create main content
            main_content = self._create_main_content(cv_data)
            
            # Create the two-column table
            table_data = [[sidebar_content, main_content]]
            
            table = Table(table_data, colWidths=[sidebar_width, main_width])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), self.colors['sidebar']),
                ('BACKGROUND', (1, 0), (1, 0), colors.white),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (0, 0), 25),
                ('RIGHTPADDING', (0, 0), (0, 0), 15),
                ('LEFTPADDING', (1, 0), (1, 0), 25),
                ('RIGHTPADDING', (1, 0), (1, 0), 25),
                ('TOPPADDING', (0, 0), (-1, -1), 30),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 30),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [self.colors['sidebar'], colors.white])
            ]))
            
            story.append(table)
            doc.build(story)
            
            logging.info(f"Modern two-column CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating modern two-column CV: {str(e)}")
            return False

    def _create_sidebar_content(self, cv_data):
        """Create sidebar with photo, contact info, skills, etc."""
        content = []
        
        # Profile photo if available
        if cv_data.get('profile_photo') and os.path.exists(cv_data['profile_photo']):
            try:
                img = Image(cv_data['profile_photo'], width=120, height=120)
                content.append(img)
                content.append(Spacer(1, 20))
            except:
                pass
        
        # About Me section
        content.append(Paragraph("ABOUT ME", self.styles['SidebarHeading']))
        if cv_data.get('summary'):
            content.append(Paragraph(cv_data['summary'], self.styles['SidebarText']))
        
        # Contact information
        contact_info = []
        if cv_data.get('phone'):
            contact_info.append(f"📞 {cv_data['phone']}")
        if cv_data.get('email'):
            contact_info.append(f"✉ {cv_data['email']}")
        if cv_data.get('address'):
            contact_info.append(f"📍 {cv_data['address']}")
        
        if contact_info:
            content.append(Spacer(1, 10))
            for info in contact_info:
                content.append(Paragraph(info, self.styles['SidebarContact']))
        
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
        
        # Languages (placeholder)
        content.append(Paragraph("LANGUAGES", self.styles['SidebarHeading']))
        content.append(Paragraph("• English", self.styles['SidebarText']))
        content.append(Paragraph("• French", self.styles['SidebarText']))
        
        # Hobbies (placeholder)
        content.append(Paragraph("HOBBIES", self.styles['SidebarHeading']))
        content.append(Paragraph("• Problem Solving", self.styles['SidebarText']))
        content.append(Paragraph("• Technology", self.styles['SidebarText']))
        content.append(Paragraph("• Innovation", self.styles['SidebarText']))
        
        return content

    def _create_main_content(self, cv_data):
        """Create main content area with name, experience, education"""
        content = []
        
        # Name and title
        content.append(Paragraph(cv_data.get('full_name', 'Your Name'), self.styles['MainName']))
        content.append(Paragraph("PROFESSIONAL TITLE", self.styles['MainTitle']))
        
        # Work Experience
        content.append(Paragraph("WORK EXPERIENCE", self.styles['MainHeading']))
        if cv_data.get('experience'):
            try:
                exp_data = json.loads(cv_data['experience']) if isinstance(cv_data['experience'], str) else cv_data['experience']
                if isinstance(exp_data, list):
                    for exp in exp_data:
                        exp_entry = self._parse_experience_entry(exp)
                        content.extend(exp_entry)
                else:
                    content.append(Paragraph(str(exp_data), self.styles['Description']))
            except:
                content.append(Paragraph(str(cv_data['experience']), self.styles['Description']))
        
        # Education
        content.append(Paragraph("EDUCATION", self.styles['MainHeading']))
        if cv_data.get('education'):
            try:
                edu_data = json.loads(cv_data['education']) if isinstance(cv_data['education'], str) else cv_data['education']
                if isinstance(edu_data, list):
                    for edu in edu_data:
                        edu_entry = self._parse_education_entry(edu)
                        content.extend(edu_entry)
                else:
                    content.append(Paragraph(str(edu_data), self.styles['Description']))
            except:
                content.append(Paragraph(str(cv_data['education']), self.styles['Description']))
        
        return content

    def _parse_experience_entry(self, experience_text):
        """Parse experience entry"""
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
            content.append(Paragraph(period, self.styles['DateStyle']))
            if description:
                content.append(Paragraph(description, self.styles['Description']))
            content.append(Spacer(1, 8))
            
        except Exception as e:
            content.append(Paragraph(str(experience_text), self.styles['Description']))
            
        return content

    def _parse_education_entry(self, education_text):
        """Parse education entry"""
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
            content.append(Paragraph(period, self.styles['DateStyle']))
            if description:
                content.append(Paragraph(description, self.styles['Description']))
            content.append(Spacer(1, 8))
            
        except Exception as e:
            content.append(Paragraph(str(education_text), self.styles['Description']))
            
        return content