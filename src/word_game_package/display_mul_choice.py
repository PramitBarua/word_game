#!/usr/bin/env python3
from click._compat import colorama

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
import msvcrt
import sys
import colorama
# from termcolor import colored
colorama.init(convert=True)

def display_value(list_single_value, list_mul_value):
    print(colorama.Back.BLACK + '\n' + list_single_value[0] + colorama.Style.RESET_ALL)
#     print('Choose the write answer:')
    x = [0,1,2,3]
    random.shuffle(x)
    ans = x.index(0)+1
    c = 1
    for idx in x:
        print(colorama.Back.BLACK + str(c) + '. ' + list_mul_value[idx] + colorama.Style.RESET_ALL)
        c = c+1
        
    check = input('Choose the right answer:')
    if check == '0000':
        sys.exit()
    while(1):
#         if type(check).__name__ != 'int':
#             print('Please pick a number.')
#             check = input('Choose the write answer:')
        try:
            if int(check)>4 or int(check)<1:
                print('Please pick a correct number')
                check = input('Choose the write answer:')
                if check == '0000':
                    sys.exit()
            else:
                break
        except:
            print('Please pick a number.')
            check = input('Choose the write answer:')       
            if check == '0000':
                sys.exit()     
        
    if check == str(ans):
        print('\nGood job\n')
        print('Question: ' + colorama.Back.BLACK + list_single_value[0] + '\n' + colorama.Style.RESET_ALL)
        print('Correct Answer: ' + colorama.Back.BLACK + list_mul_value[0] + colorama.Style.RESET_ALL)
        print('Your Answer: ' + colorama.Back.BLACK + colorama.Fore.RED + list_mul_value[x[int(check)-1]] + colorama.Style.RESET_ALL)
        a = input('Press any key to continue.')
        if a == '0000':
            sys.exit()
        os.system('cls')
        return 1
    else:
        print('\nYou are wrong\n')
        print('Question: ' + colorama.Back.BLACK + list_single_value[0] + '\n' + colorama.Style.RESET_ALL)
        print('Correct Answer: ' + colorama.Back.BLACK + list_mul_value[0] + colorama.Style.RESET_ALL)
        print('Your Answer: ' + colorama.Back.BLACK + colorama.Fore.RED + list_mul_value[x[int(check)-1]] + colorama.Style.RESET_ALL)
        a = input('Press any key to continue.')
        if a == '0000':
            sys.exit()
        os.system('cls')
        return -1

if __name__ == '__main__':
    display_value(['a'], ['a','b','c','d'])