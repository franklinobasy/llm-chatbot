"""
Module: base_handler.py

Abstract base class for section handlers.

Classes:
    - BaseHandler: Abstract base class for section handlers.

Attributes:
    - section_templates (Dict[str, str]): Dictionary containing section templates indexed by section type.

"""

from abc import ABC, abstractmethod, abstractproperty
from chatbot_v2.templates.templates import section_templates

class BaseHandler(ABC):
    """
    Abstract base class for section handlers.
    """

    def __init__(self, section_type: str):
        """
        Initialize the BaseHandler.

        Parameters:
            section_type (str): Type of section.
        
        Raises:
            ValueError: If the provided section type is not supported.
        """
        if section_type not in section_templates.keys():
            raise ValueError(
                f'This section type: "{section_type}" is not supported.\
                \nAvailable supported sections are: {list(section_templates.keys())}'
            )
        self._section_template = section_templates.get(section_type)

    @abstractproperty
    def section(self):
        """
        Abstract property for accessing the section.
        """
        pass
