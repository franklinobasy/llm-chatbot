from chatbot_v2.ai.generate_proposal import AutoFillTemplate
from chatbot_v2.handlers.question_handler import QuestionHandler
from chatbot_v2.handlers.template_handler import TemplateHandler
from chatbot_v2.handlers.field_handler import FieldHandler


introQ = QuestionHandler("introduction")
questions = introQ.get_questions()
answers = [
    input(f"{i}). " + question + ": ")
    for i, question in enumerate(questions, start=1)
]
questions_answers = introQ.set_answers(answers)

introT = TemplateHandler("introduction")
templates = introT.get_templates()
choosen_template = templates[0]

fh = FieldHandler(choosen_template)
fields = fh.get_fields_from_template()

bot = AutoFillTemplate("gpt-3.5-turbo-0301")
filled_fields = bot.fill_fields(fields, questions_answers)

introduction = fh.fill_template(filled_fields)
print(introduction)
