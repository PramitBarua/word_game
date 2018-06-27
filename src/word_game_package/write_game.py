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
from src.word_game_package.update_result import update_result

import os
import pickle
import sys
import colorama

def write_game(num_dict, **kargs):
    if 'index' in kargs:
        index = kargs['index']
    else:
        index = random_number(num_dict)
        
    print('\n' + colorama.Back.BLACK + num_dict['meaning'][index] + colorama.Style.RESET_ALL)
    check = input('Write the word:')
    if check.lower() == num_dict['word'][index].lower():
        print('\nGood job\n')
        print('Question: ' + colorama.Back.BLACK + num_dict['meaning'][index] + colorama.Style.RESET_ALL)
        print('Correct Answer: ' + colorama.Back.BLACK + num_dict['word'][index] + colorama.Style.RESET_ALL)
        print('Your Answer: ' + colorama.Back.BLACK + check + colorama.Style.RESET_ALL)
        a = input('Press any key to continue.')
        if a == '0000':
            sys.exit()
        os.system('cls')
        num_dict = update_result(1, index, num_dict)
        return num_dict
    else:
        print('\nYou are wrong\n')
        print('Question: ' + colorama.Back.BLACK + num_dict['meaning'][index] + colorama.Style.RESET_ALL)
        print('Correct Answer: ' + colorama.Back.BLACK + num_dict['word'][index] + colorama.Style.RESET_ALL)
        print('Your Answer: ' + colorama.Back.BLACK + colorama.Fore.RED + check + colorama.Style.RESET_ALL)
        a = input('Press any key to continue.')
        if a == '0000':
            sys.exit()
        os.system('cls')
        num_dict = update_result(-1, index, num_dict)
        return num_dict

if __name__ == '__main__':    
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #removing last 2 folders from location variable
    location = location[:location.find('src')] 
    with open(os.path.join(location, 'word_list.pickle'), 'rb') as handle:
        dict_old = pickle.load(handle)
    dict_old = write_game(dict_old)