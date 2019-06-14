import sys
import os
from pathlib import Path
import json
import random



class WordGameModel:
    """Model class of the word game application."""  
    def __init__(self):
        ## - path to the word list
        self.FILE_PATH = os.path.join(Path(sys.argv[0]).parents[0], 'data', 'updated_word_list.json')
    
    def get_word_list(self):
        with open(self.FILE_PATH, 'r', encoding = 'utf-8') as f:
            self.WORD_LIST = json.load(f)
        return self.WORD_LIST
            
    
    def generate_random_num(self, start=0, end=100):
        return random.randint(start, end)
    
    def save_word_list(self, index, data):
        if self.WORD_LIST[index] != data:
            for key, value in self.WORD_LIST[index].items():
                if key in ('Group', 'Visited'):
                    continue
                self.WORD_LIST[index][key] = data[key]
            with open(self.FILE_PATH, 'w', encoding = 'utf-8') as f:
                json.dump(self.WORD_LIST, f, indent = 2)