from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

import os
from chatbot_v2.configs.constants import MODEL_NAME

from chatbot_v2.nda.templates import NDA
from utilities.tools import duration


templates = NDA()


class GenerateNDA:
    def __init__(self, model_name=MODEL_NAME, answers=None):
        questions = templates.prepare_questions()
        if len(questions) != len(answers):
            raise ValueError(f"Number of answers supplied mismatch number of questions")
        self.questions_answers = {
            question:answer for question, answer in zip(questions, answers)
        }
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            cache=True
        )
    
    @duration
    def handle_section(self, section, context):
        PROMPT = f'''
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
        '''
        
        messages = [
            SystemMessage(
                content=PROMPT
            ),
            HumanMessage(
                content=f"context: {context}"
            ),
        ]

        result = self.llm(messages)
        return result.content
    
    @duration
    def handle_sections(self):
        context = "Use the questions and answers supplied to edit the text."
        sections = templates.prepare_sections()
        sections[0] = self.handle_section(sections[0], context)
        sections[1] = self.handle_section(sections[1], context)
        sections[3] = self.handle_section(sections[3], context)

        return "\n".join(sections)

    @duration
    def handle_sections_2(self, chunk_size=500):
        context = "Use the questions and answers supplied to edit the text."
        sections = templates.prepare_sections()
        sections[0] = self.handle_section(sections[0], context)
        sections[1] = self.handle_section(sections[1], context)
        sections[3] = self.handle_section(sections[3], context)
        
        text = "\n".join(sections)
        
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        for chunk in chunks:
            yield chunk
