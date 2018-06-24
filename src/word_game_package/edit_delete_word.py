#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018"
__credits__ = ["Pramit Barua"]
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]


'''

'''

import pickle

def edit_word(dict_old):    
    old_word = input("What to edit? ")
    if old_word == '':
        print('No input')
    elif old_word not in dict_old['word']:
        print('Word does not exists')
    else:
        index = dict_old['word'].index(old_word)                
        check = input('Do you like to edit\n'+ dict_old['word'][index] + 
                      '\n' + dict_old['meaning'][index] +
                      str(dict_old['score'][index]) + '?\n')
        if check == 'y' or check == 'Y':
            flag = True
            while(flag):
                new_word = input("What to add? ")
                if new_word == '':
                    print('No input')
                    flag = False
                elif new_word in dict_old['word']:
                    print('Word exists')                            
                else:
                    new_meaning = input("What is the meaning of " + new_word + '? ')
                    check = input('Do you like to add\n'+ new_word + 
                              '\t' + new_meaning + '?\n')
                    if check == 'y' or check == 'Y':
                        dict_old['word'][index] = new_word
                        dict_old['meaning'][index] = new_meaning + '\n'
                        dict_old['score'][index] = 0
#                         with open('word_list.pickle', 'wb') as handle:
#                             pickle.dump(dict_old, handle, protocol=pickle.HIGHEST_PROTOCOL)
                        print('Edit complete')
                        flag = False 
    return dict_old

def delete_word(dict_old):    
    old_word = input("What to delete? ")
    if old_word == '':
        print('No input')
    elif old_word not in dict_old['word']:
        print('Word does not exists')
    else:
        index = dict_old['word'].index(old_word)                
        check = input('Do you like to delete\n'+ dict_old['word'][index] + 
                      '\n' + dict_old['meaning'][index] +
                      str(dict_old['score'][index]) + '?\n')
        if check == 'y' or check == 'Y':
            del dict_old['word'][index]
            del dict_old['meaning'][index]
            del dict_old['score'][index]
#             with open('word_list.pickle', 'wb') as handle:
#                 pickle.dump(dict_old, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print('Delete complete')
    
    return dict_old

    

if __name__ == '__main__':    
    edit_word()