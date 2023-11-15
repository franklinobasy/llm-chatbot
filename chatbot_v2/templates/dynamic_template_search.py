'''
Templates function handler
'''

import os

# Define the function that reads the text files in the folder and
# its subfolders recursively


def files_for_section(base_path, folder_name, get_questions: bool = False):
    '''Get files content for a section'''
    files_contents = []
    if get_questions:
        path = os.path.join(
            base_path, folder_name, f"{folder_name}_questions"
        )
    else:
        path = os.path.join(base_path, folder_name)
    if folder_name in os.listdir(base_path):
        for file_name in os.listdir(path):
            item_path = os.path.join(path, file_name)
            if os.path.isfile(item_path):
                with open(item_path, 'r', encoding='utf-8') as file:
                    contents = file.read()
                    files_contents.append(contents)
    else:
        raise FileNotFoundError(f"{folder_name} not found in templates")

    return files_contents


# Define the top-level folder path
BASE_PATH = os.path.join(
    os.getcwd(), 'chatbot_v2', 'templates', 'template_files'
)


if __name__ == "__main__":
    texts = files_for_section(BASE_PATH, "our_clients", get_questions=True)

    for i, text in enumerate(texts):
        print(f"Contents of file {i + 1}:\n{text}\n")