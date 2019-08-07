
import requests
# import urllib
from bs4 import BeautifulSoup
import json
import time
import re
# import pandas as pd
# import numpy as np

# import reportlab
# from reportlab.platypus import *
# from reportlab.lib import colors
# from reportlab.pdfgen import canvas
# from reportlab.pdfbase.pdfmetrics import stringWidth
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import mm
# from textwrap import wrap
# 
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont

class conversions():
    def __init__(self):
        self.filepath = r'C:\Users\PRAMIT\Documents\Dropbox\python_project\Word_game\data/'

    def generate_pdf(self):
        with open(self.filepath+'updated_word_list.json', 'r', encoding='utf-8') as f:
            word_list = json.load(f)
            
        word = [item['Word'].lower() for item in word_list]
            
        with open(self.filepath+'word_smart.txt', 'r', encoding='utf-8') as f:
            word_smart = f.read()
        
        word_smart = word_smart.split('\n')
        for line in word_smart:
            if line.lower() not in word:
                print(line)
                
        print(1)

    def get_text_from_web(self):
        with open(self.filepath+'updated_word_list.json', 'r', encoding='utf-8') as f:
            word_list = json.load(f)
        
        for idx, item in enumerate(word_list):
            if item['Sentence'] == '':
                print(item['Word'])
                page = requests.get("https://sentence.yourdictionary.com/"+item['Word'].lower())
                soup = BeautifulSoup(page.content, 'html.parser')
                time.sleep(1)
                
                try:
                    # for www.merriam-webster.com    
                    html = list(soup.children)[6]
                    body = list(html.children)[5]
                    p = list(body.children)[8]
                    
                    page_text = p.get_text()
                    pattern = re.compile('\n+')
                    page_text = pattern.sub('\n', page_text)
                    sentence_index = page_text.find('Examples')
                    if sentence_index == -1:
                        print('Sentence not found.\n')
                    else:
                        sentence = page_text[sentence_index+len('Examples'):].split('.')[0] + '.'
                        word_list[idx]['Sentence'] = sentence
                        print(sentence +'\n')
#                     print('\n')
                except:
                    print('Error occurred\n')
                    continue
            else:
                 print(item['Word'])
                 print('Sentence exists\n')   
        with open(self.filepath + 'update_Sentence.json', 'w', encoding = 'utf-8') as f:
            json.dump(word_list, f, indent = 2)
        
    def combine_word_list(self):
        with open(self.filepath + 'manhattan_500_advance.json', 'r', encoding='utf-8') as f:
            manhattan_list = json.load(f)
        
        with open(self.filepath + 'combine_memrise_manhattan_ess_500.json', 'r', encoding='utf-8') as f:
            memrise_list = json.load(f)
            
        memrise_word = [item['Word'].lower() for item in memrise_list]
        
        
        for item in manhattan_list:
            if item['Word'].lower() in memrise_word:
                pass
            else:
                memrise_list.append(item)
        print(1)
        with open(self.filepath + 'combine_memrise_manhattan_full.json', 'w', encoding = 'utf-8') as f:
            json.dump(memrise_list, f, indent = 2)
        
    def text_to_json_manhattan_essential(self):
               
        parts_of_speech = ('noun', 'pronoun', 'adj', 'verb', 'adverb', 'preposition', 'conjunction', 'interjection')
        
        with open(self.filepath + 'manhattan_500_essential.txt', 'r', encoding='utf-8') as f:
            word_list_txt = f.read()
        word_list_txt = word_list_txt.split('\n')
        word_visited = True
        pos_visited = True
        meaning_visited = True
        
        word_list_json = []
        dict_new = {'Word':'', 'Meaning':'', 'Root':'', 'Parts of speech':'',
                        'Sentence':'', 'Synonym':[], 'Antonym':[], 
                        'Notes':'', 'Rating':0, 'Star':0, 'visited':False}
        
        for line in word_list_txt:
            if line == '':
                continue
            
            line = line.lower()
           
            if '---' in line:
                print('sentence: ', line)
                word_visited = True
                dict_new['Sentence'] = line
                continue
            
            if word_visited:
                word_list_json.append(dict_new)
                dict_new = {'Word':'', 'Meaning':'', 'Root':'', 'Parts of speech':'',
                        'Sentence':'', 'Synonym':[], 'Antonym':[], 
                        'Notes':'', 'Rating':0, 'Star':0, 'visited':False}
                print('\n')
                print('word: ', line)
                pos_visited = True
                word_visited = False
                dict_new['Word'] = line
            elif pos_visited:
                print('parts of speech: ', line)
                meaning_visited = True
                pos_visited = False
                dict_new['Parts of speech'] = line
            elif meaning_visited:
                print('meaning: ', line)
                word_visited = True
                dict_new['Meaning'] = line
                word_list_json.append(dict_new)
                
        word_list_json = word_list_json[1:]
#         with open(self.filepath + 'manhattan_500_essential.json', 'w', encoding = 'utf-8') as f:
#             json.dump(word_list_json, f, indent = 2)

    def text_to_json_manhattan_advance(self):
        with open(self.filepath + 'manhattan_500_advance.txt', 'r', encoding='utf-8') as f:
            word_list_txt = f.read()
        word_list_txt = word_list_txt.split('\n')
        word_visited = True
        
        word_list_json = []

        for line in word_list_txt:
            if line == '':
                continue
            
            line = line.lower()
                       
            if word_visited:
                dict_new = {'Word':'', 'Meaning':'', 'Root':'', 'Parts of speech':'',
                        'Sentence':'', 'Synonym':[], 'Antonym':[], 
                        'Notes':'', 'Rating':0, 'Star':0, 'visited':False}
                print('\n')
                print('word: ', line)
                word_visited = False
                dict_new['Word'] = line
            else:
                print('meaning: ', line)
                word_visited = True
                dict_new['Meaning'] = line
                word_list_json.append(dict_new)
        
#         with open(self.filepath + 'manhattan_500_advance.json', 'w', encoding = 'utf-8') as f:
#             json.dump(word_list_json, f, indent = 2)
    
    def text_to_json(self):

        filepath = r'C:\Users\PRAMIT\Documents\Dropbox\python_project\Word_game\data/'
        with open(filepath + 'memrize_wordlist.txt', 'r', encoding='utf-8') as f:
            word_list_txt = f.read()
        word_list_txt = word_list_txt.split('\n')
        
        word_list_json = []
        for idx, line in enumerate(word_list_txt):
            dict_new = {'Word':'', 'Meaning':'', 'Root':'', 'Parts of speech':'',
                        'Sentence':'', 'Synonym':[], 'Antonym':[], 
                        'Notes':'', 'Rating':0, 'Star':0, 'visited':False}
            if idx % 2 != 0:
                print(line)
                dict_new['Word'] = word_list_txt[idx-1]
                dict_new['Meaning'] = line
#             else:
#                 print(line)
#                 dict_new['Meaning'] = line
                word_list_json.append(dict_new)
        
#         with open(filepath + 'memrize_wordlist.json', 'w', encoding = 'utf-8') as f:
#             json.dump(word_list_json, f, indent = 2)

    def add_info_in_dict(self):
        ''' please read method before using this method'''

#         file_path = r'C:\Users\PRAMIT\Documents\Dropbox\python_project\Word_game\data\memrize_wordlist.json'
        with open(self.filepath + 'combine_memrise_manhattan_full.json', 'r', encoding = 'utf-8') as f:
            word_list = json.load(f)
        
        word_not_found = []
        synonym_not_found = []
        antonym_not_found = []
        list_dict = []
#         short_word_list = word_list[920:]
        for idx, item in enumerate(word_list[920:]):
            idx += 920
            word = item['Word'].lower()
            if item['Parts of speech'] == '' or item['Synonym'] == []: 
                page = requests.get("https://www.merriam-webster.com/dictionary/" + word)
                soup = BeautifulSoup(page.content, 'html.parser')
            else:
                continue
            # print(soup.prettify())
            # 
            # # for www.vocabulary.com
            # # html = list(soup.children)[3]
            # # body = list(html.children)[3]
            # # p = list(body.children)[1]
            # 
            # for https://en.oxforddictionaries.com/
            # html = list(soup.children)[6]
            # body = list(html.children)[1]
            # p = list(body.children)[1]
             
            # for www.merriam-webster.com    
            html = list(soup.children)[2]
            body = list(html.children)[3]
            p = list(body.children)[1]
            
            page_text = p.get_text()#.split('\n')
            # replace multiple '\n' with a single '\n'
            p = re.compile('\n+')
            page_text = p.sub('\n', page_text)
            
            # replace multiple ' ' with single ' '
            p = re.compile(' +')
            page_text = p.sub(' ', page_text)
            page_text = page_text.split('\n')

            if item['Parts of speech'] == '':
                try:
                    Word_index = page_text.index(word)
                    page_text = page_text[Word_index:]
                    page_text = [e for e in page_text if e not in ('')]
                    pos = page_text[1].replace(' ', '')
                    if pos in ('noun', 'pronoun', 'adjective', 'verb', 'adverb', 'preposition', 'conjunction', 'interjection'):
                        print('word: ', word)
                        print('parts of speech: ', pos)
                        item['Parts of speech'] = pos
                    else:
                        raise Exception('')
                        
                except:
                    print(f'{word} is not found')
                    word_not_found.append(word)
            else:
                print(f'Parts of speech of {word} is present')
            
            if item['Synonym'] == []:
                try:
                    syn_index = page_text.index('Synonyms')+1
                    print('synonyms: ', page_text[syn_index])
                    item['Synonym'] = page_text[syn_index]
                except ValueError:
                    print(f'Synonym of {word} is not found')
                    synonym_not_found.append(word)
            else:
                print(f'Synonym of the {word} is present')
            print('\n')
            # aa = p.get_text().replace('\n\n\n\n\n\n', '\n').split('\n')
            
#             list_dict.append(item)
            word_list[idx] = item
            time.sleep(1)
            
        file_word_list = 'updated_word_list.json'
        file_synonym_not_found = 'memrise_synonym_not_found.json'
        file_word_not_found = 'memrise_word_not_found.json'
        filepath = r'C:\Users\PRAMIT\Documents\Dropbox\python_project\Word_game\data/'
        
#         with open(filepath + file_word_list, 'w', encoding = 'utf-8') as f:
#             json.dump(word_list, f, indent = 2)
#         
#         with open(filepath + file_synonym_not_found, 'w', encoding = 'utf-8') as f:
#             json.dump(synonym_not_found, f, indent = 2)
#         
#         with open(filepath + file_word_not_found, 'w', encoding = 'utf-8') as f:
#             json.dump(word_not_found, f, indent = 2)
        
        print(page_text)
        
    def update_list(self):
        file_word_list = 'updated_word_list.json'
        with open(self.filepath + file_word_list, 'r', encoding = 'utf-8') as f:
            word_list = json.load(f)
        
        count=1
        for idx, item in enumerate(word_list):
            word_list[idx].pop('Visited', None)
            
#             word_list[idx]['Rating'] = str(0)
#             word_list[idx]['Star'] = str(0)
#             word_list[idx]['visited'] = str(0)
            
#             if isinstance(item['Antonym'], list):
# #                 word_list[idx]['Synonym'] = item['Synonym'].replace(' ', '').split(',')
#                 buf = ','.join(item['Antonym'])
#                 word_list[idx]['Antonym'] = buf.replace(' ', '').split(',')

#         with open(self.filepath + file_word_list, 'w', encoding = 'utf-8') as f:
#             json.dump(word_list, f, indent = 2)

    def print_rated_word(self, rating: int = -10, show_def: bool = True):
        file_word_list = 'updated_word_list.json'
        with open(self.filepath + file_word_list, 'r', encoding = 'utf-8') as f:
            word_list = json.load(f)
            
        for idx, item in enumerate(word_list):
            if int(item['Rating']) == rating:
                if show_def:
                    print(item['Word'], '\t', item['Meaning'])
                else:
                    print(item['Word'])
                    
    def check_unwanted_rating(self):
        file_word_list = 'updated_word_list.json'
        with open(self.filepath + file_word_list, 'r', encoding = 'utf-8') as f:
            word_list = json.load(f)
            
        for idx, item in enumerate(word_list):
            if int(item['Rating']) < -10:
                print(item['Word'])

    def check_status(self):
        file_word_list = 'updated_word_list.json'
        with open(self.filepath + file_word_list, 'r', encoding = 'utf-8') as f:
            word_list = json.load(f)

        studied_count = 0
        rating_count = [0]*21
        
        for idx, item in enumerate(word_list):
            if int(item['Studied']) == 1:
                studied_count += 1
                rating_count[int(item['Rating'])+10] += 1 
        
        for idx, item in enumerate(rating_count):
            print(f'{item} words have a rating of {idx-10}')
        print(f'{studied_count} out of {len(word_list)} words have been studied')

if __name__ == '__main__':
    app = conversions()
    app.print_rated_word(rating=-7)
    