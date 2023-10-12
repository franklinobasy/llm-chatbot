from chatbot.auto_response.prompts import AVAILABLE_PROMPTS

APPLICATION_START_INSTRUCTIONS = '''
Welcome to CCL AI-Assitant
Choose:
    1 - To use Automated Responses
    2 - To generate proposal

'''

AUTORESPONSE_INSTRUCTIONS = "Choose from the available query:\n"
for i, prompt in enumerate(AVAILABLE_PROMPTS, start=1):
    AUTORESPONSE_INSTRUCTIONS += f"\t{i} - {prompt}\n"
