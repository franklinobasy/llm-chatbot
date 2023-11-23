'''
Custom error handler
'''


class AnswersMisMatchQuestion(Exception):
    '''Exception class for bad Answer Input'''
    def __init__(self, n_questions, n_answers):
        super().__init__(
            f"Number of expected answers given mismatched number of questions. Questions: {n_questions}, Answers: {n_answers}."
        )


class UnknownSectionName(Exception):
    '''Exception class for unsupportrd section name'''
    def __init__(self, section_name):
        super().__init__(
            f"'{section_name}' is not a supported template section."
        )


class UnknownSectionID(Exception):
    '''Exception class for unsupported section id'''
    def __init__(self, section_id):
        super().__init__(
            f"No section with section_id:'{section_id}'."
        )


class UnknownTemplateID(Exception):
    '''Exception class for unsupported section id'''
    def __init__(self, template_id):
        super().__init__(
            f"No section with section_id:'{template_id}'."
        )


class PathTypeMisMatch(Exception):
    '''Exception class for handling wrong query type'''
    def __init__(self, type_):
        super().__init__(
            f"'{type(type_)}' is not supported"
        )


class VectorIndexError(Exception):
    '''Exception class for handling wrong query type'''
    def __init__(self, e):
        super().__init__(
            f"Something went wrong while building vector store: '{e}'"
        )
