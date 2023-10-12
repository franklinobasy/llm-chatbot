'''
This module contains functionality for structuring prompts
'''

from langchain import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage


get_fields_prompt = '''
Your are an AI bot that finds custom fields in a text and
return them as Python language dictionary.
Your response should be strictly a python dictionary.

Use the format below as output:
{
    'custom field description': 'datatype of field (str, list or int)'
}
'''
