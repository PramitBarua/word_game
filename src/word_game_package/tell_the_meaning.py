#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018"
__credits__ = ["Pramit Barua"]
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]


'''

'''
from src.word_game_package.update_result import update_result
from src.word_game_package.save_file import saving_file

import os
import pickle
import random
import sys
import colorama

def tell_the_meaning(dict_old, **kargs):
    num_list = []
    if 'index' in kargs:
        num_list.append(kargs['index'])
    else:
        num_list = [index for index in range(len(dict_old['score'])) if dict_old['score'][index] !=0]
    if num_list: #check the list is not empty
        if 'all' in kargs: 
    #         num_list = [index for index in range(len(dict_old['score'])) if dict_old['score'][index] > 0]
            visited = []
            while(True):
                number = random.randint(0,len(num_list)-1)
                index = num_list[number]
                if index not in visited:
                    visited.append(index)
    #                 print(colorama.Back.BLACK + '\n' + list_single_value[0] + colorama.Style.RESET_ALL)
                    print('Guess the meaning of the word: ' + colorama.Back.BLACK + dict_old['word'][index] + colorama.Style.RESET_ALL)
                    a = input()  
                    if a == '0000':
                        sys.exit()          
                    print('The correct answer: ' + colorama.Back.BLACK + dict_old['meaning'][index] + colorama.Style.RESET_ALL)
                    while(True):
                        a = input('Do you think you are correct?(y/n)')
                        if a == 'y':
                            dict_old = update_result(1, index, dict_old)
                            saving_file(dict_old)
                            break
                        elif a == 'n':
                            dict_old = update_result(-1, index, dict_old)
                            saving_file(dict_old)
                            break
                        elif a == '0000':
                            sys.exit()
                            break                            
                    os.system('cls')
                elif len(visited)==len(num_list):
                    os.system('cls')
                    break            
        else:
            number = random.randint(0,len(num_list)-1)
            index = num_list[number]
            print('Guess the meaning of the word: ' + colorama.Back.BLACK + dict_old['word'][index] + colorama.Style.RESET_ALL)
            a = input()
            if a == '0000':
                sys.exit()          
            print('The correct answer: ' + colorama.Back.BLACK + dict_old['meaning'][index] + colorama.Style.RESET_ALL)
            while(True):
                a = input('Do you think you are correct?(y/n)')
                if a == 'y':
                    dict_old = update_result(1, index, dict_old)
                    saving_file(dict_old)
                    break
                elif a == 'n':
                    dict_old = update_result(-1, index, dict_old)
                    saving_file(dict_old)
                    break
                elif a == '0000':
                    sys.exit()
                    break
            os.system('cls')
    
if __name__ == '__main__':    
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #removing last 2 folders from location variable
    location = location[:location.find('src')] 
    with open(os.path.join(location, 'word_list.pickle'), 'rb') as handle:
        dict_old = pickle.load(handle)
    tell_the_meaning(dict_old)