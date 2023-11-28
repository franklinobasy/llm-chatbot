from chatbot_v2.templates.templates import create_section, create_question
from chatbot_v2.templates.dynamic_template_search import files_for_section

import os


BASE_PATH = os.path.join(
    os.getcwd(), "data", "NDA", "NDA_templates"
)


class NDA:
    def __init__(self, base_path=BASE_PATH):
        self.base_path = base_path
    
    def prepare_sections(self):
        section_names = [
            f"section_{i}"
            for i in range(1, 5)
        ]
        
        raw_sections = [
            create_section(section_name, "", base_path=self.base_path)
            for section_name in section_names
        ]
        
        sections = []
        for section in raw_sections:
            sections += [section['1'][-1]]
        
        return sections
    
    def prepare_questions(self):
        section_names = [
            f"section_{i}"
            for i in range(1, 5)
        ]
        
        raw_questions = [
            create_question(section_name, base_path=self.base_path)
            for section_name in section_names
        ]
        
        questions = []
        
        for item in raw_questions:
            for qs in list(item.values()):
                questions += qs.split("\n")
        
        questions = list(filter(lambda x: x, questions))
        
        return questions
