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

def display_value(list_single_value, list_mul_value):
    print('\n' + list_single_value[0])
#     print('Choose the write answer:')
    x = [0,1,2,3]
    random.shuffle(x)
    ans = x.index(0)+1
    c = 1
    for idx in x:
        print(str(c) +'. '+list_mul_value[idx])
        c = c+1
        
    check = input('Choose the write answer:')
    while(1):
        if int(check)>4 or int(check)<1:
            print('please pick a correct value')
        else:
            break
    if check == str(ans):
        print('\nGood job\n')
        print('Question: ' + list_single_value[0] + '\n')
        print('Correct Answer: ' + list_mul_value[0])
        print('Your Answer: ' + list_mul_value[x[int(check)-1]])
        a = input('Press any key to continue.')
        os.system('cls')
        return 1
    else:
        print('\nYou are wrong\n')
        print('Question: ' + list_single_value[0] + '\n')
        print('Correct Answer: ' + list_mul_value[0])
        print('Your Answer: ' + list_mul_value[x[int(check)-1]])
        a = input('Press any key to continue.')
        os.system('cls')
        return -1
#     print(1)