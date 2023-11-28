from typing import Dict, List, Tuple
from chatbot_v2.templates.dynamic_template_search import BASE_PATH, files_for_section


def clean_template(item: Tuple) -> Tuple[str, List[str]]:
    """Utility for cleaning template texts"""
    item = list(item)
    summary = item[1][0].replace("\n", "").replace(" " * 8, "")
    template = item[1][1].replace("\n", "").replace(" " * 8, "")
    item = (item[0], [summary, template])
    return item


def clean_question(item: Tuple) -> Tuple[str, str]:
    """Utility for cleaning question texts"""
    item = list(item)
    question = item[1].replace("\n", "").replace(" " * 4, "")
    item = (item[0], question)
    return item


def create_section(section_name, c_summary, base_path=BASE_PATH):
    '''Creates a section'''
    dict_ = {}
    for i, template in enumerate(
        files_for_section(base_path, section_name),
        start=1
    ):
        values = [
            c_summary,
            template
        ]
        dict_[str(i)] = values
    return dict_


def create_question(section_name, base_path=BASE_PATH):
    '''Create a section questions'''
    dict_ = {}
    for i, question in enumerate(
        files_for_section(base_path, section_name, get_questions=True),
        start=1
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
EXECUTIVE_SUMMARY_TEMPLATE = create_section(
    "executive_summary", "EXECUTIVE SUMMARY"
)


OVERVIEW_QUESTIONS = create_question("overview")
INTRODUCTION_DESCRIPTION_QUESTIONS = create_question("introduction")
PROBLEM_DESCRIPTION_QUESTIONS = create_question("problem")
PROPOSED_SOLUTION_QUESTIONS = create_question("proposed_solution")
IMPORTANCE_DESCRIPTION_QUESTION = create_question("importance")
BENEFITS_DESCRIPTION_QUESTION = create_question("benefits")
EXECUTIVE_SUMMARY_QUESTION = create_question("executive_summary")

# templates
section_templates: Dict[str, List[Dict]] = {
    "about_cyphercrescent": [
        ABOUT_CYPHERCRESCENT
        ],
    "our_team": [
        OUR_TEAM
        ],
    "our_commitment": [
        OUR_COMMITMENT
        ],
    "our_clients": [
        OUR_CLIENTS
        ],
    "overview_template": [
        OVERVIEW_TEMPLATE, OVERVIEW_QUESTIONS
        ],
    "introduction": [
        INTRODUCTION_TEMPLATES, INTRODUCTION_DESCRIPTION_QUESTIONS
        ],
    "problems": [
        PROBLEM_TEMPLATE, PROBLEM_DESCRIPTION_QUESTIONS
        ],
    "proposed_solution": [
        PROPOSED_SOLUTION_TEMPLATE, PROPOSED_SOLUTION_QUESTIONS
        ],
    "importance": [
        IMPORTANCE_TEMPLATE, IMPORTANCE_DESCRIPTION_QUESTION
        ],
    "benefits": [
        BENEFITS_TEMPLATE, BENEFITS_DESCRIPTION_QUESTION
        ],
    "executive_summary": [
        EXECUTIVE_SUMMARY_TEMPLATE, EXECUTIVE_SUMMARY_QUESTION
        ],
}
