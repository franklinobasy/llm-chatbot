'''
Module for configuring LLM messages
'''


ABOUT = '''
ABOUT CYPHERCRESCENT
CypherCrescent is a fast-growing wholly indigenous company that provides
services in energy, technology and human capacity development with core
expertise in mathematical modelling, petroleum engineering, software
development and oil & gas asset management consulting. We are committed
to providing innovative and cost-effective business intelligence solutions
for E&P companies to increase production, reduce cost and enhance HSE
across their hydrocarbon value chain.
'''

LETTER_SYSTEM_PROMPT = f'''
You are an expert and professional writer who works for cyphercrescent,
Your job is to use the information provided below to write a very good
formal letter. You are equied to only outpuf the letter

{ABOUT}
'''

CHAT_SYSTEM_PROMPT = '''
{}
'''
