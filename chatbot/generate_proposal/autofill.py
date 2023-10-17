'''Module for filling fields into text using llm'''

from typing import List
import json
import os

from chatbot.generate_proposal.extractor import TextExtractor
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


class AutoFill():
    '''
    class for filling fields with text
    '''

    def __init__(self, model_name='str'):
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    def get_text(self):
        text_extractor = TextExtractor()
        text_extractor.load_file("data/template1.txt")
        self.text = text_extractor.get_text_file()

    def fill_text(self, context):
        if not hasattr(self, "text"):
            raise ValueError("No text has been loaded yet!")

        messages = [
            SystemMessage(
                content=f"Assume the role of a proposal writer. Use the context and template provided to write a good proposal"
            ),
            HumanMessage(
                content=f"context: {context}, template: {self.text}"
            ),
        ]

        result = self.llm(messages)
        return result.content


class AutoFillField():
    '''
    class for filling fields with answers
    '''

    def __init__(self, fields: List[str], model_name='str'):
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.fields = fields

    def set_context(self, context):
        self.context = context

    def prepare_prompt(self):
        prompt = '''
        Your job is to use the context as a guide to provide answers to each
        question in the python list. Your are expected find the best suitable
        answers for each question. Each question appears as keys in the dictionary

        Note:
        Use the format below as output:{"question": "answer",...}
        '''

        return prompt

    def fill_fields(self):
        prompt = self.prepare_prompt()
        messages = [
            SystemMessage(
                content=prompt
            ),
            HumanMessage(
                content=f"context: {self.context}, python list: {self.fields}"
            ),
        ]

        result = self.llm(messages)
        return json.loads(result.content)
