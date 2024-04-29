"""
Custom error handler for API routes.
"""


class AnswersMisMatchQuestion(Exception):
    """
    Exception raised when the number of provided answers mismatches the number of questions.

    Attributes:
        n_questions (int): Number of expected questions.
        n_answers (int): Number of provided answers.
    """

    def __init__(self, n_questions, n_answers):
        """
        Initialize the exception with the number of questions and answers.

        Args:
            n_questions (int): Number of expected questions.
            n_answers (int): Number of provided answers.
        """
        super().__init__(
            f"Number of expected answers given mismatched number of questions. Questions: {n_questions}, Answers: {n_answers}."
        )


class UnknownSectionName(Exception):
    """
    Exception raised for unknown section name.

    Attributes:
        section_name (str): Name of the unknown section.
    """

    def __init__(self, section_name):
        """
        Initialize the exception with the unknown section name.

        Args:
            section_name (str): Name of the unknown section.
        """
        super().__init__(f"'{section_name}' is not a supported template section.")


class UnknownSectionID(Exception):
    """
    Exception raised for unknown section ID.

    Attributes:
        section_id (int): ID of the unknown section.
    """

    def __init__(self, section_id):
        """
        Initialize the exception with the unknown section ID.

        Args:
            section_id (int): ID of the unknown section.
        """
        super().__init__(f"No section with section_id:'{section_id}'.")


class UnknownTemplateID(Exception):
    """
    Exception raised for unknown template ID.

    Attributes:
        template_id (int): ID of the unknown template.
    """

    def __init__(self, template_id):
        """
        Initialize the exception with the unknown template ID.

        Args:
            template_id (int): ID of the unknown template.
        """
        super().__init__(f"No template with template_id:'{template_id}'.")


class PathTypeMisMatch(Exception):
    """
    Exception raised for wrong query type.

    Attributes:
        type_ (type): Type of the query.
    """

    def __init__(self, type_):
        """
        Initialize the exception with the wrong query type.

        Args:
            type_ (type): Type of the query.
        """
        super().__init__(f"'{type(type_)}' is not supported")


class VectorIndexError(Exception):
    """
    Exception raised for vector index errors.

    Attributes:
        e (str): Error message.
    """

    def __init__(self, e):
        """
        Initialize the exception with the error message.

        Args:
            e (str): Error message.
        """
        super().__init__(f"Something went wrong while building vector store: '{e}'")
