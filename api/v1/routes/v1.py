#!/bin/python3
from fastapi import APIRouter

from api.v1.models.model import (
    LetterContext,
    LetterResult,
    ProposalResult,
    Questions,
    Sections,
    Templates,
    UserInput,
)
from api.v1.routes.error_handler import (
    AnswersMisMatchQuestion,
    PathTypeMisMatch,
    UnknownSectionID,
    UnknownSectionName,
    UnknownTemplateID
)
from chatbot_v2.ai.generate_proposal import AutoFillTemplate
from chatbot_v2.ai.generate_letter import AutoWriteLetter
from chatbot_v2.handlers.field_handler import FieldHandler
from chatbot_v2.handlers.question_handler import QuestionHandler
from chatbot_v2.handlers.template_handler import TemplateHandler

from chatbot_v2.templates.templates import (
    section_templates
)


router = APIRouter()
MODEL_NAME = "gpt-3.5-turbo-0301"


@router.get("/sections")
async def get_all_sections():
    return Sections(
        sections=list(section_templates.keys())
    )


@router.get("/questions/{section_id}")
async def get_section_questions(section_id: int):
    if not isinstance(section_id, int):
        raise PathTypeMisMatch(section_id)

    try:
        section_name = list(section_templates.keys())[section_id]
        section = QuestionHandler(section_name)
        questions = section.get_questions()
        return Questions(
            section_name=section_name,
            questions=questions
        )
    except IndexError:
        raise UnknownSectionID(section_id)


@router.get("/templates/{section_id}")
async def get_section_templates(section_id: int):
    if not isinstance(section_id, int):
        raise PathTypeMisMatch(section_id)

    try:
        section_name = list(section_templates.keys())[section_id]
        template_store = TemplateHandler(section_name)
        templates = template_store.get_templates()
        return Templates(
            section_name=section_name,
            templates=templates
        )
    except IndexError:
        raise UnknownSectionID(section_id)


@router.post("/generate")
async def generate_proposal(user_input: UserInput):
    section_name = user_input.section_name
    template_index = user_input.template_index
    answers = user_input.answers

    if section_name not in list(section_templates.keys()):
        raise UnknownSectionName(section_name)

    template_store = TemplateHandler(section_name)

    try:
        template = template_store.get_templates()[template_index]
    except IndexError:
        raise UnknownTemplateID(template_index)

    try:
        question_handler = QuestionHandler(section_name)
        questions_answers = question_handler.set_answers(answers)
    except ValueError:
        raise AnswersMisMatchQuestion(
            n_questions=len(question_handler.get_questions()),
            n_answers=len(answers)
        )

    # Field selection section
    fh = FieldHandler(template)

    # # Get all the fiels in the selected template
    fields = fh.get_fields_from_template()

    # LLM section
    bot = AutoFillTemplate(MODEL_NAME)

    # using the questions, answers and the field, the bot
    # is used to fill the fields with the appropriate answers
    # and stores the result in a dictionary
    filled_fields = bot.fill_fields(fields, questions_answers)

    # the filled fields are inserted into the template
    filled_templates = fh.fill_template(filled_fields)

    return ProposalResult(
        text=filled_templates
    )


@router.post("/letter")
def write_letter(letter_context: LetterContext):
    context = letter_context.context
    llm = AutoWriteLetter(MODEL_NAME)
    generated_letter = llm.generate(context)
    return LetterResult(
        text=generated_letter
    )
