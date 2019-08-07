import sys
import os
from pathlib import Path
import json


class WordGameModel:
    """Model class of the word game application."""  
    def __init__(self):
        ## - path to the word list
        self.FILE_PATH = os.path.join(Path(sys.argv[0]).parents[0], 'data', 'updated_word_list.json')
    
    def get_word_list(self):
        '''loads json file and return word list'''
        with open(self.FILE_PATH, 'r', encoding = 'utf-8') as f:
            word_list = json.load(f)
        return word_list
    
    def save_word_list(self, window:str, index:int, data:dict, word_list:dict):
        if window == 'Delete Window':
            # delete word
            del word_list[index]
        elif window == 'Edit Window' and word_list[index] != data:
            # if some edit is done by user
            for key, value in word_list[index].items():
                # data does not contain 'Group' Key
                if key in ('Group',):
                    continue
                word_list[index][key] = data[key]
        elif window == 'New Window':
            # get the last group in the json
            last_group = word_list[-1]['Group']
            # check the length of word in the last group
            last_group_len = len([item['Group'] for item in word_list if item['Group'] == last_group])
            # each group contain at most 25 words
            if last_group_len < 25:
                data['Group'] = last_group
            else:
                # create new group when last group contain more than 25 words
                data['Group'] = f'group {int(last_group.split(" ")[1]) + 1}'
            # add word in word list
            word_list.append(data)
        else:
            return
        
        # update json
        with open(self.FILE_PATH, 'w', encoding = 'utf-8') as f:
            json.dump(word_list, f, indent = 2)