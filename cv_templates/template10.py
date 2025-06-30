
"""
Professional Two-Column CV Template
Clean modern design with sidebar and timeline layout
"""

import json
import logging
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import Drawing, Circle, Line

class TimelineFlowable(Flowable):
    """Custom flowable for timeline elements"""
    def __init__(self, width=10, height=10, color=colors.HexColor('#34495E')):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.circle(self.width/2, self.height/2, 3, fill=1)

class TemplateGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.color_schemes = {
            'blue': {
                'primary': colors.HexColor('#34495E'),
                'secondary': colors.HexColor('#2C3E50'),
                'accent': colors.HexColor('#3498DB'),
                'light': colors.HexColor('#ECF0F1'),
                'sidebar': colors.HexColor('#F8F9FA')
            },
            'green': {
                'primary': colors.HexColor('#27AE60'),
                'secondary': colors.HexColor('#2E7D32'),
                'accent': colors.HexColor('#4CAF50'),
                'light': colors.HexColor('#E8F5E8'),
                'sidebar': colors.HexColor('#F1F8E9')
            },
            'purple': {
                'primary': colors.HexColor('#8E44AD'),
                'secondary': colors.HexColor('#7B1FA2'),
                'accent': colors.HexColor('#9C27B0'),
                'light': colors.HexColor('#F3E5F5'),
                'sidebar': colors.HexColor('#F8F5FA')
            },
            'red': {
                'primary': colors.HexColor('#E74C3C'),
                'secondary': colors.HexColor('#C62828'),
                'accent': colors.HexColor('#F44336'),
                'light': colors.HexColor('#FFEBEE'),
                'sidebar': colors.HexColor('#FCF8F8')
            },
            'orange': {
                'primary': colors.HexColor('#E67E22'),
                'secondary': colors.HexColor('#D84315'),
                'accent': colors.HexColor('#FF5722'),
                'light': colors.HexColor('#FFF3E0'),
                'sidebar': colors.HexColor('#FDF7F0')
            },
            'navy': {
                'primary': colors.HexColor('#2C3E50'),
                'secondary': colors.HexColor('#1A252F'),
                'accent': colors.HexColor('#34495E'),
                'light': colors.HexColor('#EAEDED'),
                'sidebar': colors.HexColor('#F4F6F6')
            }
        }
        self.current_colors = self.color_schemes['blue']  # Default
        self.setup_custom_styles()
        
    def set_color_scheme(self, scheme_name):
        """Set color scheme for the template"""
        if scheme_name in self.color_schemes:
            self.current_colors = self.color_schemes[scheme_name]
            self.setup_custom_styles()  # Refresh styles with new colors
        
    def setup_custom_styles(self):
        """Setup professional two-column styles"""
        # Header name style
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=32,
            spaceAfter=2,
            alignment=TA_LEFT,
            textColor=self.current_colors['primary'],
            fontName='Helvetica-Bold',
            leftIndent=0
        ))
        
        # Job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=10,
            alignment=TA_LEFT,
            textColor=self.current_colors['secondary'],
            fontName='Helvetica',
            leftIndent=0
        ))
        
        # Sidebar section headings
        self.styles.add(ParagraphStyle(
            name='SidebarHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceBefore=15,
            spaceAfter=8,
            textColor=self.current_colors['primary'],
            fontName='Helvetica-Bold',
            alignment=TA_LEFT,
            textTransform='uppercase'
        ))
        
        # Main section headings
        self.styles.add(ParagraphStyle(
            name='MainHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=10,
            textColor=self.current_colors['primary'],
            fontName='Helvetica-Bold',
            alignment=TA_LEFT,
            textTransform='uppercase'
        ))
        
        # Contact info in sidebar
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=6,
            textColor=colors.HexColor('#2C3E50'),
            fontName='Helvetica',
            leftIndent=15
        ))
        
        # Skills list
        self.styles.add(ParagraphStyle(
            name='SkillItem',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=4,
            textColor=colors.HexColor('#2C3E50'),
            fontName='Helvetica',
            bulletIndent=5,
            leftIndent=15
        ))
        
        # Experience company/position
        self.styles.add(ParagraphStyle(
            name='CompanyName',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=8,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=self.current_colors['primary']
        ))
        
        # Position title
        self.styles.add(ParagraphStyle(
            name='PositionTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=3,
            fontName='Helvetica',
            textColor=self.current_colors['secondary']
        ))
        
        # Date range
        self.styles.add(ParagraphStyle(
            name='DateRange',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName='Helvetica',
            textColor=colors.HexColor('#7F8C8D'),
            alignment=TA_RIGHT
        ))
        
        # Description bullets
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=3,
            textColor=colors.HexColor('#2C3E50'),
            fontName='Helvetica',
            bulletIndent=8,
            leftIndent=15
        ))
        
        # Education
        self.styles.add(ParagraphStyle(
            name='EducationDegree',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=8,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=self.current_colors['primary']
        ))
        
        self.styles.add(ParagraphStyle(
            name='EducationSchool',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            fontName='Helvetica',
            textColor=self.current_colors['secondary']
        ))
    
    def generate(self, cv_data, filepath, color_scheme='blue'):
        """Generate two-column CV"""
        try:
            # Set color scheme
            self.set_color_scheme(color_scheme)
            
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=15*mm,
                leftMargin=15*mm,
                topMargin=20*mm,
                bottomMargin=20*mm
            )
            
            story = []
            
            # Create main layout table
            main_content = self._create_main_content(cv_data)
            sidebar_content = self._create_sidebar_content(cv_data)
            
            # Create two-column layout
            layout_data = [[sidebar_content, main_content]]
            layout_table = Table(layout_data, colWidths=[65*mm, 115*mm])
            layout_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('BACKGROUND', (0, 0), (0, -1), self.current_colors['sidebar']),
                ('LINEAFTER', (0, 0), (0, -1), 1, colors.HexColor('#BDC3C7')),
            ]))
            
            story.append(layout_table)
            doc.build(story)
            logging.info(f"Template10 CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating Template10 CV: {str(e)}")
            return False
    
    def _create_sidebar_content(self, cv_data):
        """Create sidebar with contact, skills, languages, references"""
        elements = []
        
        # Profile photo if available
        profile_photo_path = cv_data.get('profile_photo')
        if profile_photo_path and os.path.exists(profile_photo_path):
            try:
                from reportlab.platypus import Image
                img = Image(profile_photo_path, width=50*mm, height=50*mm)
                img.hAlign = 'CENTER'
                elements.append(Spacer(1, 10))
                elements.append(img)
                elements.append(Spacer(1, 15))
            except Exception as e:
                logging.error(f"Error adding photo to sidebar: {str(e)}")
        
        # Contact section
        elements.append(Paragraph("CONTACT", self.styles['SidebarHeading']))
        elements.append(HRFlowable(width=50*mm, thickness=1, color=self.current_colors['accent']))
        
        if cv_data.get('phone'):
            elements.append(Paragraph(f"📞 {cv_data['phone']}", self.styles['ContactInfo']))
        if cv_data.get('email'):
            elements.append(Paragraph(f"✉ {cv_data['email']}", self.styles['ContactInfo']))
        if cv_data.get('address'):
            elements.append(Paragraph(f"📍 {cv_data['address']}", self.styles['ContactInfo']))
        if cv_data.get('website'):
            elements.append(Paragraph(f"🌐 {cv_data['website']}", self.styles['ContactInfo']))
        
        # Skills section
        if cv_data.get('skills'):
            elements.append(Paragraph("SKILLS", self.styles['SidebarHeading']))
            elements.append(HRFlowable(width=50*mm, thickness=1, color=self.current_colors['accent']))
            
            if isinstance(cv_data['skills'], list):
                for skill in cv_data['skills'][:8]:  # Limit to 8 skills
                    elements.append(Paragraph(f"• {skill}", self.styles['SkillItem']))
            else:
                skills_text = str(cv_data['skills'])
                for skill in skills_text.split(',')[:8]:
                    elements.append(Paragraph(f"• {skill.strip()}", self.styles['SkillItem']))
        
        # Languages section (if available in CV data)
        languages = cv_data.get('languages', [])
        if languages:
            elements.append(Paragraph("LANGUAGES", self.styles['SidebarHeading']))
            elements.append(HRFlowable(width=50*mm, thickness=1, color=self.current_colors['accent']))
            
            if isinstance(languages, list):
                for lang in languages:
                    elements.append(Paragraph(f"• {lang}", self.styles['SkillItem']))
            else:
                elements.append(Paragraph(f"• {str(languages)}", self.styles['SkillItem']))
        
        # Reference section (placeholder)
        elements.append(Paragraph("REFERENCE", self.styles['SidebarHeading']))
        elements.append(HRFlowable(width=50*mm, thickness=1, color=self.current_colors['accent']))
        elements.append(Paragraph("Available upon request", self.styles['ContactInfo']))
        
        return elements
    
    def _create_main_content(self, cv_data):
        """Create main content area with header, profile, experience, education"""
        elements = []
        
        # Header
        elements.append(Paragraph(cv_data.get('full_name', '').upper(), self.styles['HeaderName']))
        elements.append(Paragraph("MARKETING MANAGER", self.styles['JobTitle']))  # Can be dynamic
        elements.append(HRFlowable(width=115*mm, thickness=2, color=self.current_colors['primary']))
        elements.append(Spacer(1, 15))
        
        # Profile section
        if cv_data.get('summary'):
            elements.append(Paragraph("👤 PROFILE", self.styles['MainHeading']))
            elements.append(HRFlowable(width=115*mm, thickness=1, color=self.current_colors['accent']))
            elements.append(Spacer(1, 5))
            elements.append(Paragraph(cv_data['summary'], self.styles['BulletPoint']))
            elements.append(Spacer(1, 15))
        
        # Work Experience
        if cv_data.get('experience'):
            elements.append(Paragraph("💼 WORK EXPERIENCE", self.styles['MainHeading']))
            elements.append(HRFlowable(width=115*mm, thickness=1, color=self.current_colors['accent']))
            elements.append(Spacer(1, 5))
            
            for exp in cv_data['experience']:
                exp_elements = self._parse_experience_entry(exp)
                elements.extend(exp_elements)
        
        # Education
        if cv_data.get('education'):
            elements.append(Paragraph("🎓 EDUCATION", self.styles['MainHeading']))
            elements.append(HRFlowable(width=115*mm, thickness=1, color=self.current_colors['accent']))
            elements.append(Spacer(1, 5))
            
            for edu in cv_data['education']:
                edu_elements = self._parse_education_entry(edu)
                elements.extend(edu_elements)
        
        return elements
    
    def _parse_experience_entry(self, experience_text):
        """Parse experience entry with timeline design"""
        elements = []
        lines = [line.strip() for line in experience_text.split('\n') if line.strip()]
        
        if not lines:
            return elements
        
        # Parse first line for company and position
        first_line = lines[0]
        company = ""
        position = ""
        
        if ' at ' in first_line:
            parts = first_line.split(' at ', 1)
            position = parts[0].strip()
            company = parts[1].strip()
        elif ' - ' in first_line:
            parts = first_line.split(' - ', 1)
            company = parts[0].strip()
            position = parts[1].strip()
        else:
            company = first_line
        
        # Create timeline entry with circle and content
        timeline_data = []
        
        # Timeline circle and company info
        circle_cell = [TimelineFlowable(color=self.current_colors['accent'])]
        
        content_cell = []
        if company:
            content_cell.append(Paragraph(company, self.styles['CompanyName']))
        if position:
            content_cell.append(Paragraph(position, self.styles['PositionTitle']))
        
        # Find date in subsequent lines
        date_found = False
        for i, line in enumerate(lines[1:], 1):
            if any(keyword in line.lower() for keyword in ['20', '19', 'present', 'current', '-']) and len(line) < 30:
                content_cell.append(Paragraph(line, self.styles['DateRange']))
                date_found = True
                break
        
        timeline_data.append([circle_cell, content_cell])
        
        timeline_table = Table(timeline_data, colWidths=[10*mm, 105*mm])
        timeline_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        elements.append(timeline_table)
        
        # Add bullet points for responsibilities
        start_idx = 2 if date_found else 1
        for line in lines[start_idx:]:
            if line and not any(keyword in line.lower() for keyword in ['20', '19', 'present', 'current']):
                elements.append(Paragraph(f"• {line}", self.styles['BulletPoint']))
        
        elements.append(Spacer(1, 10))
        return elements
    
    def _parse_education_entry(self, education_text):
        """Parse education entry"""
        elements = []
        lines = [line.strip() for line in education_text.split('\n') if line.strip()]
        
        if not lines:
            return elements
        
        first_line = lines[0]
        degree = ""
        school = ""
        
        if ' at ' in first_line or ' from ' in first_line:
            parts = first_line.split(' at ' if ' at ' in first_line else ' from ', 1)
            degree = parts[0].strip()
            school = parts[1].strip()
        else:
            degree = first_line
        
        # Create timeline entry for education
        timeline_data = []
        circle_cell = [TimelineFlowable(color=self.current_colors['accent'])]
        
        content_cell = []
        if degree:
            content_cell.append(Paragraph(degree, self.styles['EducationDegree']))
        if school:
            content_cell.append(Paragraph(school, self.styles['EducationSchool']))
        
        # Find date
        for line in lines[1:]:
            if any(keyword in line for keyword in ['20', '19']) and len(line) < 20:
                content_cell.append(Paragraph(line, self.styles['DateRange']))
                break
        
        timeline_data.append([circle_cell, content_cell])
        
        timeline_table = Table(timeline_data, colWidths=[10*mm, 105*mm])
        timeline_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(timeline_table)
        return elements
