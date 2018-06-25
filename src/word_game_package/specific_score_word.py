#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018"
__credits__ = ["Pramit Barua"]
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]


'''

'''
from src.word_game_package.choose_the_game import choose_the_game

import os
import pickle
import random
import sys

def specific_score_words(dict_old, num_list):
#     num_list contains index of more than 5 words
    print('We have more than 5 words that score below -3.\n')
    while(True):
        while(True):
            for item in num_list:
                print(dict_old['word'][item] + '\n')
                print(dict_old['meaning'][item])
                b = input('Press any key to continue.')
                if b == '0000':
                    sys.exit()
            a = input('Confident enough to play the game?(y/n)')
            if a == '0000':
                sys.exit()
            if a == 'y':
                break #break the 1st inner while
        visited = []
        while(True):
            number = random.randint(0,len(num_list)-1)
            index = num_list[number]
            if index not in visited:
                choose_the_game(dict_old, index = index)
                visited.append(index)
            elif len(visited) == len(num_list):
                num_list = [index for index in range(len(dict_old['score'])) if dict_old['score'][index] < -3]
                break #break 2nd while
        if len(num_list) > 0:
            check = input('Still there are some words would you to study now?(y/n)')
            if check == '0000':
                sys.exit()
            if check == 'n':
                break
        else:
            break    


if __name__ == '__main__':    
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #removing last 2 folders from location variable
    location = location[:location.find('src')] 
    with open(os.path.join(location, 'word_list.pickle'), 'rb') as handle:
        dict_old = pickle.load(handle)
    num_list = [index for index in range(len(dict_old['score'])) if dict_old['score'][index] < -1]
    specific_score_words(dict_old, num_list)