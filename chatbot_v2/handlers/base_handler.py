from abc import ABC, abstractmethod, abstractproperty
from chatbot_v2.templates.templates import (
    section_templates
)


class BaseHandler(ABC):
    def __init__(self, section_type: str):
        if section_type not in section_templates.keys():
            raise ValueError(
                f"This section type: \"{section_type}\" is not supported.\
                \nAvailable supported sections are: {list(section_templates.keys())}"
            )
        self._section_template = section_templates.get(section_type)

    @abstractproperty
    def section(self):
        pass
