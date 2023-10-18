from chatbot_v2.ai.generate_proposal import AutoFillTemplate
from chatbot_v2.handlers.question_handler import QuestionHandler
from chatbot_v2.handlers.template_handler import TemplateHandler


introQ = QuestionHandler("introduction")
questions = introQ.get_questions()
answers = [
    input(f"{i}). " + question + ": ")
    for i, question in enumerate(questions, start=1)
]
questions_answers = introQ.set_answers(answers)

introT = TemplateHandler("introduction")
templates = introT.get_template_data()

prompt = '''
You are an AI bot specialized at writing proposal for My company - Cyphercrescent.
You are expected to read and understand the questions and
answer provided in the python list. Then from the understanding
gained, you are expected to choose from the available templates in
the second python lists provided, and fill the fields enclosed within square brackets in templates with the
understanding gained from the questions and answer.

NOTE: You are expected to choose and fill from the templates the most suitable that
best fits the questions and answers given.Fill only the options in the square brackets of the chosen template.Make sure to trictly follow the
template you have chosen.
'''

bot = AutoFillTemplate("gpt-3.5-turbo-0301")
result = bot.fill_template(
    "introduction",
    prompt,
    questions_answers,
    templates
)
print()
print(result)
