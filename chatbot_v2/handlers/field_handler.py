"""
Module: field_handler.py

Contains utility functions for handling fields within templates.

Classes:
    - FieldHandler: Class for handling fields within templates.

"""

import re
from typing import Dict, List
from utilities.tools import duration

class FieldHandler:
    """
    Class for handling fields within templates.
    """

    def __init__(self, template: str):
        """
        Initialize the FieldHandler.

        Parameters:
            template (str): The template containing fields.
        """
        self.__template = template

    @duration
    def get_fields_from_template(self) -> List[str]:
        """
        Get fields from the template.

        Returns:
            List[str]: List of fields extracted from the template.
        """
        pattern = r"\[([^\[\]]+)\]"
        matches: List[str] = re.findall(pattern, self.__template)
        matches = [match + "?" for match in matches]
        return matches

    @duration
    def fill_template(self, list_filled_fields: List[Dict]) -> str:
        """
        Fill the template with filled fields.

        Parameters:
            list_filled_fields (List[Dict]): List of dictionaries containing filled fields.

        Returns:
            str: The template with filled fields.
        """
        filled_fields = {}

        for item in list_filled_fields:
            filled_fields[item["question"]] = item["answer"]

        filled_fields = list(filled_fields.values())
        pattern = r"\[([^\[\]]+)\]"

        def repl(match):
            """
            Replacement function for filling fields in the template.

            Parameters:
                match (re.Match): The matched field.

            Returns:
                str: The replacement string.
            """
            nonlocal filled_fields
            if filled_fields:
                replacement = filled_fields.pop(0)
                return "[" + replacement + "]"
            else:
                return match.group(0)  # If field not found, keep it as is

        filled_template = re.sub(pattern, repl, self.__template)
        return filled_template
