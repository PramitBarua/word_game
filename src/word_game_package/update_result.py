#!/usr/bin/env python3

__author__ = "Pramit Barua"
__copyright__ = "Copyright 2018"
__credits__ = ["Pramit Barua"]
__version__ = "1"
__maintainer__ = "Pramit Barua"
__email__ = ["pramit.barua@student.kit.edu", "pramit.barua@gmail.com"]


'''

'''


def update_result(result, index, num_dict):
    num_dict['visited'][index] = num_dict['visited'][index] + 1
    if result > 0:
        if num_dict['visited'][index] >= 2:
            num_dict['score'][index] = num_dict['score'][index] + result
            num_dict['visited'][index] = 0
    else:
        num_dict['score'][index] = num_dict['score'][index] + result
        num_dict['visited'][index] = 0
        
    if num_dict['score'][index] > 5:
        num_dict['score'][index] = 5
    elif num_dict['score'][index] < -5:
        num_dict['score'][index] = -5
    
    return num_dict    
#     num_dict['score'][index]
    
    