"""
Module: generate_proposal.py

Module for filling fields into text using LLM (Large Language Model).

Classes:
    - AutoFillTemplate: A class for filling fields in a template.

Functions:
    - fill_template: Fill fields in a template synchronously.
    - fill_fields: Fill fields in a template asynchronously with streaming.
"""

from typing import Dict, List
import json
import os

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from utilities.tools import duration

response_schema = [
    ResponseSchema(name="question", description="This is the question asked"),
    ResponseSchema(
        name="answer", description="This is the answer you provided"),
]

output_parser = StructuredOutputParser.from_response_schemas(response_schema)
format_instructions = output_parser.get_format_instructions()


class AutoFillTemplate:
    """
    AutoFillTemplate class for filling fields in a template.

    Attributes:
        model_name (str): The name of the language model to use.
        llm (ChatOpenAI): The ChatOpenAI instance for filling fields.
    """

    def __init__(self, model_name="str"):
        """
        Initialize the AutoFillTemplate class.

        Parameters:
            model_name (str): The name of the language model to use.
        """
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            cache=True,
        )

    def fill_template(
        self,
        section_type,
        prompt: str,
        questions_answers: List[Dict],
        templates: List[Dict],
    ):
        """
        Fill fields in a template synchronously.

        Parameters:
            section_type (str): The type of the proposal section to generate.
            prompt (str): The prompt or instruction for filling the template.
            questions_answers (List[Dict]): List of questions and answers.
            templates (List[Dict]): List of template options.

        Returns:
            str: The filled template.
        """
        extra_info = f'The template provided is strictly for {section_type} section of the proposal. You are expected to only write the {section_type} part of the proposal. Include "{section_type}" as title. Indicate the index of the template that was chosen.'
        messages = [
            SystemMessage(content=prompt + extra_info),
            HumanMessage(
                content=f"Questions and Answers: \n{questions_answers},\n\nTemplates: \n{templates}"
            ),
        ]

        result = self.llm(messages)
        return result.content

    @duration
    def fill_fields(self, fields: List[str], questions_answers: List[Dict]):
        """
        Fill fields in a template asynchronously with streaming.

        Parameters:
            fields (List[str]): List of fields to fill in the template.
            questions_answers (List[Dict]): List of questions and answers.

        Returns:
            Dict: The filled fields as a dictionary.
        """
        template_string = """
        We want to create a proposal using provided fill in the blank template.
        Your job is to use the context as a guide to provide answers to each
        question in the Python list. Your are expected to find the best suitable
        answers for each question.

        Note:
        Use the format below strictly as output because the output is only
        need as a Python dictionary, no trailing commas at the end of the dictionary:

        Output Format:
        {format_instructions}
        
        Wrap your final output with closed and open brackets (a list of JSON objects)
        
        """

        prompt = ChatPromptTemplate(
            messages=[HumanMessagePromptTemplate.from_template(
                template_string)],
            partial_variables={"format_instructions": format_instructions},
        )

        messages_for_list_prompt = prompt.format_messages(
            format_instructions=format_instructions
        )

        result = self.llm(messages_for_list_prompt)
        return json.loads(result.content)
