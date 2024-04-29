"""
Module: nda/templates.py

Contains utility functions for preparing sections and
questions from NDA templates.

Functions:
    - prepare_sections: Function to prepare sections from NDA templates.
    - prepare_questions: Function to prepare questions from NDA templates.

Classes:
    - NDA: Class for handling NDA templates.

Attributes:
    - BASE_PATH (str): The base path for NDA templates.

"""

import os
from chatbot_v2.templates.templates import create_section, create_question

BASE_PATH = os.path.join(os.getcwd(), "data", "NDA", "NDA_templates")


class NDA:
    """
    Class for handling NDA templates.
    """

    def __init__(self, base_path=BASE_PATH):
        """
        Initialize the NDA class.

        Parameters:
            base_path (str): The base path for the NDA templates.
        """
        self.base_path = base_path
        self.section_names = [f"section_{i}" for i in range(1, 5)]

    def prepare_sections(self):
        """
        Prepare sections from NDA templates.

        Returns:
            List[str]: List of prepared sections.
        """
        raw_sections = [
            create_section(section_name, "", base_path=self.base_path)
            for section_name in self.section_names
        ]

        sections = []
        for section in raw_sections:
            sections += [section["1"][-1]]

        return sections

    def prepare_questions(self):
        """
        Prepare questions from NDA templates.

        Returns:
            List[str]: List of prepared questions.
        """
        raw_questions = [
            create_question(section_name, base_path=self.base_path)
            for section_name in self.section_names
        ]

        questions = []

        for item in raw_questions:
            for qs in list(item.values()):
                questions += qs.split("\n")

        questions = list(filter(lambda x: x, questions))

        return questions
