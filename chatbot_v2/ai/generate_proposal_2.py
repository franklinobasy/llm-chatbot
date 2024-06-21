"""
Module: generate_proposal_2.py

Module for auto-generating proposal sections.

Classes:
    - AutoGenerateSection: A class for generating proposal sections.

Functions:
    - section_template: Set the template for the proposal section.
    - template_questions: Get the questions related to the proposal section.
    - generate_section: Generate a proposal section synchronously.
    - generate_section_2: Generate a proposal section asynchronously with streaming.
    - generate_controller: Decide whether to generate the proposal section synchronously or asynchronously.
    - stream_section_generation: Generate the proposal section asynchronously with streaming.
"""

from typing import Dict, List, Union
import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from chatbot_v2.handlers.template_handler import TemplateHandler
from chatbot_v2.templates.domains import DOMAINS, STATIC_SECTIONS
from utilities.tools import duration


class AutoGenerateSection:
    """
    AutoGenerateSection class for generating proposal sections.

    Attributes:
        model_name (str): The name of the language model to use.
        section_type (str): The type of the proposal section to generate.
        llm (ChatOpenAI): The ChatOpenAI instance for generating proposal sections.
        no_llm_sections (List[str]): Sections that do not require the language model.
    """

    def __init__(self, model_name: str, domain:str, section_type: str):
        """
        Initialize the AutoGenerateSection class.

        Parameters:
            model_name (str): The name of the language model to use.
            section_type (str): The type of the proposal section to generate.
        """
        if domain not in DOMAINS.keys():
            raise ValueError(f'Invalid domain: {domain}')
        
        if section_type not in DOMAINS[domain].keys():
            raise ValueError(f'section_type: "{section_type}" not valid for this domain: "{domain}"')
        
        self._domain = domain
        self.section_type = section_type
        
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            cache=True,
            streaming=True,
        )
        
        self.no_llm_sections = STATIC_SECTIONS[self._domain]

    SYSTEM_PROMPT = """
    You are a professional proposal writer that works in Cycphercrescent.
    Cyphercrscent mission is to co-create innovative technology solutions
    for enterprises to accelerate adoption of sustainable digitalisation
    practices.
    
    You role is to write the particular section of a proposal.
    Do not include any conclusion after writing the section.
    """

    HUMAN_PROMPT = """
    You are expected to write only a section of the proposal.
    The section of the proposal you are writing is {section_type}.
    
    Use the provided context to write the section.
    A template has also been provided to give you an example of how
    the section should be.
    
    NOTE: You are expected to only write the specified section of the proposal.
    Do not include any conclusion after writing the section.
    You are free to get creative with the generation of the section whether template
    was provided or not using the given context. If you have a list of template, you
    can choose to work the ost suitable template
    
    CONTEXT:
    {context}
    
    TEMPLATE(S):
    {template}
    """

    def set_template(self):
        """
        Set the template for the proposal section.

        Parameters:
            index (int): The index of the template to use. Default is -1 for all templates.
        """
        th = TemplateHandler(self._domain, self.section_type)
        self.ts = th.get_template()

    def template_hint(self):
        """Get the context related to the proposal section."""
        th = TemplateHandler(self.domain, self.section_type)
        return th.get_hint()

    @duration
    def generate_section(self, context):
        """
        Generate a proposal section synchronously.

        Parameters:
            context (str): The context or additional information for generating the section.

        Returns:
            str: The generated proposal section.
        """
        prompt = self.HUMAN_PROMPT.format(
            section_type=self.section_type,
            context=context,
            template=self.ts,
        )

        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        result = self.llm(messages)
        return result.content

    @duration
    def generate_section_2(self, context):
        """
        Generate a proposal section asynchronously with streaming.

        Parameters:
            context (str): The context or additional information for generating the section.

        Yields:
            str: A chunk of the generated proposal section.
        """
        prompt = self.HUMAN_PROMPT.format(
            section_type=self.section_type,
            context=context,
            template=self.ts,
        )

        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        for chunk in self.llm.stream(input=messages):
            yield chunk.content

    @duration
    def generate_controller(self, context=None, chunk_size=10):
        """
        Decide whether to generate the proposal section synchronously or asynchronously.

        Parameters:
            context (str): The context or additional information for generating the section.
            chunk_size (int): The size of each chunk of text to yield. Default is 10.

        Returns:
            function: The function for generating the proposal section.
        """
        if self.section_type in self.no_llm_sections:
            return self.stream_section_generation(chunk_size)
        else:
            return self.generate_section_2(context)

    @duration
    def stream_section_generation(self, chunk_size):
        """
        Generate the proposal section asynchronously with streaming.

        Parameters:
            chunk_size (int): The size of each chunk of text to yield.

        Yields:
            str: A chunk of the generated proposal section.
        """
        text = self.ts
        chunks = [text[i: i + chunk_size]
                  for i in range(0, len(text), chunk_size)]
        for chunk in chunks:
            yield chunk
