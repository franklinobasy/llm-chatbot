from chatbot.generate_proposal.extractor import FieldExtractor
from chatbot.generate_proposal.autofill import AutoFillField
e = FieldExtractor()
e.load_file("data/template1.txt")
fields = e.get_fields()
a = AutoFillField(fields, "gpt-3.5-turbo-0301")
context = "A questionaire for writing a proposal for an oil and gas firm who is into well intervention services and wants to use some of your products with a budget of $100,000"
a.set_context(context)
filled_fields = a.fill_fields()
e.fill_text(filled_fields)


# import re

# # Read the content of the file
# def read_text_file(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         return file.read()

# # Define a function to replace words within brackets
# def replace_words_in_brackets(text, replacement_words):
#     # Define a regular expression pattern to match words within brackets
#     pattern = r'\[([^\[\]]+)\]'

#     # Use a function to perform replacements based on the matched words
#     def repl(match):
#         nonlocal replacement_words
#         if replacement_words:
#             replacement = replacement_words.pop(0)
#             return '[' + replacement + ']'
#         else:
#             return match.group(0)  # If no more replacements, keep the original text inside the brackets


#     # Use re.sub to replace words within brackets
#     result = re.sub(pattern, repl, text)

#     return result

# # Specify the file path and replacement words
# file_path = 'file.txt'  # Replace with the path to your file
# replacement_words = ['apple', 'banana', 'cherry', 'date']  # Replace with your list of words

# # Read the content from the file
# text = read_text_file(file_path)

# # Replace words within brackets
# result_text = replace_words_in_brackets(text, replacement_words)

# # Save or print the result
# with open('output.txt', 'w', encoding='utf-8') as output_file:
#     output_file.write(result_text)
