#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018"
__credits__ = ["Pramit Barua"]
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]


'''

'''

from src.word_game_package.add_word import add_word
from src.word_game_package.edit_delete_word import edit_word
from src.word_game_package.edit_delete_word import delete_word
from src.word_game_package.mul_choice_que import mul_choice_que
from src.word_game_package.write_game import write_game

import pickle
import random
import argparse

def saving_file(num_dict):
    with open('word_list.pickle', 'wb') as handle:
        pickle.dump(dict_old, handle, protocol=pickle.HIGHEST_PROTOCOL)
    

if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description='WORD GAME')
    parser.add_argument('-M', "--Modify_word_list",
                        help="Add word in the list: a"+
                        "Edit word in the list: e" +
                        "Delete word in the list: d" +
                        "Show the word list: s")
#     parser.add_argument("-g","--Play_game",
#                         help="Word play")
    
    args = parser.parse_args()
    
    with open('word_list.pickle', 'rb') as handle:
        dict_old = pickle.load(handle)
        
    if args.Modify_word_list == 'a':
        dict_new = add_word(dict_old)
        saving_file(dict_new)
    elif args.Modify_word_list == 'e':
        dict_new = edit_word(dict_old)
        saving_file(dict_new)
    elif args.Modify_word_list == 'd':
        dict_new = delete_word(dict_old)
        saving_file(dict_new)
    elif args.Modify_word_list == 's':
        for idx in range(len(dict_old['word'])):
            print(dict_old['word'][idx] + '\t' +dict_old['meaning'][idx] + '\t' + 
                  str(dict_old['score'][idx])+ '\n\n')
    else:        
        for x in range(15):
            seed = random.randint(-1,1) #decide which game will perform
            if seed < 0: # means multiple choice ans 
                dict_new = mul_choice_que(dict_old)
                saving_file(dict_new)
            else: #writing the word, meaning will be given
                dict_new = write_game(dict_old)
                saving_file(dict_new)
            