#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018"
__credits__ = ["Pramit Barua"]
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]


'''

'''

from src.word_game_package.random_number import random_number
from src.word_game_package.display_mul_choice import display_value
from src.word_game_package.update_result import update_result
 
import pickle
import random
import os

def mul_choice_que(num_dict):
    word_meaning = random.randint(0,1) # 0 means word 1 means meaning
    index = random_number(num_dict)
    word = []
    meaning = []
    if word_meaning == 0:
        word.append(num_dict['word'][index]) #word contains only one value
        meaning.append(num_dict['meaning'][index])
        for idx in range(3):
            meaning.append(num_dict['meaning'][random.randint(0,len(num_dict['word'])-1)])
        result = display_value(word, meaning)
        num_dict = update_result(result, index, num_dict)
#         print(1)
    else:
        meaning.append(num_dict['meaning'][index]) #meaning contains only one value
        word.append(num_dict['word'][index])
        for idx in range(3):
            word.append(num_dict['word'][random.randint(0,len(num_dict['word'])-1)])
        result = display_value(meaning, word)
        num_dict = update_result(result, index, num_dict)
#         print(1)
    return num_dict

if __name__ == '__main__':    
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #removing last 2 folders from location variable
    location = location[:location.find('src')] 
    with open(os.path.join(location, 'word_list.pickle'), 'rb') as handle:
        dict_old = pickle.load(handle)
    dict_old = mul_choice_que(dict_old)