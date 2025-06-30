
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
from . import template3
from . import template4
from . import template5
from . import template6
from . import template7
from . import template8
from . import template9
from . import template10

# List of available templates
AVAILABLE_TEMPLATES = [
    'template1',
    'template2',
    'template3',
    'template4',
    'template5',
    'template6',
    'template7',
    'template8',
    'template9',
    'template10'
]

def get_template_generator(template_name):
    """Get template generator by name"""
    if template_name == 'template1':
        return template1.TemplateGenerator
    elif template_name == 'template2':
        return template2.TemplateGenerator
    elif template_name == 'template3':
        return template3.TemplateGenerator
    elif template_name == 'template4':
        return template4.TemplateGenerator
    elif template_name == 'template5':
        return template5.TemplateGenerator
    elif template_name == 'template6':
        return template6.TemplateGenerator
    elif template_name == 'template7':
        return template7.TemplateGenerator
    elif template_name == 'template8':
        return template8.TemplateGenerator
    elif template_name == 'template9':
        return template9.TemplateGenerator
    elif template_name == 'template10':
        return template10.TemplateGenerator
    else:
        raise ValueError(f"Unknown template: {template_name}")
