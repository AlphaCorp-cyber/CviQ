
"""
Technical Professional CV Template
Designed for IT and technical professionals
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
                'primary': colors.HexColor('#2E86C1'),
                'secondary': colors.HexColor('#1F618D'),
                'accent': colors.HexColor('#5DADE2'),
                'background': colors.HexColor('#EBF5FB')
            },
            'green': {
                'primary': colors.HexColor('#28B463'),
                'secondary': colors.HexColor('#1E8449'),
                'accent': colors.HexColor('#58D68D'),
                'background': colors.HexColor('#E8F8F5')
            },
            'red': {
                'primary': colors.HexColor('#E74C3C'),
                'secondary': colors.HexColor('#C0392B'),
                'accent': colors.HexColor('#F1948A'),
                'background': colors.HexColor('#FDEDEC')
            },
            'purple': {
                'primary': colors.HexColor('#8E44AD'),
                'secondary': colors.HexColor('#7D3C98'),
                'accent': colors.HexColor('#BB8FCE'),
                'background': colors.HexColor('#F4ECF7')
            },
            'orange': {
                'primary': colors.HexColor('#E67E22'),
                'secondary': colors.HexColor('#D35400'),
                'accent': colors.HexColor('#F39C12'),
                'background': colors.HexColor('#FEF9E7')
            },
            'navy': {
                'primary': colors.HexColor('#34495E'),
                'secondary': colors.HexColor('#2C3E50'),
                'accent': colors.HexColor('#5D6D7E'),
                'background': colors.HexColor('#EBF5FB')
            }
        }
        
    def setup_custom_styles(self, color_scheme='blue'):
        """Setup technical-focused styles with dynamic colors"""
        colors_set = self.color_schemes.get(color_scheme, self.color_schemes['blue'])
        # Tech-style header
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=6,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#0D47A1'),
            fontName='Helvetica-Bold',
            borderWidth=2,
            borderColor=colors.HexColor('#0D47A1'),
            borderPadding=8
        ))
        
        # Technical contact info
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            spaceAfter=16,
            textColor=colors.HexColor('#37474F'),
            fontName='Courier'
        ))
        
        # Code-style section headings
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=16,
            spaceAfter=8,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#1976D2'),
            borderPadding=6
        ))
        
        # Technical job title
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=8,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#0D47A1')
        ))
        
        # Company style
        self.styles.add(ParagraphStyle(
            name='Organization',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=2,
            fontName='Helvetica',
            textColor=colors.HexColor('#424242')
        ))
        
        # Tech date style
        self.styles.add(ParagraphStyle(
            name='DateStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            textColor=colors.HexColor('#666666'),
            fontName='Courier'
        ))
        
        # Technical description
        self.styles.add(ParagraphStyle(
            name='Description',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#212121')
        ))
        
        # Code-style skills
        self.styles.add(ParagraphStyle(
            name='SkillsCode',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            textColor=colors.HexColor('#1565C0'),
            fontName='Courier',
            backColor=colors.HexColor('#F5F5F5'),
            borderPadding=3
        ))
    
    def generate(self, cv_data, filepath):
        """Generate technical CV"""
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
            
            # Technical summary
            if cv_data.get('summary'):
                story.extend(self._create_summary_section(cv_data['summary']))
            
            # Technical experience
            if cv_data.get('experience'):
                story.extend(self._create_experience_section(cv_data['experience']))
            
            # Education
            if cv_data.get('education'):
                story.extend(self._create_education_section(cv_data['education']))
            
            # Technical skills
            if cv_data.get('skills'):
                story.extend(self._create_skills_section(cv_data['skills']))
            
            doc.build(story)
            logging.info(f"Template5 CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating Template5 CV: {str(e)}")
            return False
    
    def _create_header(self, cv_data):
        """Create technical header with photo support"""
        elements = []
        
        # Check if profile photo exists
        profile_photo_path = cv_data.get('profile_photo')
        if profile_photo_path and os.path.exists(profile_photo_path):
            try:
                # Create table for header layout with photo
                from reportlab.platypus import Image
                img = Image(profile_photo_path, width=50*mm, height=50*mm)
                
                # Create info content
                info_content = []
                name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
                info_content.append(name)
                
                # Contact info in code style
                contact_lines = []
                if cv_data.get('email'):
                    contact_lines.append(f"email: {cv_data['email']}")
                if cv_data.get('phone'):
                    contact_lines.append(f"phone: {cv_data['phone']}")
                if cv_data.get('address'):
                    contact_lines.append(f"location: {cv_data['address']}")
                
                for line in contact_lines:
                    contact = Paragraph(line, self.styles['ContactInfo'])
                    info_content.append(contact)
                
                # Create table with photo and info
                header_data = [[img, info_content]]
                header_table = Table(header_data, colWidths=[60*mm, 130*mm])
                header_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ]))
                elements.append(header_table)
                
            except Exception as e:
                logging.error(f"Error adding photo to header: {str(e)}")
                # Fallback to text-only header
                elements.extend(self._create_text_header(cv_data))
        else:
            # No photo - use text-only header
            elements.extend(self._create_text_header(cv_data))
        
        return elements
    
    def _create_text_header(self, cv_data):
        """Create text-only header"""
        elements = []
        
        # Name with tech border
        name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
        elements.append(name)
        
        # Contact info in code style
        contact_lines = []
        if cv_data.get('email'):
            contact_lines.append(f"email: {cv_data['email']}")
        if cv_data.get('phone'):
            contact_lines.append(f"phone: {cv_data['phone']}")
        if cv_data.get('address'):
            contact_lines.append(f"location: {cv_data['address']}")
        
        for line in contact_lines:
            contact = Paragraph(line, self.styles['ContactInfo'])
            elements.append(contact)
        
        return elements
    
    def _create_summary_section(self, summary):
        """Create technical summary"""
        elements = []
        heading = Paragraph("// PROFESSIONAL SUMMARY", self.styles['SectionHeading'])
        elements.append(heading)
        summary_para = Paragraph(summary, self.styles['Description'])
        elements.append(summary_para)
        return elements
    
    def _create_experience_section(self, experience_list):
        """Create technical experience section"""
        elements = []
        heading = Paragraph("// WORK EXPERIENCE", self.styles['SectionHeading'])
        elements.append(heading)
        
        for exp in experience_list:
            exp_elements = self._parse_experience_entry(exp)
            elements.extend(exp_elements)
        
        return elements
    
    def _parse_experience_entry(self, experience_text):
        """Parse experience with technical formatting"""
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
        
        elements.append(Paragraph(f"function {job_title.replace(' ', '_').lower()}() {{", self.styles['JobTitle']))
        if company:
            elements.append(Paragraph(f"  company: '{company}'", self.styles['Organization']))
        
        # Find duration and description
        for line in lines[1:]:
            if any(keyword in line.lower() for keyword in ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                          'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
                                                          '20', '19', 'present', 'current', '-']):
                elements.append(Paragraph(f"  duration: '{line}'", self.styles['DateStyle']))
            else:
                elements.append(Paragraph(f"  // {line}", self.styles['Description']))
        
        elements.append(Paragraph("}", self.styles['JobTitle']))
        elements.append(Spacer(1, 6))
        
        return elements
    
    def _create_education_section(self, education_list):
        """Create technical education section"""
        elements = []
        heading = Paragraph("// EDUCATION", self.styles['SectionHeading'])
        elements.append(heading)
        
        for edu in education_list:
            edu_para = Paragraph(f"• {edu}", self.styles['Description'])
            elements.append(edu_para)
        
        return elements
    
    def _create_skills_section(self, skills_list):
        """Create code-style skills section"""
        elements = []
        heading = Paragraph("// TECHNICAL SKILLS", self.styles['SectionHeading'])
        elements.append(heading)
        
        if isinstance(skills_list, list):
            # Group skills by categories
            programming = []
            frameworks = []
            tools = []
            other = []
            
            for skill in skills_list:
                skill_lower = skill.lower()
                if any(lang in skill_lower for lang in ['python', 'java', 'javascript', 'c++', 'php', 'ruby', 'go', 'rust']):
                    programming.append(skill)
                elif any(fw in skill_lower for fw in ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express']):
                    frameworks.append(skill)
                elif any(tool in skill_lower for tool in ['git', 'docker', 'kubernetes', 'aws', 'azure', 'linux']):
                    tools.append(skill)
                else:
                    other.append(skill)
            
            if programming:
                quoted_prog = [f'"{s}"' for s in programming]
                prog_text = f"languages = [{', '.join(quoted_prog)}]"
                elements.append(Paragraph(prog_text, self.styles['SkillsCode']))
            
            if frameworks:
                quoted_fw = [f'"{s}"' for s in frameworks]
                fw_text = f"frameworks = [{', '.join(quoted_fw)}]"
                elements.append(Paragraph(fw_text, self.styles['SkillsCode']))
            
            if tools:
                quoted_tools = [f'"{s}"' for s in tools]
                tools_text = f"tools = [{', '.join(quoted_tools)}]"
                elements.append(Paragraph(tools_text, self.styles['SkillsCode']))
            
            if other:
                quoted_other = [f'"{s}"' for s in other]
                other_text = f"other = [{', '.join(quoted_other)}]"
                elements.append(Paragraph(other_text, self.styles['SkillsCode']))
        else:
            skills_text = f"skills = ['{str(skills_list)}']"
            elements.append(Paragraph(skills_text, self.styles['SkillsCode']))
        
        return elements
