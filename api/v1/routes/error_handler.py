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
