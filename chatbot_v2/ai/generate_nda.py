"""
Module: generate_nda.py

Module for generating Non-Disclosure Agreements (NDAs) using language models.

Classes:
    - GenerateNDA: A class for generating NDAs.

Functions:
    - handle_section: Handle a single section of the NDA synchronously.
    - handle_sections: Handle all sections of the NDA synchronously.
    - handle_sections_2: Handle all sections of the NDA asynchronously with streaming.
"""

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
from chatbot_v2.configs.constants import MODEL_NAME
from chatbot_v2.nda.templates import NDA
from utilities.tools import duration

templates = NDA()


class GenerateNDA:
    """
    GenerateNDA class for generating Non-Disclosure Agreements (NDAs).

    Attributes:
        model_name (str): The name of the language model to use.
        questions_answers (dict): A dictionary containing questions and their corresponding answers.
        llm (ChatOpenAI): The ChatOpenAI instance for generating NDAs.
    """

    def __init__(self, model_name=MODEL_NAME, answers=None):
        """
        Initialize the GenerateNDA class.

        Parameters:
            model_name (str): The name of the language model to use. Default is the value from constants.
            answers (list): A list of answers to the NDA questions. Must match the number of questions.
        """
        questions = templates.prepare_questions()
        if len(questions) != len(answers):
            raise ValueError(
                "Number of answers supplied mismatch number of questions")
        self.questions_answers = {
            question: answer for question, answer in zip(questions, answers)
        }
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            cache=True,
        )

    @duration
    def handle_section(self, section, context):
        """
        Handle a single section of the NDA synchronously.

        Parameters:
            section (str): The text of the section to handle.
            context (str): The context or additional information for handling the section.

        Returns:
            str: The edited text of the section.
        """
        PROMPT = f"""
        Your job is to use the questions and answers given below
        to edit and rewrite the given text:

        Note that the output must contain only the edited Text.
        if there is nothing to edit, return only the original Text.
        
        The questions and answer below are meant to replace every
        information about XYZ, because XYZ is just a place holder.

        Questions and Answers:
        {self.questions_answers}

        Text:
        {section}
        """

        messages = [
            SystemMessage(content=PROMPT),
            HumanMessage(content=f"context: {context}"),
        ]

        result = self.llm(messages)
        return result.content

    @duration
    def handle_sections(self):
        """
        Handle all sections of the NDA synchronously.

        Returns:
            str: The edited text of all sections combined.
        """
        context = "Use the questions and answers supplied to edit the text."
        sections = templates.prepare_sections()
        sections[0] = self.handle_section(sections[0], context)
        sections[1] = self.handle_section(sections[1], context)
        sections[3] = self.handle_section(sections[3], context)

        return "\n".join(sections)

    @duration
    def handle_sections_2(self, chunk_size=500):
        """
        Handle all sections of the NDA asynchronously with streaming.

        Parameters:
            chunk_size (int): The size of each chunk of text to yield. Default is 500.

        Yields:
            str: A chunk of the edited text of all sections.
        """
        context = "Use the questions and answers supplied to edit the text."
        sections = templates.prepare_sections()
        sections[0] = self.handle_section(sections[0], context)
        sections[1] = self.handle_section(sections[1], context)
        sections[3] = self.handle_section(sections[3], context)

        text = "\n".join(sections)

        chunks = [text[i: i + chunk_size]
                  for i in range(0, len(text), chunk_size)]
        for chunk in chunks:
            yield chunk
