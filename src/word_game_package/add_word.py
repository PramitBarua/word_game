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

# def load_file():
#     with open('word_list.txt') as f:
#         content = f.readlines()
#                        
#         word = []
#         meaning = []
#         for idx1, line in enumerate(content):
#             if '\t' in line and '\n' in line:
#                 info = line.split('\t')
#                 word.append(info[0])
#                 meaning.append(info[1])                
#             elif line == '\n':
#                 pass
#             elif '\n' in line and '\t' not in line:
#                 meaning[-1] = meaning[-1] + line
#         
#         score = [0]*len(word)
#         dict = {'word':word, 'meaning':meaning, 'score':score}
#         with open('python_word_list.pickle', 'wb') as handle:
#             pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
#         print(1)

def add_word(dict_old):
#     with open('word_list.pickle', 'rb') as handle:
#         dict_old = pickle.load(handle)

    new_word = input("What to add? ")
    
    if new_word == '':
        print('No input')
    elif new_word in dict_old['word']:
        print('Word exists')
    else:
        new_meaning = input("What is the meaning of " + new_word + '?')
        check = input("Do you like to add\n" + new_word + '\t' + new_meaning)
        if check == 'y' or check == 'Y':
            dict_old['word'].append(new_word)
            dict_old['meaning'].append(new_meaning)
            dict_old['score'].append(0)
            
#             with open('word_list.pickle', 'wb') as handle:
#                 pickle.dump(dict_old, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
            print('Word is added')            
        else:
            print('Word is not added')
    return dict_old
    

if __name__ == '__main__':    
    add_word()