'''Module for filling fields into text using llm'''

from typing import Dict, List
import json
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


class AutoFillTemplate():
    '''
    class for filling fields in template
    '''

    def __init__(self, model_name='str'):
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY")
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
