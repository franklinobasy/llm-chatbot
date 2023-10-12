'''
This modules contains classes for Extracting texts from files
'''

from abc import ABC, abstractmethod


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
