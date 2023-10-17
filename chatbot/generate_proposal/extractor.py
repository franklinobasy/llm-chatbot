'''
This modules contains classes for Extracting texts from files
'''

from abc import ABC, abstractmethod
from typing import Dict, List
import docx
from pdfminer.high_level import extract_text
import re


class Extractor(ABC):

    @abstractmethod
    def load_file(self, file_path: str):
        '''
        Load file from file path

        Args:
            file_path: path to file
        '''
        pass

    @abstractmethod
    def get_text_file(self):
        '''
        Get processed text
        '''
        pass


class TextExtractor(Extractor):
    '''
    TextExtractor class for processing texts from txt files
    '''
    def load_file(self, file_path):
        '''
        Load text from a .txt file

        Args:
            file_path: path to the .txt file
        '''
        if not file_path.endswith(".txt"):
            raise ValueError(
                "Invalid file format. This extractor only works with .txt files."
            )

        with open(file_path, 'r', encoding='utf-8') as file:
            self.text = file.read()

    def get_text_file(self):
        '''
        Get the loaded text

        Returns:
            The extracted text from the .txt file
        '''
        if not hasattr(self, "text"):
            raise ValueError("No text has been loaded yet.")
        return self.text


class FieldExtractor(Extractor):
    '''An Extractor class for getting fields in a text file'''

    VALID_EXTS = ('.txt', '.pdf', '.docx')
    
    def load_file(self, file_path):
        '''
        Load text from a .txt file

        Args:
            file_path: path to the .txt file
        '''

        if not file_path.endswith(self.VALID_EXTS):
            raise ValueError(
                f"Invalid file format. This extractor only works with \
                    {','.join(self.VALID_EXTS)} files."
            )

        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                self.text = file.read()
        elif file_path.endswith('.pdf'):
            self.text = extract_text(file_path)
        elif file_path.endswith('.docx'):
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
            self.text = text

    def get_text_file(self):
        return super().get_text_file()

    def get_fields(self):
        if not hasattr(self, "text"):
            raise ValueError("No text has been loaded yet.")

        pattern = r'\[([^\[\]]+)\]'
        matches: List[str] = re.findall(pattern, self.text)
        matches = [match + '?' for match in matches]
        return matches

    def fill_text(self, filled_fields: Dict):
        if not hasattr(self, "text"):
            raise ValueError("No text has been loaded yet.")

        filled_fields = list(filled_fields.values())
        pattern = r'\[([^\[\]]+)\]'

        def repl(match):
            nonlocal filled_fields
            if filled_fields:
                replacement = filled_fields.pop(0)
                return '[' + replacement + ']'
            else:
                return match.group(0)  # If field not found, keep it as is

        filled_text = re.sub(pattern, repl, self.text)
        self.filled_text = filled_text
        with open('output.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(self.filled_text)
        return self.filled_text
