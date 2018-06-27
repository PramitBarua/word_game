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
import os
import colorama

colorama.init(convert=True)

def edit_word(dict_old):    
    old_word = input("What to edit? ")
    if old_word == '':
        print('No input')
    elif old_word not in dict_old['word']:
        print('Word does not exists')
    else:
        index = dict_old['word'].index(old_word)                
        print('Do you like to edit\n'+ colorama.Back.BLACK +
                      dict_old['word'][index] + '\n' + 
                      dict_old['meaning'][index] + colorama.Style.RESET_ALL
                      + str(dict_old['score'][index]) + '?\n' )
        check = input()
        if check == 'y' or check == 'Y':
            flag = True
            while(flag):
                new_word = input("What to add? ")
                if new_word == '':
                    print('No input')
                    flag = False
#                 elif new_word in dict_old['word']:
#                     print('Word exists')                            
                else:
                    lines = []
                    print("What is the meaning of " + new_word + '? ')
                    while(True):
                        line = input()
                        if line:
                            lines.append(line)
                        else:
                            break                    
                    new_meaning = '\n'.join(lines)
                    print('Do you like to add\n'+ colorama.Back.BLACK +
                                  new_word + '\t' + new_meaning + 
                                  colorama.Style.RESET_ALL + '?\n')
                    check = input()
                    if check == 'y' or check == 'Y':
                        dict_old['word'][index] = new_word
                        dict_old['meaning'][index] = new_meaning + '\n'
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
        print('Do you like to delete\n'+ colorama.Back.BLACK +
                      dict_old['word'][index] + '\n' + 
                      dict_old['meaning'][index] + colorama.Style.RESET_ALL
                      + str(dict_old['score'][index]) + '?\n' )           
        check = input()
        if check == 'y' or check == 'Y':
            del dict_old['word'][index]
            del dict_old['meaning'][index]
            del dict_old['score'][index]
            del dict_old['visited'][index]
#             with open('word_list.pickle', 'wb') as handle:
#                 pickle.dump(dict_old, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print('Delete complete')
    
    return dict_old

    

if __name__ == '__main__':    
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #removing last 2 folders from location variable
    location = location[:location.find('src')] 
    with open(os.path.join(location, 'word_list.pickle'), 'rb') as handle:
        dict_old = pickle.load(handle)
    edit_word(dict_old)