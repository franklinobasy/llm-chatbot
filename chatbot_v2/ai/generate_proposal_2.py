'''Module for proposal auto-generation'''

from typing import Dict, List
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from chatbot_v2.handlers.question_handler import QuestionHandler
from chatbot_v2.handlers.template_handler import TemplateHandler

# Remove unnecessary imports: json, logging, and duration (if not used elsewhere)

class AutoGenerateSection:
    def __init__(self, model_name: str, section_type: str):
        self.__model_name = model_name
        self.llm = ChatOpenAI(
            model=self.__model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            cache=True
        )
        self.section_type = section_type

    SYSTEM_PROMPT = '''
    You are a professional proposal writer that works in Cycphercrescent.
    Cyphercrscent mission is to co-create innovative technology solutions
    for enterprises to accelerate adoption of sustainable digitalisation
    practices.
    '''

    HUMAN_PROMPT = '''
    You are expected to write of a section of the proposal.
    The name of the section is {section_type}.
    
    A list of questions has been given below, followed by a template example
    of how the proposal section shoud be. A context will be provided to help you
    answer the questions. Note that answering the questions will help you
    with more information on how to write the section of the proposal.
    
    if no question is supplied, or/and no template is supplied, feel free
    to generate the template using the context provided.
    
    NOTE: You are expected to only write the specified section of the template.
    You are free to get creative with the generation of the section whether template
    was provided or not using the given context. If you have a list of template, you
    can choose to work with the most appropriate
    
    CONTEXT:
    {context}
    
    QUESTIONS:
    {questions}
    
    TEMPLATE:
    {template}
    '''

    def section_template(self, index=-1):
        th = TemplateHandler(self.section_type)
        ts = th.get_templates()
        if index != -1:
            if index >= len(ts):
                raise IndexError("Index out of range for template list")
        self.ts: List = ts if index == -1 else ts[index]

    def template_questions(self):
        qh = QuestionHandler(self.section_type)
        self.qs = qh.get_questions()


    def generate_section(self, context):
        prompt = self.HUMAN_PROMPT.format(
            section_type=self.section_type,
            context=context,
            questions=self.qs,
            template=self.ts
        )

        messages = [
            SystemMessage(
                content=self.SYSTEM_PROMPT
            ),
            HumanMessage(
                content=prompt
            ),
        ]

        result = self.llm(messages)
        return result.content
    
    def generate_section_2(self, context):
        prompt = self.HUMAN_PROMPT.format(
            section_type=self.section_type,
            context=context,
            questions=self.qs,
            template=self.ts
        )

        messages = [
            SystemMessage(
                content=self.SYSTEM_PROMPT
            ),
            HumanMessage(
                content=prompt
            ),
        ]

        for chunck in self.llm.stream(input=messages):
            yield chunck.content
