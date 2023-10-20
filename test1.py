from chatbot_v2.ai.generate_proposal import AutoFillTemplate
from chatbot_v2.handlers.question_handler import QuestionHandler
from chatbot_v2.handlers.template_handler import TemplateHandler
from chatbot_v2.handlers.field_handler import FieldHandler


model_name = "gpt-3.5-turbo-0301"
section = "introduction"

# Question Section
introQ = QuestionHandler(section)

# # Get questions required to provide context for llm
questions = introQ.get_questions()

# # Ask the user the questions and store the answers
# # provide by th user in answers list
answers = [
    input(f"{i}). " + question + ": ")
    for i, question in enumerate(questions, start=1)
]

# # Combine the questions and answers in a dictionary
questions_answers = introQ.set_answers(answers)

# Template section
introT = TemplateHandler(section)

# # Get all available templates for the introduction
templates = introT.get_templates()

# # The first template was choosen
choosen_template = templates[0]

# Field selection section
fh = FieldHandler(choosen_template)

# # Get all the fiels in the selected template
fields = fh.get_fields_from_template()

# LLM section
bot = AutoFillTemplate(model_name)

# using the questions, answers and the field, the bot
# is used to fill the fields with the appropriate answers
# and stores the result in a dictionary
filled_fields = bot.fill_fields(fields, questions_answers)

# the filled fields are inserted into the template
introduction = fh.fill_template(filled_fields)
print(introduction)
