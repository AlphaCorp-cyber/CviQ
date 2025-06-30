
"""
Creative Arts CV Template
Designed for artists, designers, and creative professionals
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
        """Setup creative artistic styles"""
        # Artistic header
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=30,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#8E24AA'),
            fontName='Helvetica-Bold'
        ))
        
        # Creative tagline
        self.styles.add(ParagraphStyle(
            name='CreativeTagline',
            parent=self.styles['Normal'],
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=4,
            textColor=colors.HexColor('#AB47BC'),
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
        
        # Creative section headings
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#9C27B0'),
            borderPadding=8,
            alignment=TA_CENTER
        ))
        
        # Project/role title
        self.styles.add(ParagraphStyle(
            name='ProjectTitle',
            parent=self.styles['Normal'],
            fontSize=13,
            spaceBefore=10,
            spaceAfter=3,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#8E24AA')
        ))
        
        # Client/company
        self.styles.add(ParagraphStyle(
            name='Client',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=2,
            fontName='Helvetica-Oblique',
            textColor=colors.HexColor('#AB47BC')
        ))
        
        # Creative description
        self.styles.add(ParagraphStyle(
            name='CreativeDescription',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#212121')
        ))
        
        # Medium/technique style
        self.styles.add(ParagraphStyle(
            name='Medium',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            textColor=colors.HexColor('#8E24AA'),
            fontName='Helvetica-Oblique'
        ))
        
        # Exhibition/award style
        self.styles.add(ParagraphStyle(
            name='Exhibition',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=colors.HexColor('#6A1B9A'),
            fontName='Helvetica-Bold'
        ))
    
    def generate(self, cv_data, filepath):
        """Generate creative arts CV"""
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
            
            # Artist statement
            if cv_data.get('summary'):
                story.extend(self._create_summary_section(cv_data['summary']))
            
            # Creative experience
            if cv_data.get('experience'):
                story.extend(self._create_experience_section(cv_data['experience']))
            
            # Education
            if cv_data.get('education'):
                story.extend(self._create_education_section(cv_data['education']))
            
            # Creative skills
            if cv_data.get('skills'):
                story.extend(self._create_skills_section(cv_data['skills']))
            
            doc.build(story)
            logging.info(f"Template10 CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating Template10 CV: {str(e)}")
            return False
    
    def _create_header(self, cv_data):
        """Create artistic header with photo support"""
        import os
        elements = []
        
        # Check if profile photo exists
        profile_photo_path = cv_data.get('profile_photo')
        if profile_photo_path and os.path.exists(profile_photo_path):
            try:
                from reportlab.platypus import Image, Table, TableStyle
                img = Image(profile_photo_path, width=60*mm, height=60*mm)
                
                # Create info content
                info_content = []
                name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
                info_content.append(name)
                tagline = Paragraph("✨ Creative Artist & Designer ✨", self.styles['CreativeTagline'])
                info_content.append(tagline)
                
                # Contact info
                contact_parts = []
                if cv_data.get('email'):
                    contact_parts.append(f"✉ {cv_data['email']}")
                if cv_data.get('phone'):
                    contact_parts.append(f"☎ {cv_data['phone']}")
                if cv_data.get('address'):
                    contact_parts.append(f"🎨 {cv_data['address']}")
                
                if contact_parts:
                    contact_text = " • ".join(contact_parts)
                    contact = Paragraph(contact_text, self.styles['ContactInfo'])
                    info_content.append(contact)
                
                # Create table with photo and info
                header_data = [[img, info_content]]
                header_table = Table(header_data, colWidths=[70*mm, 120*mm])
                header_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ]))
                elements.append(header_table)
                
            except Exception as e:
                logging.error(f"Error adding photo to creative header: {str(e)}")
                elements.extend(self._create_text_header(cv_data))
        else:
            elements.extend(self._create_text_header(cv_data))
        
        return elements
    
    def _create_text_header(self, cv_data):
        """Create text-only header"""
        elements = []
        
        # Name with artistic flair
        name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
        elements.append(name)
        
        # Creative tagline
        tagline = Paragraph("✨ Creative Artist & Designer ✨", self.styles['CreativeTagline'])
        elements.append(tagline)
        
        # Contact info with creative symbols
        contact_parts = []
        if cv_data.get('email'):
            contact_parts.append(f"✉ {cv_data['email']}")
        if cv_data.get('phone'):
            contact_parts.append(f"☎ {cv_data['phone']}")
        if cv_data.get('address'):
            contact_parts.append(f"🎨 {cv_data['address']}")
        
        if contact_parts:
            contact_text = " • ".join(contact_parts)
            contact = Paragraph(contact_text, self.styles['ContactInfo'])
            elements.append(contact)
        
        return elements
    
    def _create_summary_section(self, summary):
        """Create artist statement"""
        elements = []
        heading = Paragraph("🎭 ARTIST STATEMENT", self.styles['SectionHeading'])
        elements.append(heading)
        summary_para = Paragraph(summary, self.styles['CreativeDescription'])
        elements.append(summary_para)
        return elements
    
    def _create_experience_section(self, experience_list):
        """Create creative experience section"""
        elements = []
        heading = Paragraph("🎨 CREATIVE EXPERIENCE", self.styles['SectionHeading'])
        elements.append(heading)
        
        for exp in experience_list:
            exp_elements = self._parse_experience_entry(exp)
            elements.extend(exp_elements)
        
        return elements
    
    def _parse_experience_entry(self, experience_text):
        """Parse creative experience entry"""
        elements = []
        lines = [line.strip() for line in experience_text.split('\n') if line.strip()]
        
        if not lines:
            return elements
        
        first_line = lines[0]
        if ' at ' in first_line:
            parts = first_line.split(' at ', 1)
            project = parts[0].strip()
            client = parts[1].strip()
        elif ' for ' in first_line:
            parts = first_line.split(' for ', 1)
            project = parts[0].strip()
            client = parts[1].strip()
        else:
            project = first_line
            client = ""
        
        elements.append(Paragraph(f"🎯 {project}", self.styles['ProjectTitle']))
        if client:
            elements.append(Paragraph(f"Client: {client}", self.styles['Client']))
        
        # Parse creative details
        for line in lines[1:]:
            line_lower = line.lower()
            
            # Check for dates
            if any(keyword in line_lower for keyword in ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                        'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
                                                        '20', '19', 'present', 'current', '-']):
                elements.append(Paragraph(f"📅 {line}", self.styles['Medium']))
            
            # Check for mediums/techniques
            elif any(medium in line_lower for medium in ['oil', 'acrylic', 'watercolor', 'digital', 'photography', 
                                                        'sculpture', 'illustration', 'design', 'photoshop', 
                                                        'illustrator', 'canvas', 'medium:', 'technique:']):
                elements.append(Paragraph(f"🖌️ {line}", self.styles['Medium']))
            
            # Check for exhibitions/awards
            elif any(achievement in line_lower for achievement in ['exhibition', 'award', 'gallery', 'show', 
                                                                 'featured', 'published', 'won', 'selected']):
                elements.append(Paragraph(f"🏆 {line}", self.styles['Exhibition']))
            
            else:
                elements.append(Paragraph(f"• {line}", self.styles['CreativeDescription']))
        
        elements.append(Spacer(1, 8))
        return elements
    
    def _create_education_section(self, education_list):
        """Create education section"""
        elements = []
        heading = Paragraph("🎓 EDUCATION & TRAINING", self.styles['SectionHeading'])
        elements.append(heading)
        
        for edu in education_list:
            edu_elements = self._parse_education_entry(edu)
            elements.extend(edu_elements)
        
        return elements
    
    def _parse_education_entry(self, education_text):
        """Parse artistic education entry"""
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
        
        elements.append(Paragraph(f"🎓 {degree}", self.styles['ProjectTitle']))
        if institution:
            elements.append(Paragraph(institution, self.styles['Client']))
        
        # Add additional details
        for line in lines[1:]:
            if any(keyword in line for keyword in ['20', '19']) and len(line) < 20:
                elements.append(Paragraph(f"📅 {line}", self.styles['Medium']))
            else:
                elements.append(Paragraph(line, self.styles['CreativeDescription']))
        
        elements.append(Spacer(1, 6))
        return elements
    
    def _create_skills_section(self, skills_list):
        """Create creative skills section"""
        elements = []
        heading = Paragraph("🛠️ CREATIVE TOOLKIT", self.styles['SectionHeading'])
        elements.append(heading)
        
        if isinstance(skills_list, list):
            # Categorize creative skills
            software = []
            traditional = []
            techniques = []
            other = []
            
            for skill in skills_list:
                skill_lower = skill.lower()
                if any(soft in skill_lower for soft in ['photoshop', 'illustrator', 'indesign', 'lightroom', 
                                                       'after effects', 'premiere', 'blender', 'maya', 
                                                       'figma', 'sketch', 'autocad']):
                    software.append(skill)
                elif any(trad in skill_lower for trad in ['oil', 'acrylic', 'watercolor', 'charcoal', 
                                                         'pencil', 'pen', 'ink', 'sculpture', 'ceramic']):
                    traditional.append(skill)
                elif any(tech in skill_lower for tech in ['photography', 'printing', 'framing', 'installation',
                                                         'digital art', 'web design', 'typography']):
                    techniques.append(skill)
                else:
                    other.append(skill)
            
            # Create colorful skills display
            skills_data = []
            
            if software:
                skills_data.append(['💻 Digital Tools:', ' • '.join(software)])
            if traditional:
                skills_data.append(['🎨 Traditional Media:', ' • '.join(traditional)])
            if techniques:
                skills_data.append(['⚡ Techniques:', ' • '.join(techniques)])
            if other:
                skills_data.append(['✨ Other Skills:', ' • '.join(other)])
            
            if skills_data:
                skills_table = Table(skills_data, colWidths=[4*cm, 13*cm])
                skills_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#8E24AA')),
                    ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#212121')),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ('TOPPADDING', (0, 0), (-1, -1), 3),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
                elements.append(skills_table)
        else:
            skills_para = Paragraph(f"🎨 {str(skills_list)}", self.styles['CreativeDescription'])
            elements.append(skills_para)
        
        return elements
