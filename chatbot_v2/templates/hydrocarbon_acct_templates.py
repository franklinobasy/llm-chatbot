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
                         "templates", "hydrocarbon_accounting")


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


INTRODUCTION = get_section('introduction', include_hint=True)
CURRENT_CHALLENGES = get_section('current_challenges', include_hint=True)
OBJECTIVES = get_section('objectives', include_hint=True)
COLLABORATIVE_APPROACH = get_section('collaborative_approach', include_hint=True)
CONCLUSION = get_section('conclusion', include_hint=True)
PROPOSED_SOLUTION = get_section('proposed_solution', include_hint=True)
STRATEGIC_INVESTMENT_PLAN = get_section('strategic_investment_plan', include_hint=True)


section_templates = {
    'introduction': INTRODUCTION,
    'collaborative_approach': COLLABORATIVE_APPROACH,
    'objectives': OBJECTIVES,
    'current_challenges': CURRENT_CHALLENGES,
    'proposed_solution': PROPOSED_SOLUTION,
    'strategic_investment_plan': STRATEGIC_INVESTMENT_PLAN,
    'conclusion': CONCLUSION
}

static_sections = [
    
]
