from typing import Dict
from chatbot_v2.templates.templates import (
    clean_question,
)
from chatbot_v2.handlers.base_handler import (
    BaseHandler,
    section_templates
)


class QuestionHandler(BaseHandler):
    def __init__(self, section_type):
        super().__init__(section_type)
        self.__answered_questions = list()

    @property
    def section(self):
        return self._section_template

    @section.setter
    def section(self, section_type: str):
        if section_type not in section_templates.keys():
            raise ValueError(
                f"This section type: \"{section_type}\" is not supported.\
                \nAvailable supported sections are: {section_templates.keys()}"
            )
        self.__section_template = section_templates.get(section_type)

    def get_questions(self):
        try:
            questions: Dict[str, str] = self._section_template[1]
            questions_to_use = [
                clean_question(question)[1] for question in questions.items()
            ]
        except IndexError as e:
            questions_to_use = []

        return questions_to_use

    def set_answers(self, answers):
        if len(answers) != len(self.get_questions()):
            raise ValueError(
                f"The answers must match all the questions: {len(answers)}\
                    answers, {len(self.get_questions())} questions"
            )
        self.__answered_questions = list()

        for question, answer in zip(self.get_questions(), answers):
            item = {}
            item["question"] = question
            item["answer"] = answer
            self.__answered_questions.append(item)

        return self.__answered_questions
