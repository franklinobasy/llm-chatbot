"""
Module: template_handler.py

Contains utility functions for handling templates.

Classes:
    - TemplateHandler: Class for handling templates.

"""

from chatbot_v2.templates.templates import clean_template
from chatbot_v2.handlers.base_handler import BaseHandler, section_templates

class TemplateHandler(BaseHandler):
    """
    Class for handling templates.
    """

    def __init__(self, section_type):
        """
        Initialize the TemplateHandler.

        Parameters:
            section_type (str): The type of section for which templates need to be handled.
        """
        super().__init__(section_type)

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
        if section_type not in section_templates.keys():
            raise ValueError(
                f'This section type: "{section_type}" is not supported.\
                \nAvailable supported sections are: {list(section_templates.keys())}'
            )
        self.__section_template = section_templates.get(section_type)

    def get_templates(self):
        """
        Get templates from the section template.

        Returns:
            List[str]: List of templates extracted from the section template.
        """
        templates = []
        for template_info in self._section_template[0].items():
            clean_template_info = clean_template(template_info)
            template = clean_template_info[1][1]
            templates.append(template)
        return templates

    def get_summaries(self):
        """
        Get summaries from the section template.

        Returns:
            List[str]: List of summaries extracted from the section template.
        """
        summaries = []
        for template_info in self._section_template[0].items():
            clean_template_info = clean_template(template_info)
            summary = clean_template_info[1][0]
            summaries.append(summary)
        return summaries

    def get_template_data(self):
        """
        Get data including summaries and templates from the section template.

        Returns:
            List[Dict[str, str]]: List of dictionaries containing the summary and template data.
        """
        templates_data = []
        templates = self.get_templates()
        summaries = self.get_summaries()

        for summary, template in zip(summaries, templates):
            templates_data.append({"summary": summary, "template": template})
        return templates_data
