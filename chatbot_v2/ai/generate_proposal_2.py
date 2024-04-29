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
from chatbot_v2.handlers.question_handler import QuestionHandler
from chatbot_v2.handlers.template_handler import TemplateHandler
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

    def __init__(self, model_name: str, section_type: str):
        """
        Initialize the AutoGenerateSection class.

        Parameters:
            model_name (str): The name of the language model to use.
            section_type (str): The type of the proposal section to generate.
        """
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            cache=True,
            streaming=True,
        )
        self.section_type = section_type
        self.no_llm_sections = [
            "about_cyphercrescent",
            "our_team",
            "our_commitment",
            "our_clients",
        ]

    SYSTEM_PROMPT = """
    You are a professional proposal writer that works in Cycphercrescent.
    Cyphercrscent mission is to co-create innovative technology solutions
    for enterprises to accelerate adoption of sustainable digitalisation
    practices.
    
    You role is to write a particular section of a proposal.
    Do not include any conclusion after writing the section.
    """

    HUMAN_PROMPT = """
    You are expected to write only a section of the proposal.
    The name of the section is {section_type}.
    
    A list of questions has been given below, followed by a template example
    of how the proposal section shoud be. A context will be provided to help you
    answer the questions. Note that answering the questions will help you
    with more information on how to write the section of the proposal.
    
    if no question is supplied, or/and no template is supplied, feel free
    to generate the template using the context provided.
    
    NOTE: You are expected to only write the specified section of the proposal.
    Do not include any conclusion after writing the section.
    You are free to get creative with the generation of the section whether template
    was provided or not using the given context. If you have a list of template, you
    can choose to work the ost suitable template
    
    CONTEXT:
    {context}
    
    QUESTIONS:
    {questions}
    
    TEMPLATE(S):
    {template}
    """

    def section_template(self, index=-1):
        """
        Set the template for the proposal section.

        Parameters:
            index (int): The index of the template to use. Default is -1 for all templates.
        """
        th = TemplateHandler(self.section_type)
        ts = th.get_templates()
        if index != -1:
            if index >= len(ts):
                raise IndexError("Index out of range for template list")
        self.ts: Union[List, str] = ts if index == -1 else ts[index]

    def template_questions(self):
        """Get the questions related to the proposal section."""
        qh = QuestionHandler(self.section_type)
        self.qs = qh.get_questions()

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
            questions=self.qs,
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
            questions=self.qs,
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
            return self.stream_section_generation
        else:
            return self.generate_section_2

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
