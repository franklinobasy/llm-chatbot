'''Module for filling fields into text using llm'''

import logging

from typing import Dict, List
import json
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

from utilities.tools import duration


response_schema = [
    ResponseSchema(
        name="question",
        description="This is the question asked"
    ),
    ResponseSchema(
        name="answer",
        description="This is the answer you provided"
    ),
]


output_parser = StructuredOutputParser.from_response_schemas(response_schema)
format_instructions = output_parser.get_format_instructions()


class AutoFillTemplate():
    '''
    class for filling fields in template
    '''

    def __init__(self, model_name='str'):
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            cache=True
        )

    def fill_template(
        self,
        section_type,
        prompt: str,
        questions_answers: List[Dict],
        templates: List[Dict]
    ):
        extra_info = f"The template provided is strictly for\
            {section_type} section of the proposal. You are\
                expected to only write the {section_type} part of the propoal.\
                    include \"{section_type}\" as title. Indicate the index\
                        of the template that was chosen."
        messages = [
            SystemMessage(
                content=prompt + extra_info
            ),
            HumanMessage(
                content=f"Questions and Answers: \n{questions_answers},\
                    \n\ntemplates: \n{templates}"
            ),
        ]

        result = self.llm(messages)
        return result.content

    @duration
    def fill_fields(self, fields: List[str], quetions_answers: List[Dict]):
        template_string = '''
        We want to create a proposal using provided fill in the blank template.
        Your job is to use the context as a guide to provide answers to each
        question in the python list. Your are expected find the best suitable
        answers for each question.

        Note:
        Use the format below strictly as output because the output is only
        need as a python dictionary,
        no trailing commas at the end of the dictionary:

        Output Format:
        {format_instructions}
        
        Wrap your final output with closed and open brackets (a list of json objects)
        
        '''

        prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(template_string)
            ],
            partial_variables={"format_instructions": format_instructions}
        )
        
        messages_for_list_prompt = prompt.format_messages(format_instructions=format_instructions)

        result = self.llm(messages_for_list_prompt)
        return json.loads(result.content)
