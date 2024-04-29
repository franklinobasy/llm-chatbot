"""
Module: generate_letter.py

Module for generating formal letters using language models.

Classes:
    - AutoWriteLetter: A class for generating formal letters.

Functions:
    - generate: Generate a formal letter synchronously.
    - generate_2: Generate a formal letter asynchronously with streaming.
"""

import os

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from chatbot_v2.templates.context_config import LETTER_SYSTEM_PROMPT
from utilities.tools import duration


class AutoWriteLetter:
    """
    AutoWriteLetter class for generating formal letters.

    Attributes:
        model_name (str): The name of the language model to use.
        llm (ChatOpenAI): The ChatOpenAI instance for generating letters.
    """

    def __init__(self, model_name="str"):
        """
        Initialize the AutoWriteLetter class.

        Parameters:
            model_name (str): The name of the language model to use. Default is "str".
        """
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            cache=True,
            streaming=True,
        )

    @duration
    def generate(self, context):
        """
        Generate a formal letter synchronously.

        Parameters:
            context (str): The context or content to include in the letter.

        Returns:
            str: The generated formal letter.
        """
        messages = [
            SystemMessage(content=LETTER_SYSTEM_PROMPT),
            HumanMessage(content=f"context: {context}"),
        ]

        result = self.llm(messages)
        return result.content

    @duration
    def generate_2(self, context):
        """
        Generate a formal letter asynchronously with streaming.

        Parameters:
            context (str): The context or content to include in the letter.

        Yields:
            str: A chunk of the generated formal letter.
        """
        messages = [
            SystemMessage(content=LETTER_SYSTEM_PROMPT),
            HumanMessage(content=f"context: {context}"),
        ]

        for chunk in self.llm.stream(input=messages):
            yield chunk.content
