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

from typing import Dict, List, Tuple
from chatbot_v2.templates.dynamic_template_search import BASE_PATH, files_for_section


def clean_template(item: Tuple) -> Tuple[str, List[str]]:
    """
    Utility function to clean template texts.

    Parameters:
        item (Tuple): Tuple containing the template summary and template text.

    Returns:
        Tuple[str, List[str]]: Cleaned template summary and template text.
    """
    item = list(item)
    summary = item[1][0].replace("\n", "").replace(" " * 8, "")
    template = item[1][1].replace("\n", "").replace(" " * 8, "")
    item = (item[0], [summary, template])
    return item


def clean_question(item: Tuple) -> Tuple[str, str]:
    """
    Utility function to clean question texts.

    Parameters:
        item (Tuple): Tuple containing the question identifier and question text.

    Returns:
        Tuple[str, str]: Cleaned question identifier and question text.
    """
    item = list(item)
    question = item[1].replace("\n", "").replace(" " * 4, "")
    item = (item[0], question)
    return item


def create_section(section_name, c_summary, base_path=BASE_PATH):
    """
    Creates a section.

    Parameters:
        section_name (str): Name of the section.
        c_summary (str): Summary of the section.
        base_path (str, optional): Base path for the templates. Defaults to BASE_PATH.

    Returns:
        dict: Dictionary containing the section.
    """
    dict_ = {}
    for i, template in enumerate(files_for_section(base_path, section_name), start=1):
        values = [c_summary, template]
        dict_[str(i)] = values
    return dict_


def create_question(section_name, base_path=BASE_PATH):
    """
    Creates section questions.

    Parameters:
        section_name (str): Name of the section.
        base_path (str, optional): Base path for the templates. Defaults to BASE_PATH.

    Returns:
        dict: Dictionary containing the section questions.
    """
    dict_ = {}
    for i, question in enumerate(
        files_for_section(base_path, section_name, get_questions=True), start=1
    ):
        dict_[f"Question {i}"] = question

    return dict_


ABOUT_CYPHERCRESCENT = create_section("about", "ABOUT CYPHERCRESCENT SUMMARY")
OUR_TEAM = create_section("our_team", "OUR TEAM SUMMARY")
OUR_COMMITMENT = create_section("our_commitment", "OUR COMMITMENT SUMMARY")
OUR_CLIENTS = create_section("our_clients", "OUR CLIENT SUMMARY")
INTRODUCTION_TEMPLATES = create_section("introduction", "INTRODUCTION SUMMARY")
OVERVIEW_TEMPLATE = create_section("overview", "OVERVIEW TEMPLATE")
PROBLEM_TEMPLATE = create_section("problem", "PROBLEM SUMMARY")
PROPOSED_SOLUTION_TEMPLATE = create_section(
    "proposed_solution", "PROPOSED_SOLUTION_TEMPLATES"
)
IMPORTANCE_TEMPLATE = create_section("importance", "IMPORTANCE DESCRIPTION")
BENEFITS_TEMPLATE = create_section("benefits", "BENEFITS TEMPLATE")
EXECUTIVE_SUMMARY_TEMPLATE = create_section("executive_summary", "EXECUTIVE SUMMARY")


OVERVIEW_QUESTIONS = create_question("overview")
INTRODUCTION_DESCRIPTION_QUESTIONS = create_question("introduction")
PROBLEM_DESCRIPTION_QUESTIONS = create_question("problem")
PROPOSED_SOLUTION_QUESTIONS = create_question("proposed_solution")
IMPORTANCE_DESCRIPTION_QUESTION = create_question("importance")
BENEFITS_DESCRIPTION_QUESTION = create_question("benefits")
EXECUTIVE_SUMMARY_QUESTION = create_question("executive_summary")

# templates
section_templates: Dict[str, List[Dict]] = {
    "about_cyphercrescent": [ABOUT_CYPHERCRESCENT],
    "our_team": [OUR_TEAM],
    "our_commitment": [OUR_COMMITMENT],
    "our_clients": [OUR_CLIENTS],
    "overview_template": [OVERVIEW_TEMPLATE, OVERVIEW_QUESTIONS],
    "introduction": [INTRODUCTION_TEMPLATES, INTRODUCTION_DESCRIPTION_QUESTIONS],
    "problems": [PROBLEM_TEMPLATE, PROBLEM_DESCRIPTION_QUESTIONS],
    "proposed_solution": [PROPOSED_SOLUTION_TEMPLATE, PROPOSED_SOLUTION_QUESTIONS],
    "importance": [IMPORTANCE_TEMPLATE, IMPORTANCE_DESCRIPTION_QUESTION],
    "benefits": [BENEFITS_TEMPLATE, BENEFITS_DESCRIPTION_QUESTION],
    "executive_summary": [EXECUTIVE_SUMMARY_TEMPLATE, EXECUTIVE_SUMMARY_QUESTION],
}
