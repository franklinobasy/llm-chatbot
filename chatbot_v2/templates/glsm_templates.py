"""
Module: templates.py

Contains utility functions and templates for generating sections and questions.

Functions:
    - clean_template: Utility function to clean template texts.
    - clean_question: Utility function to clean question texts.
    - create_section: Function to create a section.
    - create_question: Function to create section questions.

Attributes:
    - section_templates (dict): Dictionary containing templates for different sections.

"""

import os
from chatbot_v2.templates.dynamic_template_search_v2 import files_for_section


# Define the top-level folder path
BASE_PATH = os.path.join(os.getcwd(), "chatbot_v2",
                         "templates", "gas_lift_system_modelling")


def get_section(section_name, include_hint=False, base_path=BASE_PATH):
    """
    Get a section.

    Parameters:
        section_name (str): Name of the section.
        include_hint (bool): Whether or not to include section context
        base_path (str, optional): Base path for the templates. Defaults to BASE_PATH.

    Returns:
        dict: Dictionary containing the section.
    """
    dict_ = {}
    contexts = None
    if include_hint:
        contexts = files_for_section(base_path, section_name, get_hint=True)
    sections = files_for_section(base_path, section_name)
    for i, template in enumerate(zip(sections, contexts) if include_hint else (sections), start=1):
        dict_[str(i)] = template
    return dict_


def get_hints(section_name, base_path=BASE_PATH):
    """
    Get section hints.

    Parameters:
        section_name (str): Name of the section.
        base_path (str, optional): Base path for the templates. Defaults to BASE_PATH.

    Returns:
        dict: Dictionary containing the section questions.
    """
    dict_ = {}
    for i, hint in enumerate(
        files_for_section(base_path, section_name, get_hint=True), start=1
    ):
        dict_[f"Hint {i}"] = hint

    return dict_


ABOUT = get_section('about', include_hint=True)
COST_BENEFIT_ANALYSIS = get_section('cost_benefit_analysis', include_hint=True)
DATA_PROCESSING = get_section('data_processing', include_hint=True)
EXECUTIVE_SUMMARY = get_section('executive_summary', include_hint=True)
GAS_LIFT_NETWORK_OPTIMISATION = get_section('gas_lift_network_optimisation', include_hint=True)
GAS_LIFT_REVIEW_SCENARIO = get_section('gas_lift_review_scenario', include_hint=True)
INTRODUCTION = get_section('introduction', include_hint=True)
IPSM = get_section('ipsm', include_hint=True)
OUR_CLIENTS = get_section('our_clients', include_hint=True)
OUR_SERVICES = get_section('our_services', include_hint=True)
OUR_TEAM = get_section('our_team', include_hint=True)
PROJECT_DETAILS = get_section('project_details', include_hint=True)
PROJECT_DELIVERABLES = get_section('project_deliverables', include_hint=True)
PROJECT_OBJECTIVES = get_section('project_objectives', include_hint=True)
PROJECT_PERSONNEL = get_section('project_personnel', include_hint=True)
PROJECT_SCOPE = get_section('project_scope', include_hint=True)
PROJECT_TIMELINE = get_section('project_timeline', include_hint=True)
PSOW_FOR_OPERATIONALISATION = get_section('psow_for_operationalisation', include_hint=True)
ROUTINE_GLS_CALLIBERATION_SURVELLANCE_SETUP = get_section('routine_gls_calliberation_survellance_setup', include_hint=True)
WELL_PERFORMANCE_REVIEW = get_section('well_performance_review', include_hint=True)

section_templates = {
    'about': ABOUT,
    'cost_benefit_analysis': COST_BENEFIT_ANALYSIS,
    'data_processing': DATA_PROCESSING,
    'executive_summary': EXECUTIVE_SUMMARY,
    'gas_lift_network_optimisation': GAS_LIFT_NETWORK_OPTIMISATION,
    'gas_lift_review_scenario': GAS_LIFT_REVIEW_SCENARIO,
    'introduction': INTRODUCTION,
    'ipsm': IPSM,
    'our_clients': OUR_CLIENTS,
    'our_services': OUR_SERVICES,
    'our_team': OUR_TEAM,
    'project_details': PROJECT_DETAILS,
    'project_deliverables': PROJECT_DELIVERABLES,
    'project_objectives': PROJECT_OBJECTIVES,
    'project_personnel': PROJECT_PERSONNEL,
    'project_scope': PROJECT_SCOPE,
    'project_timeline': PROJECT_TIMELINE,
    'psow_for_operationalisation': PSOW_FOR_OPERATIONALISATION,
    'routine_gls_calliberation_survellance_setup': ROUTINE_GLS_CALLIBERATION_SURVELLANCE_SETUP,
    'well_performance_review': WELL_PERFORMANCE_REVIEW,
}


static_sections = [
    
]
