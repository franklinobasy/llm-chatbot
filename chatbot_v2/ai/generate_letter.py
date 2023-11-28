'''Module for generating letter using llm'''


import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from chatbot_v2.templates.context_config import LETTER_SYSTEM_PROMPT


class AutoWriteLetter:
    '''
    class fo generating formal letter
    '''

    def __init__(self, model_name='str'):
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            cache=True
        )

    def generate(self, context):
        messages = [
            SystemMessage(
                content=LETTER_SYSTEM_PROMPT
            ),
            HumanMessage(
                content=f"context: {context}"
            ),
        ]

        result = self.llm(messages)
        return result.content
