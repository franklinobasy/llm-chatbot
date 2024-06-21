"""
Module: template_handler.py

Contains utility functions for handling templates.

Classes:
    - TemplateHandler: Class for handling templates.

"""

from chatbot_v2.templates.domains import DOMAINS
from chatbot_v2.templates.templates import clean_template
from chatbot_v2.handlers.base_handler import BaseHandler


class TemplateHandler(BaseHandler):
    """
    Class for handling templates.
    """

    def __init__(self, domain, section_type):
        """
        Initialize the TemplateHandler.

        Parameters:
            section_type (str): The type of section for which templates need to be handled.
        """
        super().__init__(domain, section_type)

    @property
    def section(self):
        """
        Getter property for the section template.

        Returns:
            dict: The section template.
        """
        return self._section_template

    @section.setter
    def section(self, section_type: str):
        """
        Setter property for the section template.

        Parameters:
            section_type (str): The type of section for which templates need to be handled.
        """
        if section_type not in DOMAINS[self.domain].keys():
            raise ValueError(
                f'This section type: "{section_type}" is not supported.\
                \nAvailable supported sections are: {list(DOMAINS[self.domain].keys())}'
            )
        self._section_template = DOMAINS[self.domain].get(section_type)

    def get_template(self):
        """
        Get templates from the section template.

        Returns:
            List[str]: List of templates extracted from the section template.
        """
        return self._section_template.get('1')[0]
        

    def get_hint(self):
        """
        Get hints from the section template.

        Returns:
            List[str]: List of summaries extracted from the section template.
        """
        if len(self._section_template.get('1')) < 2:
            raise Exception('No hint available')
        return self._section_template.get('1')[1]

    def get_template_data(self):
        """
        Get data including summaries and templates from the section template.

        Returns:
            List[Dict[str, str]]: List of dictionaries containing the summary and template data.
        """
        return self._section_template.get('1')
