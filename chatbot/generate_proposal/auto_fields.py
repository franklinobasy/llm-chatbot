'''
This modules contains classes that leverages LLM to
extract fields from texts
'''

import dotenv
import json
import os

from chatbot.generate_proposal.extractor import TextExtractor
from chatbot.generate_proposal.prompts import get_fields_prompt
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


dotenv.load_dotenv()


class AutoField:
    '''
    class for getting fields from text
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

    def clean_extracted_fields(self, text):
        text = text.replace('\n', '')
        text = text.replace('    ', '')
        text = text.replace('\'', '"')
        d = json.loads(text)
        for k, v in d.items():
            if v == 'str':
                d[k] = str()
            elif v == 'list':
                d[k] = list()
        return d

    def get_fields(self):
        if not hasattr(self, "text"):
            raise ValueError("No text has been loaded yet!")

        messages = [
            SystemMessage(
                content=get_fields_prompt
            ),
            HumanMessage(
                content=f"{self.text}"
            ),
        ]

        result = self.llm(messages)
        return self.clean_extracted_fields(result.content)
