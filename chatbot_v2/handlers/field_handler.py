import re
from typing import Dict, List

from utilities.tools import duration


class FieldHandler:
    def __init__(self, template: str):
        self.__template = template

    @duration
    def get_fields_from_template(self):
        pattern = r'\[([^\[\]]+)\]'
        matches: List[str] = re.findall(pattern, self.__template)
        matches = [match + '?' for match in matches]
        return matches
    @duration
    def fill_template(self, list_filled_fields: List):
        filled_fields = {}
        
        for item in list_filled_fields:
            filled_fields[item["question"]] = item["answer"]

        filled_fields = list(filled_fields.values())
        pattern = r'\[([^\[\]]+)\]'

        def repl(match):
            nonlocal filled_fields
            if filled_fields:
                replacement = filled_fields.pop(0)
                return '[' + replacement + ']'
            else:
                return match.group(0)  # If field not found, keep it as is

        filled_template = re.sub(pattern, repl, self.__template)
        return filled_template
