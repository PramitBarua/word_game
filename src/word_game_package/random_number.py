#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018"
__credits__ = ["Pramit Barua"]
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]


'''

'''

import random
import os
import pickle

def while_loop(num_dict):
    number = random.randint(-5,5)
    while(1):
        if number in num_dict['score']:
            break
        else: 
            number = random.randint(-5,5)
    num_list = [index for index in range(len(num_dict['score'])) if num_dict['score'][index] == number]
    return num_list

def random_number(num_dict):
    num_list = while_loop(num_dict)
    index = num_list[random.randint(0,len(num_list)-1)]           
    
    while(1):
        if num_dict['score'][index]<-3:
            break
        elif len(num_list)>15:
            break
        else:
            num_list = while_loop(num_dict)
            index = num_list[random.randint(0,len(num_list)-1)]
    return index
#     if len(num_list)>5 
#     return num_list[random.randint(0,len(num_list)-1)]


if __name__ == '__main__':    
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #removing last 2 folders from location variable
    location = location[:location.find('src')] 
    with open(os.path.join(location, 'word_list.pickle'), 'rb') as handle:
        dict_old = pickle.load(handle)
    random_number(dict_old)