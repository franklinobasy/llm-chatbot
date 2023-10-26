import os

# Define the function that reads the text files in the folder and its subfolders recursively
def read_text_files_recursive(folder_path):
    text_list = []  # List to store the contents of text files

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            # It's a file, so read it
            try:
                with open(item_path, 'r', encoding='utf-8') as file:
                    file_contents = file.read()
                    text_list.append(file_contents)
            except Exception as e:
                print(f"Something went wrong while reading {item_path}: {str(e)}")
        elif os.path.isdir(item_path):
            # It's a directory, so recursively call the function
            text_list.extend(read_text_files_recursive(item_path))

    return text_list

# Define the top-level folder path
top_folder = r'chatbot_v2\templates'

texts = read_text_files_recursive(top_folder)

for i, text in enumerate(texts):
    print(f"Contents of file {i + 1}:\n{text}\n")