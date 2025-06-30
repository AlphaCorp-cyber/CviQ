
"""
Healthcare Professional CV Template
Designed for doctors, nurses, and healthcare professionals
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
        """Setup healthcare-focused styles"""
        # Medical header
        self.styles.add(ParagraphStyle(
            name='HeaderName',
            parent=self.styles['Title'],
            fontSize=26,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#C62828'),
            fontName='Helvetica-Bold'
        ))
        
        # Medical credentials
        self.styles.add(ParagraphStyle(
            name='Credentials',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=4,
            textColor=colors.HexColor('#D32F2F'),
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
        
        # Medical section headings
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=18,
            spaceAfter=8,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#D32F2F'),
            borderPadding=6
        ))
        
        # Position/specialty
        self.styles.add(ParagraphStyle(
            name='Position',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=8,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#C62828')
        ))
        
        # Medical facility
        self.styles.add(ParagraphStyle(
            name='Facility',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=2,
            fontName='Helvetica',
            textColor=colors.HexColor('#424242')
        ))
        
        # Medical dates
        self.styles.add(ParagraphStyle(
            name='MedicalDate',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            textColor=colors.HexColor('#757575')
        ))
        
        # Clinical description
        self.styles.add(ParagraphStyle(
            name='Clinical',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#212121')
        ))
        
        # Certification style
        self.styles.add(ParagraphStyle(
            name='Certification',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            textColor=colors.HexColor('#C62828'),
            fontName='Helvetica-Bold'
        ))
    
    def generate(self, cv_data, filepath):
        """Generate healthcare CV"""
        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=22*mm,
                leftMargin=22*mm,
                topMargin=20*mm,
                bottomMargin=20*mm
            )
            
            story = []
            
            # Header
            story.extend(self._create_header(cv_data))
            
            # Professional summary
            if cv_data.get('summary'):
                story.extend(self._create_summary_section(cv_data['summary']))
            
            # Clinical experience
            if cv_data.get('experience'):
                story.extend(self._create_experience_section(cv_data['experience']))
            
            # Medical education
            if cv_data.get('education'):
                story.extend(self._create_education_section(cv_data['education']))
            
            # Clinical skills & certifications
            if cv_data.get('skills'):
                story.extend(self._create_skills_section(cv_data['skills']))
            
            doc.build(story)
            logging.info(f"Template8 CV generated: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating Template8 CV: {str(e)}")
            return False
    
    def _create_header(self, cv_data):
        """Create medical header with photo support"""
        import os
        elements = []
        
        # Check if profile photo exists
        profile_photo_path = cv_data.get('profile_photo')
        if profile_photo_path and os.path.exists(profile_photo_path):
            try:
                from reportlab.platypus import Image, Table, TableStyle
                img = Image(profile_photo_path, width=55*mm, height=55*mm)
                
                # Create info content
                info_content = []
                name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
                info_content.append(name)
                credentials = Paragraph("M.D. | Healthcare Professional", self.styles['Credentials'])
                info_content.append(credentials)
                
                # Contact info
                contact_parts = []
                if cv_data.get('phone'):
                    contact_parts.append(f"☎ {cv_data['phone']}")
                if cv_data.get('email'):
                    contact_parts.append(f"✉ {cv_data['email']}")
                if cv_data.get('address'):
                    contact_parts.append(f"⚕ {cv_data['address']}")
                
                if contact_parts:
                    contact_text = " | ".join(contact_parts)
                    contact = Paragraph(contact_text, self.styles['ContactInfo'])
                    info_content.append(contact)
                
                # Create table with photo and info
                header_data = [[img, info_content]]
                header_table = Table(header_data, colWidths=[65*mm, 125*mm])
                header_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ]))
                elements.append(header_table)
                
            except Exception as e:
                logging.error(f"Error adding photo to healthcare header: {str(e)}")
                elements.extend(self._create_text_header(cv_data))
        else:
            elements.extend(self._create_text_header(cv_data))
        
        return elements
    
    def _create_text_header(self, cv_data):
        """Create text-only header"""
        elements = []
        
        # Name
        name = Paragraph(cv_data.get('full_name', ''), self.styles['HeaderName'])
        elements.append(name)
        
        # Medical credentials
        credentials = Paragraph("M.D. | Healthcare Professional", self.styles['Credentials'])
        elements.append(credentials)
        
        # Contact info with medical symbols
        contact_parts = []
        if cv_data.get('phone'):
            contact_parts.append(f"☎ {cv_data['phone']}")
        if cv_data.get('email'):
            contact_parts.append(f"✉ {cv_data['email']}")
        if cv_data.get('address'):
            contact_parts.append(f"⚕ {cv_data['address']}")
        
        if contact_parts:
            contact_text = " | ".join(contact_parts)
            contact = Paragraph(contact_text, self.styles['ContactInfo'])
            elements.append(contact)
        
        return elements
    
    def _create_summary_section(self, summary):
        """Create professional summary"""
        elements = []
        heading = Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeading'])
        elements.append(heading)
        summary_para = Paragraph(summary, self.styles['Clinical'])
        elements.append(summary_para)
        return elements
    
    def _create_experience_section(self, experience_list):
        """Create clinical experience section"""
        elements = []
        heading = Paragraph("CLINICAL EXPERIENCE", self.styles['SectionHeading'])
        elements.append(heading)
        
        for exp in experience_list:
            exp_elements = self._parse_experience_entry(exp)
            elements.extend(exp_elements)
        
        return elements
    
    def _parse_experience_entry(self, experience_text):
        """Parse medical experience entry"""
        elements = []
        lines = [line.strip() for line in experience_text.split('\n') if line.strip()]
        
        if not lines:
            return elements
        
        first_line = lines[0]
        if ' at ' in first_line:
            parts = first_line.split(' at ', 1)
            position = parts[0].strip()
            facility = parts[1].strip()
        else:
            position = first_line
            facility = ""
        
        elements.append(Paragraph(f"⚕ {position}", self.styles['Position']))
        if facility:
            elements.append(Paragraph(facility, self.styles['Facility']))
        
        # Find dates and responsibilities
        for line in lines[1:]:
            if any(keyword in line.lower() for keyword in ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                          'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
                                                          '20', '19', 'present', 'current', '-']):
                elements.append(Paragraph(f"📅 {line}", self.styles['MedicalDate']))
            else:
                # Highlight clinical responsibilities
                if any(keyword in line.lower() for keyword in ['patient', 'diagnosis', 'treatment', 'surgery', 'care', 'clinical']):
                    clinical_text = f"• {line}"
                    elements.append(Paragraph(clinical_text, self.styles['Clinical']))
                else:
                    elements.append(Paragraph(line, self.styles['Clinical']))
        
        elements.append(Spacer(1, 8))
        return elements
    
    def _create_education_section(self, education_list):
        """Create medical education section"""
        elements = []
        heading = Paragraph("MEDICAL EDUCATION", self.styles['SectionHeading'])
        elements.append(heading)
        
        for edu in education_list:
            edu_elements = self._parse_education_entry(edu)
            elements.extend(edu_elements)
        
        return elements
    
    def _parse_education_entry(self, education_text):
        """Parse medical education entry"""
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
            elements.append(Paragraph(institution, self.styles['Facility']))
        
        # Add additional education details
        for line in lines[1:]:
            if any(keyword in line for keyword in ['20', '19']) and len(line) < 20:
                elements.append(Paragraph(f"📅 {line}", self.styles['MedicalDate']))
            else:
                elements.append(Paragraph(line, self.styles['Clinical']))
        
        elements.append(Spacer(1, 6))
        return elements
    
    def _create_skills_section(self, skills_list):
        """Create clinical skills and certifications"""
        elements = []
        heading = Paragraph("CLINICAL SKILLS & CERTIFICATIONS", self.styles['SectionHeading'])
        elements.append(heading)
        
        if isinstance(skills_list, list):
            # Categorize skills
            clinical_skills = []
            certifications = []
            technical_skills = []
            
            for skill in skills_list:
                skill_lower = skill.lower()
                if any(cert in skill_lower for cert in ['certification', 'certified', 'license', 'board']):
                    certifications.append(skill)
                elif any(clinical in skill_lower for clinical in ['patient', 'surgery', 'diagnosis', 'treatment', 'clinical']):
                    clinical_skills.append(skill)
                else:
                    technical_skills.append(skill)
            
            # Display certifications first
            if certifications:
                cert_heading = Paragraph("Certifications & Licenses:", self.styles['Certification'])
                elements.append(cert_heading)
                for cert in certifications:
                    cert_para = Paragraph(f"✓ {cert}", self.styles['Clinical'])
                    elements.append(cert_para)
                elements.append(Spacer(1, 6))
            
            # Clinical skills
            if clinical_skills:
                clinical_heading = Paragraph("Clinical Competencies:", self.styles['Certification'])
                elements.append(clinical_heading)
                for skill in clinical_skills:
                    skill_para = Paragraph(f"⚕ {skill}", self.styles['Clinical'])
                    elements.append(skill_para)
                elements.append(Spacer(1, 6))
            
            # Technical skills
            if technical_skills:
                tech_heading = Paragraph("Technical Skills:", self.styles['Certification'])
                elements.append(tech_heading)
                for skill in technical_skills:
                    skill_para = Paragraph(f"• {skill}", self.styles['Clinical'])
                    elements.append(skill_para)
        else:
            skills_para = Paragraph(f"⚕ {str(skills_list)}", self.styles['Clinical'])
            elements.append(skills_para)
        
        return elements
