import re
from typing import Dict, List


class FieldHandler:
    def __init__(self, template: str):
        self.__template = template

    def get_fields_from_template(self):
        pattern = r'\[([^\[\]]+)\]'
        matches: List[str] = re.findall(pattern, self.__template)
        matches = [match + '?' for match in matches]
        return matches

    def fill_template(self, filled_fields: Dict):

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
        with open('output2.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(filled_template)
        return filled_template
