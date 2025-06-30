"""
CV Templates Package

This package contains different CV template generators.
Each template is implemented as a separate module with a TemplateGenerator class.
"""

__version__ = '1.0.0'
__author__ = 'CV Maker Bot'

# Import all available templates
from . import template1
from . import template2

# List of available templates
AVAILABLE_TEMPLATES = [
    'template1',
    'template2'
]

def get_template_generator(template_name):
    """Get template generator by name"""
    if template_name == 'template1':
        return template1.TemplateGenerator
    elif template_name == 'template2':
        return template2.TemplateGenerator
    else:
        raise ValueError(f"Unknown template: {template_name}")
