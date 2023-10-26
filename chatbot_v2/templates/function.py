def read_file(template_files):
    try:
        with open(template_files, 'r',encoding='utf8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "please wait!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

template_file = r'chatbot_v2\templates\template_files\executive_summary\executive_summary_questions\summary_questions_1.txt'
file_content = read_file(template_file)
print(file_content)