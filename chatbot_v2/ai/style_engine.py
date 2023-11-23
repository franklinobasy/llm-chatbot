import os
import glob
from typing import List, Dict
from pydantic import BaseModel, Field
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema.messages import SystemMessage
from langchain.output_parsers import PydanticOutputParser
from dotenv import load_dotenv

from chatbot_v2.configs.constants import MODEL_NAME

# Load .env file
load_dotenv()

# Accessing variables
API_KEY = os.getenv("OPENAI_API_KEY")

## define the output schema
class StyleGuideParser(BaseModel):
    corrected_text: str = Field(
        description="Suggest a simple modification/correction for \
            the input,keep the corrected text precise as close as \
            possible to the input. DO NOT make up additional text"
    )
    explanation: None | Dict[str, str | List[str]] = Field(
        description="""In this field, several language style guide \
            context headers will be provided, you will return a \
            dictionary output as follows.
            Keys: You most only list the provided context headers \
            that were found applicable for editing and modifying \
            the given input, DO NOT mention any header that was \
            not found applicable for corrections.
            Values: As values carefully explain under each context \
            header that was found applicable, the different rules \
            that was considered while making the corrections to provide \
            the user with a rational explanation for your corrections."""
    )


class StyleGuide:
    def __init__(self):
        self.file_contents = None
        self.load_files()

    def read_style_guide_files(self, path: List[str]) -> Dict[str, str]:
        file_contents = {file_path.split("\\")[-1]: open(file_path, "r", encoding='utf8').read() for file_path in path}
        return file_contents

    def load_files(self) -> None:
        if self.file_contents is None:
            file_path = glob.glob(
                "data/style_guide/*.txt"
            )
            self.file_contents = self.read_style_guide_files(file_path)

    def generate_chat_template(self) -> str:
        ellipses = self.file_contents[
            "ELLIPSES (…).txt"
        ]
        alphabetisation = self.file_contents[
            "ALPHABETISATION.txt"
        ]
        dashes = self.file_contents[
            "DASHES AND HYPHENS.txt"
        ]
        bulleting = self.file_contents[
            "BULLETED AND NUMBERED LISTS.txt"
        ]
        ampersand = self.file_contents[
            "AMPERSANDS (&).txt"
        ]
        dates_time = self.file_contents[
            "DATES AND TIMES.txt"
        ]
        quotation = self.file_contents[
            "QUOTATION MARKS.txt"
        ]
        brackets = self.file_contents[
            "BRACKETS () [].txt"
        ]
        foreign_words = self.file_contents[
            "FOREIGN WORDS.txt"
        ]
        gender = self.file_contents[
            "GENDER AND INCLUSIVE LANGUAGE.txt"
        ]
        slashes = self.file_contents[
            "SLASHES.txt"
        ]
        spellings = self.file_contents[
            "SPELLINGS.txt"
        ]
        business_emails = self.file_contents[
            "BASICS OF A BUSINESS EMAIL.txt"
        ]
        acronyms = self.file_contents[
            "ACRONYMS.txt"
        ]
        capitalization = self.file_contents[
            "CAPITALISATION.txt"
        ]
        full_stops = self.file_contents[
            "FULL STOPS (.).txt"
        ]
        apostrophies = self.file_contents[
            "APOSTROPHES.txt"
        ]
        money = self.file_contents[
            "MONEY.txt"
        ]
        abbreviation = self.file_contents[
            "ABBREVIATIONS, TITLES, AND CONTRACT.txt"
        ]
        figures_tables = self.file_contents[
            "FIGURES AND TABLES.txt"
        ]
        numbers = self.file_contents[
            "NUMBERS.txt"
        ]
        commas = self.file_contents[
            "COMMAS (,).txt"
        ]
        parallelism = self.file_contents[
            "PARALLELISM.txt"
        ]
        colons = self.file_contents[
            "COLONS AND SEMICOLONS.txt"
        ]
        contacts = self.file_contents[
            "CONTACT DETAILS.txt"
        ]

        guide_template_context = """ 

        "# CONTEXT HEADERS": Here are different style guide context hearders for consideration

        "dates_time context"
        {dates_time_context}

        "quotation context"
        {quotation_context}

        "brackets context"
        {brackets_context}

        "foreign_words context"
        {foreign_words_context}

        "gender context"
        {gender_context}

        "slashes context"
        {slashes_context}

        "business_emails context"
        {business_emails_context}

        "acronyms context"
        {acronyms_context}

        "spellings context" 
        {spellings_context}

        "capitalization context"
        {capitalization_context}

        "full_stops context"
        {full_stops_context}

        "apostrophies context"
        {apostrophies_context}

        "money context"
        {money_context}

        "abbreviation context"
        {abbreviation_context}

        "numbers context"
        {numbers_context}

        "commas context"
        {commas_context}

        "colons context"
        {colons_context}

        "contacts context"
        {contacts_context}

        "ellipses context"
        {ellipses_context}

        "dashes context"
        {dashes_context}

        "bulleting context"
        {bulleting_context}

        "parallelism context"
        {parallelism_context}

        "figures_tables context"
        {figures_tables_context}

        "ampersand context"
        {ampersand_context}
        
        "alphabetisation context"
        {alphabetisation_context}
        """.format(
            alphabetisation_context=alphabetisation,
            parallelism_context=parallelism,
            figures_tables_context=figures_tables,
            ampersand_context=ampersand,
            ellipses_context=ellipses,
            dashes_context=dashes,
            bulleting_context=bulleting,
            dates_time_context=dates_time,
            quotation_context=quotation,
            brackets_context=brackets,
            foreign_words_context=foreign_words,
            gender_context=gender,
            slashes_context=slashes,
            business_emails_context=business_emails,
            acronyms_context=acronyms,
            spellings_context=spellings,
            capitalization_context=capitalization,
            full_stops_context=full_stops,
            apostrophies_context=apostrophies,
            money_context=money,
            abbreviation_context=abbreviation,
            numbers_context=numbers,
            commas_context=commas,
            colons_context=colons,
            contacts_context=contacts,
        )

        return guide_template_context

    def styleguide_modify_input(self):  # , input_query: str
        # import styleguide context

        chat_model = ChatOpenAI(model=MODEL_NAME, temperature=0, api_key=API_KEY)

        parser = PydanticOutputParser(pydantic_object=StyleGuideParser)
        format_instructions = parser.get_format_instructions()
        style_guide_context = self.generate_chat_template()
        human_style_context = (
            """
        You are a Language Engine, you are tasked with validating, correcting, and interpreting user mistakes in a text inputs, in accordance with a set of intructions provided in an editorial style guide manual.
        {format_instructions}
        """
            + style_guide_context
            + """
        "INPUT": {input}
        "OUTPUT":
        """
        )
        system_template = SystemMessage(
            content=(
                """You are an intelligent Language engine, you will provide helpful language related corrections.
                Your default language is British English, all spellings must be in British English"""
            )
        )

        ## chat template
        chat_prompt_template = ChatPromptTemplate(
            messages=[
                system_template,
                HumanMessagePromptTemplate.from_template(human_style_context),
            ],
            input_variables=["input"],
            partial_variables={"format_instructions": format_instructions},
        )

        # chat_response = chat_model(query_window1.to_messages())
        # chat_result = parser.parse(chat_response.content)
        # modified_text: str = chat_result.corrected_text
        # explanation: dict[str, str | list[str]] | None = chat_result.explanation

        chain = chat_prompt_template | chat_model | parser
        # chain_output = chain.invoke({"input": input_query})
        return chain  # modified_text, explanation


if __name__ == "__main__":
    user_input = """
    hello mister james

    i am doctor martins, here are some of my request

    1. color is yellow
    b. 100000000 naira should be added to the sum of 2 million naira
    """
    style_guide = StyleGuide()
    chain_result = style_guide.styleguide_modify_input()
    # modified_text, _ = style_guide.styleguide_modify_input(user_input)

    # corrected_text, explanation = process_user_input(user_input)
    response_data = (
        chain_result if isinstance(chain_result, dict) else chain_result.dict()
    )
    f = open("text.json", "w", encoding='utf8')
    print(response_data, file=f)
    f.close()
    # print('\n')
    # print(output.explanation)
