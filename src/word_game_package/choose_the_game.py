#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018"
__credits__ = ["Pramit Barua"]
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]


'''

'''

from src.word_game_package.mul_choice_que import mul_choice_que
from src.word_game_package.write_game import write_game
from src.word_game_package.save_file import saving_file

import os
import pickle
import random

def choose_the_game(dict_old, **kargs):
    seed = random.randint(-1,1) #decide which game will perform
    if 'index' in kargs:
        if seed < 0: # means multiple choice ans 
            dict_new = mul_choice_que(dict_old, index = kargs['index'])
            saving_file(dict_new)
        else: #writing the word, meaning will be given
            dict_new = write_game(dict_old, index = kargs['index'])
            saving_file(dict_new)
    else:
        if seed < 0: # means multiple choice ans 
            dict_new = mul_choice_que(dict_old)
            saving_file(dict_new)
        else: #writing the word, meaning will be given
            dict_new = write_game(dict_old)
            saving_file(dict_new)
        
    
if __name__ == '__main__':    
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #removing last 2 folders from location variable
    location = location[:location.find('src')] 
    with open(os.path.join(location, 'word_list.pickle'), 'rb') as handle:
        dict_old = pickle.load(handle)
    choose_the_game(dict_old, index = 2)