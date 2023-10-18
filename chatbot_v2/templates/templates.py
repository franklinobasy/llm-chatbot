from typing import Dict, List, Tuple


def clean_template(item: Tuple) -> Tuple[str, List[str]]:
    '''Utility for cleaning template texts'''
    item = list(item)
    summary = item[1][0].replace("\n", "").replace(" " * 8, "")
    template = item[1][1].replace("\n", "").replace(" " * 8, "")
    item = (item[0], [summary, template])
    return item


def clean_question(item: Tuple) -> Tuple[str, str]:
    '''Utility for cleaning question texts'''
    item = list(item)
    question = item[1].replace("\n", "").replace(" " * 4, "")
    item = (item[0], question)
    return item


INTRODUCTION_TEMPLATES = {
    "1": [
        '''
        This template introduces a proposal where a company or organization
        has conducted research in specific areas and aims to integrate the
        findings into a robust surveillance solution tailored for a
        particular industry or niche.
        ''',
        '''
        [Your Company/Organization Name] has been conducting research in
        areas of [Research Focus] and [Another Research Focus].
        We would like to combine the results of these efforts into a solid
        solution for [Industry or Niche] surveillance.
        '''
    ],
    "2": [
        '''
        This template introduces a proposal in which a company with a history
        of innovation in a specific industry or niche outlines its vision to
        leverage its expertise in key areas to revolutionize a specific aspect
        within that industry or niche.
        ''',
        '''
        [Your Company/Organization Name] has a long-standing history of
        innovation in [Industry or Niche]. Our expertise in
        [Key Expertise Area] and [Another Key Expertise Area] has allowed
        us to identify a unique opportunity to revolutionize
        [Specific Area within Industry/Niche]. This proposal aims to outline
        our vision for an innovative solution that will reshape the landscape
        of [Industry or Niche]
        '''
    ],
    "3": [
        '''
        This template introduces a proposal by emphasizing the company's
        expertise and past research achievements, positioning it to address
        a critical issue in a specific industry or niche and outlining plans
        to create a transformative solution for the benefit of a particular
        stakeholder or beneficiary.
        ''',
        '''
        With a track record of groundbreaking research in [Research Focus] and
        [Another Research Focus], [Your Company/Organization Name] is
        well-positioned to address a pressing challenge in
        [Industry or Niche]. This proposal outlines our ambitious plans to
        leverage our expertise and resources to create a game-changing
        solution that will benefit [Stakeholder or Beneficiary].
        '''
    ],
    "4": [
        '''
        This template introduces a proposal in which a company, having
        invested resources in researching specific areas, aims to utilize
        their knowledge and insights to create a groundbreaking solution
        for a specific problem within a particular industry or niche.
        ''',
        '''
        [Your Company/Organization Name] has dedicated significant resources
        to exploring the intricacies of [Research Focus] and
        [Another Research Focus]. We believe that the knowledge and insights
        gained from our efforts can be harnessed to develop a transformative
        solution for [Specific Problem or Challenge] within
        [Industry or Niche]. This proposal outlines our vision for a
        groundbreaking project that will address this issue head-on.
        '''
    ],
}

INTRODUNCTION_DESCRIPTION_QUESTION = {
    "Question 1": '''
    What are the specific areas of research focuses that Cyphercrescent has
    dedicated resources to explore?
    ''',
    "Question 2": "What Industry or Niche is this proposal focused on?",
    "Question 3": '''
    What knowledge and insights have you gained from these research efforts,
    and how do they relate to addressing the Specific Problem or Challenge
    within the Industry or Niche?
    ''',
    "Question 4": '''
    How do you envision harnessing the acquired knowledge and insights to
    develop a transformative solution for the identified problem or challenge?
    ''',
    "Question 5": '''
    Could you describe the key elements of your groundbreaking project, and
    how it intends to directly address the issue within the Industry or Niche?
    '''
}


section_templates: Dict[str, List[Dict]] = {
    "introduction": [
        INTRODUCTION_TEMPLATES, INTRODUNCTION_DESCRIPTION_QUESTION
    ],
}
