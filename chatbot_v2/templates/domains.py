

from chatbot_v2.templates.hydrocarbon_acct_templates import (
    section_templates as hc_section_template,
    static_sections as hc_static_section
)

from chatbot_v2.templates.glsm_templates import (
    section_templates as glsm_section_template,
    static_sections as glsm_static_section
)

DOMAINS = {
    'Hydrocarbon Accounting': hc_section_template,
    'Gas Lift System Modelling': glsm_section_template,
}

STATIC_SECTIONS = {
    'Hydrocarbon Accounting': hc_static_section,
    'Gas Lift System Modelling': glsm_static_section,
}
