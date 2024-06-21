

from chatbot_v2.templates.hydrocarbon_acct_templates import (
    section_templates as hc_section_template,
    static_sections as hc_static_section
)

DOMAINS = {
    'Hydrocarbon Accounting': hc_section_template,
    'Gas Lift System Modelling': None,
}

STATIC_SECTIONS = {
    'Hydrocarbon Accounting': hc_static_section,
    'Gas Lift System Modelling': None,
}
