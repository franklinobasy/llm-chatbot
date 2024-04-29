"""
Module: style_engine.py

Module for language style correction and interpretation based on an editorial style guide manual.

Classes:
    - StyleGuideParser: Pydantic BaseModel for parsing style guide suggestions.
    - StyleGuideParserV2: Pydantic BaseModel for parsing style guide suggestions (alternate version).
    - StyleGuide: A class for generating and managing style guide information.

Functions:
    - styleguide_modify_input: Modify input text based on style guide suggestions.
"""


import os
import glob
from typing import Any, List, Dict
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage
from langchain.output_parsers import PydanticOutputParser
from chatbot_v2.configs.constants import MODEL_NAME


class StyleGuideParser(BaseModel):
    """
    Pydantic BaseModel for parsing style guide suggestions.

    Attributes:
        corrected_text (str): Suggested correction for the input text.
        explanation (Dict[str, Union[str, List[str]]]): Explanation for the correction under different context headers.
    """
    corrected_text: str = Field(
        description="Suggest a simple modification/correction for the input, keep the corrected text precise as close as possible to the input. DO NOT make up additional text"
    )
    explanation: None | Dict[str, str | List[str]] = Field(
        description="""In this field, several language style guide context headers will be provided, you will return a dictionary output as follows.
                                              Keys: You most only list the provided context headers that were found applicable for editing and modifying the given input, DO NOT mention any header that was not found applicable for corrections.
                                              Values: As values carefully explain under each context header that was found applicable, the different rules that was considered while making the corrections to provide the user with a rational explanation for your corrections."""
    )  # as value answer correctly if the rule was followed with a Yes, No or Not Applicable. Do not mention any rule that was not applied.


class StyleGuideParserV2(BaseModel):
    """
    Pydantic BaseModel for parsing style guide suggestions (alternate version).

    Attributes:
        corrected_text (str): Suggested correction for the input text.
    """
    corrected_text: str = Field(
        description="Suggest a simple modification/correction for the input, keep the corrected text precise as close as possible to the input. DO NOT make up additional text"
    )


class StyleGuide:
    """
    A class for generating and managing style guide information.
    """

    def __init__(self):
        """
        Initialize the StyleGuide class.
        """
        self.file_contents = None
        self.load_files()

    def read_style_guide_files(self, path: List[str]) -> Dict[str, str]:
        """
        Read and store contents of style guide files.

        Parameters:
            path (List[str]): List of file paths.

        Returns:
            Dict[str, str]: Dictionary containing file contents indexed by file path.
        """
        file_contents = {
            file_path: open(file_path, "r", encoding="utf8").read()
            for file_path in path
        }
        return file_contents

    def load_files(self) -> None:
        """
        Load style guide files into memory.
        """
        if self.file_contents is None:
            file_dir = os.path.join(os.getcwd(), "data", "style_guide", "*.txt")
            file_path = glob.glob(file_dir)
            self.file_contents = self.read_style_guide_files(file_path)

    def generate_chat_template(self) -> str:
        """
        Generate a chat template based on style guide context.

        Returns:
            str: Generated chat template.
        """
        current_directory = os.path.join(os.getcwd(), "data", "style_guide")
        ellipses = self.file_contents[
            os.path.join(current_directory, "ELLIPSES (…).txt")
        ]
        alphabetisation = self.file_contents[
            os.path.join(current_directory, "ALPHABETISATION.txt")
        ]
        dashes = self.file_contents[
            os.path.join(current_directory, "DASHES AND HYPHENS.txt")
        ]
        bulleting = self.file_contents[
            os.path.join(current_directory, "BULLETED AND NUMBERED LISTS.txt")
        ]
        ampersand = self.file_contents[
            os.path.join(current_directory, "AMPERSANDS (&).txt")
        ]
        dates_time = self.file_contents[
            os.path.join(current_directory, "DATES AND TIMES.txt")
        ]
        quotation = self.file_contents[
            os.path.join(current_directory, "QUOTATION MARKS.txt")
        ]
        brackets = self.file_contents[
            os.path.join(current_directory, "BRACKETS () [].txt")
        ]
        foreign_words = self.file_contents[
            os.path.join(current_directory, "FOREIGN WORDS.txt")
        ]
        gender = self.file_contents[
            os.path.join(current_directory, "GENDER AND INCLUSIVE LANGUAGE.txt")
        ]
        slashes = self.file_contents[os.path.join(current_directory, "SLASHES.txt")]
        spellings = self.file_contents[os.path.join(current_directory, "SPELLINGS.txt")]
        business_emails = self.file_contents[
            os.path.join(current_directory, "BASICS OF A BUSINESS EMAIL.txt")
        ]
        acronyms = self.file_contents[os.path.join(current_directory, "ACRONYMS.txt")]
        capitalization = self.file_contents[
            os.path.join(current_directory, "CAPITALISATION.txt")
        ]
        full_stops = self.file_contents[
            os.path.join(current_directory, "FULL STOPS (.).txt")
        ]
        apostrophies = self.file_contents[
            os.path.join(current_directory, "APOSTROPHES.txt")
        ]
        money = self.file_contents[os.path.join(current_directory, "MONEY.txt")]
        abbreviation = self.file_contents[
            os.path.join(current_directory, "ABBREVIATIONS, TITLES, AND CONTRACT.txt")
        ]
        figures_tables = self.file_contents[
            os.path.join(current_directory, "FIGURES AND TABLES.txt")
        ]
        numbers = self.file_contents[os.path.join(current_directory, "NUMBERS.txt")]
        commas = self.file_contents[os.path.join(current_directory, "COMMAS (,).txt")]
        parallelism = self.file_contents[
            os.path.join(current_directory, "PARALLELISM.txt")
        ]
        colons = self.file_contents[
            os.path.join(current_directory, "COLONS AND SEMICOLONS.txt")
        ]
        contacts = self.file_contents[
            os.path.join(current_directory, "CONTACT DETAILS.txt")
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

    def styleguide_modify_input(self, basemodel_class: BaseModel = StyleGuideParserV2):
        """
        Modify input text based on style guide suggestions.

        Parameters:
            basemodel_class (BaseModel, optional): Pydantic BaseModel for parsing style guide suggestions. Defaults to StyleGuideParserV2.

        Returns:
            chain: A chain for modifying input text based on style guide suggestions.
        """
        chat_model = ChatOpenAI(model=MODEL_NAME, temperature=0, streaming=True)

        parser = PydanticOutputParser(pydantic_object=basemodel_class)
        format_instructions = parser.get_format_instructions()
        style_guide_context = self.generate_chat_template()
        human_style_context = (
            """
        You are a Language Engine, you are tasked with validating, correcting, and interpreting user mistakes in a text inputs, in accordance with a set of intructions provided in an editorial style guide manual.
        
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

        chat_prompt_template = ChatPromptTemplate(
            messages=[
                system_template,
                HumanMessagePromptTemplate.from_template(human_style_context),
            ],
            input_variables=["input"],
            partial_variables={"format_instructions": format_instructions},
        )

        chain = chat_prompt_template | chat_model
        return chain
