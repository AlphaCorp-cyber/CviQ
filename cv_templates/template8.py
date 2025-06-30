
"""
Professional Sales CV Template
Clean, modern design for sales professionals
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

class TemplateGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup professional sales-focused styles"""
        # Header name
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=28,
            spaceAfter=4,
            alignment=TA_LEFT,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        ))
        
        # Job title
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=16,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#666666'),
            fontName='Helvetica'
        ))
        
        # Contact info
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            textColor=colors.black,
            fontName='Helvetica'
        ))
        
        # Summary
        self.styles.add(ParagraphStyle(
            name='Summary',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=16,
            alignment=TA_JUSTIFY,
            textColor=colors.black,
            fontName='Helvetica'
        ))
        
        # Section headings with icons
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=12,
            textColor=colors.black,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#F5F5F5'),
            borderPadding=8
        ))
        
        # Job position
        self.styles.add(ParagraphStyle(
            name='JobPosition',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=12,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=colors.black
        ))
        
        # Company name
        self.styles.add(ParagraphStyle(
            name='CompanyName',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=2,
            fontName='Helvetica',
            textColor=colors.HexColor('#666666'),
            fontStyle='italic'
        ))
        
        # Date range
        self.styles.add(ParagraphStyle(
            name='DateRange',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            textColor=colors.HexColor('#666666'),
            fontName='Helvetica'
        ))
        
        # Bullet points
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=3,
            textColor=colors.black,
            fontName='Helvetica',
            bulletIndent=12,
            leftIndent=18
        ))
        
        # Key achievement
        self.styles.add(ParagraphStyle(
            name='KeyAchievement',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            textColor=colors.black,
            fontName='Helvetica-Bold',
            leftIndent=18
        ))
        
        # Education degree
        self.styles.add(ParagraphStyle(
            name='EducationDegree',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=8,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=colors.black
        ))
        
        # Education school
        self.styles.add(ParagraphStyle(
            name='EducationSchool',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=2,
            fontName='Helvetica',
            textColor=colors.HexColor('#666666'),
            fontStyle='italic'
        ))
        
        # Skill name
        self.styles.add(ParagraphStyle(
            name='SkillName',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            fontName='Helvetica',
            textColor=colors.black
        ))
    
    def generate(self, cv_data, filepath):
        """Generate professional sales CV"""
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
            
            # Professional summary
            if cv_data.get('summary'):
                story.extend(self._create_summary_section(cv_data['summary']))
            
            # Experience
            if cv_data.get('experience'):
                story.extend(self._create_experience_section(cv_data['experience']))
            
            # Education
            if cv_data.get('education'):
                story.extend(self._create_education_section(cv_data['education']))
            
            # Skills
            if cv_data.get('skills'):
                story.extend(self._create_skills_section(cv_data['skills']))
            
            # Languages (if available)
            languages = cv_data.get('languages', [])
            if languages:
                story.extend(self._create_languages_section(languages))
            
            doc.build(story)
            logging.info(f"Template8 CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating Template8 CV: {str(e)}")
            return False
    
    def _create_header(self, cv_data):
        """Create professional header"""
        elements = []
        
        # Name
        name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
        elements.append(name)
        
        # Job title (use a default if not provided)
        job_title = cv_data.get('job_title', 'Sales Representative')
        title = Paragraph(job_title, self.styles['JobTitle'])
        elements.append(title)
        
        # Create contact info in two columns
        contact_left = []
        contact_right = []
        
        if cv_data.get('phone'):
            contact_left.append(Paragraph(f"📞 {cv_data['phone']}", self.styles['ContactInfo']))
        if cv_data.get('email'):
            contact_left.append(Paragraph(f"✉ {cv_data['email']}", self.styles['ContactInfo']))
        
        if cv_data.get('website') or cv_data.get('linkedin'):
            linkedin = cv_data.get('linkedin', cv_data.get('website', ''))
            if linkedin:
                contact_right.append(Paragraph(f"🔗 {linkedin}", self.styles['ContactInfo']))
        
        if contact_left or contact_right:
            contact_data = [[contact_left, contact_right]]
            contact_table = Table(contact_data, colWidths=[85*mm, 85*mm])
            contact_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            elements.append(contact_table)
        
        elements.append(Spacer(1, 16))
        return elements
    
    def _create_summary_section(self, summary):
        """Create professional summary"""
        elements = []
        summary_para = Paragraph(summary, self.styles['Summary'])
        elements.append(summary_para)
        return elements
    
    def _create_experience_section(self, experience_list):
        """Create experience section"""
        elements = []
        heading = Paragraph("💼 Experience", self.styles['SectionHeading'])
        elements.append(heading)
        
        for exp in experience_list:
            exp_elements = self._parse_experience_entry(exp)
            elements.extend(exp_elements)
        
        return elements
    
    def _parse_experience_entry(self, experience_text):
        """Parse experience entry"""
        elements = []
        lines = [line.strip() for line in experience_text.split('\n') if line.strip()]
        
        if not lines:
            return elements
        
        # Parse first line for position and company
        first_line = lines[0]
        position = ""
        company = ""
        
        if ' at ' in first_line:
            parts = first_line.split(' at ', 1)
            position = parts[0].strip()
            company = parts[1].strip()
        else:
            position = first_line
        
        # Add position and company
        if position:
            elements.append(Paragraph(position, self.styles['JobPosition']))
        if company:
            elements.append(Paragraph(company, self.styles['CompanyName']))
        
        # Find and add date range
        date_line = None
        for i, line in enumerate(lines[1:], 1):
            if any(keyword in line.lower() for keyword in ['20', '19', 'present', 'current', '-']) and len(line) < 30:
                date_line = line
                elements.append(Paragraph(date_line, self.styles['DateRange']))
                break
        
        # Add bullet points and key achievements
        start_idx = 2 if date_line else 1
        key_achievement = None
        
        for line in lines[start_idx:]:
            if line and not any(keyword in line.lower() for keyword in ['20', '19', 'present', 'current']):
                # Check if this looks like a key achievement (contains numbers, percentages, etc.)
                if any(indicator in line for indicator in ['$', '%', 'million', 'thousand', 'increased', 'achieved', 'over']):
                    if not key_achievement:  # Only take the first key achievement
                        key_achievement = line
                        elements.append(Paragraph(f"Key Achievement", self.styles['KeyAchievement']))
                        elements.append(Paragraph(line, self.styles['Summary']))
                    else:
                        elements.append(Paragraph(f"• {line}", self.styles['BulletPoint']))
                else:
                    elements.append(Paragraph(f"• {line}", self.styles['BulletPoint']))
        
        elements.append(Spacer(1, 8))
        return elements
    
    def _create_education_section(self, education_list):
        """Create education section"""
        elements = []
        heading = Paragraph("🎓 Education", self.styles['SectionHeading'])
        elements.append(heading)
        
        for edu in education_list:
            edu_elements = self._parse_education_entry(edu)
            elements.extend(edu_elements)
        
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
        
        if degree:
            elements.append(Paragraph(degree, self.styles['EducationDegree']))
        if school:
            elements.append(Paragraph(school, self.styles['EducationSchool']))
        
        # Add year and additional details
        for line in lines[1:]:
            if any(keyword in line for keyword in ['20', '19']) and len(line) < 20:
                elements.append(Paragraph(line, self.styles['DateRange']))
            elif line and not any(keyword in line for keyword in ['20', '19']):
                elements.append(Paragraph(line, self.styles['Summary']))
        
        elements.append(Spacer(1, 8))
        return elements
    
    def _create_skills_section(self, skills_list):
        """Create skills section with rating bars"""
        elements = []
        heading = Paragraph("⚙ Skills", self.styles['SectionHeading'])
        elements.append(heading)
        
        if isinstance(skills_list, list):
            for skill in skills_list:
                # Create skill with rating visualization
                skill_table = self._create_skill_with_rating(skill)
                elements.append(skill_table)
                elements.append(Spacer(1, 6))
        else:
            skills_text = str(skills_list)
            for skill in skills_text.split(','):
                skill = skill.strip()
                if skill:
                    skill_table = self._create_skill_with_rating(skill)
                    elements.append(skill_table)
                    elements.append(Spacer(1, 6))
        
        return elements
    
    def _create_skill_with_rating(self, skill_name):
        """Create skill with rating bars"""
        # Create rating bars (4 out of 5 filled as default)
        filled_bar = "■"
        empty_bar = "□"
        rating = filled_bar * 4 + empty_bar * 1
        
        skill_data = [[
            Paragraph(skill_name, self.styles['SkillName']),
            Paragraph(rating, self.styles['SkillName'])
        ]]
        
        skill_table = Table(skill_data, colWidths=[120*mm, 40*mm])
        skill_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        
        return skill_table
    
    def _create_languages_section(self, languages_list):
        """Create languages section"""
        elements = []
        heading = Paragraph("🗣 Languages", self.styles['SectionHeading'])
        elements.append(heading)
        
        if isinstance(languages_list, list):
            for lang in languages_list:
                # Add proficiency level (default to intermediate)
                lang_table = self._create_language_with_level(lang)
                elements.append(lang_table)
                elements.append(Spacer(1, 6))
        else:
            lang_text = str(languages_list)
            for lang in lang_text.split(','):
                lang = lang.strip()
                if lang:
                    lang_table = self._create_language_with_level(lang)
                    elements.append(lang_table)
                    elements.append(Spacer(1, 6))
        
        return elements
    
    def _create_language_with_level(self, language):
        """Create language with proficiency level"""
        # Default proficiency visualization
        filled_bar = "■"
        empty_bar = "□"
        proficiency = filled_bar * 4 + empty_bar * 1
        level_text = "C1 Certified" if "spanish" in language.lower() else "Fluent"
        
        lang_data = [[
            Paragraph(language, self.styles['SkillName']),
            Paragraph(proficiency, self.styles['SkillName'])
        ]]
        
        lang_table = Table(lang_data, colWidths=[120*mm, 40*mm])
        lang_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        
        # Add level text below
        level_para = Paragraph(level_text, self.styles['ContactInfo'])
        
        return lang_table
