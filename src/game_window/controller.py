import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import random
from random import randint
from textwrap import wrap


from .. import models as m
from . import views as v


class GameWindowController(tk.Toplevel):
    def __init__(self, app_callbacks):
        super().__init__()

        # hide window until the application is set up
        self.withdraw()
        
        # initiate model
        self.word_game_model = m.WordGameModel()
        
        # initiate views
        self.middle_frame = {}
        
        self.header = ttk.Label(self)
        self.middle_frame['Selection Mode'] = v.SelectModeFrame(self)
        self.middle_frame['Study New Words'] = v.StudyFrame(self)
        self.middle_frame['Writing Word'] = v.WritingGameFrame(self)
        self.middle_frame['Multiple Choice'] = v.MultiChoiceGame(self)
        self.bottom_frame = v.BottomFrame(self)

        # instantiate variables
        self.app_callbacks = app_callbacks
        self.word_list = self.word_game_model.get_word_list()
        self._initiate_variable()

        # get group names from json
        for item in self.word_list:
            if item['Group'] not in self.unique_group:
                self.unique_group.append(item['Group'])

        # create a protocol on deleting the window
        self.protocol("WM_DELETE_WINDOW", self.on_delete_window)

        # initiate welcome window
        self._instantiate_gui(frame_name = 'Selection Mode')
        self._setup_callbacks_bottom_frame()
        self._set_window_geometry()
        
    ##################################
    ###    COMMON SETUP METHODS    ###
    ##################################    
    def _initiate_variable(self):
        '''define default values for the program'''
        self._index = None                                      # keep tracks of the current item/dict of list
        self.game_count = 0                                     # keep tracks of the number of game has played 
        self.index_list = []                                    # keep index of dicts
        self.unique_group = ['']                                # keep the name of the groups that words belong
        self.index_tested = []                                  # keep track of the index of the tested word
        self.chunk = 25                                         # number of word to study/practice in one session
    
    def _setup_callbacks_bottom_frame(self):
        """Configures widgets of the application 
        view instances to enable their functionality."""
        # add new, edit and delete callback
        for key, widget in self.bottom_frame.widgets.items():
            widget.config(command=lambda btn=key: self.on_bottom_btn(btn))
        
    def _set_window_geometry(self):
        """Places the application window
        in the center of the screen."""
        # define width offset and height offset variables as correction factors for window header and frame
        offset_width, offset_height = -16, -68
        # update idle tasks to make sure that the widget size will be appropriate
        self.update_idletasks()
        # retrieve requested window width and height
        width, height = self.winfo_reqwidth(), self.winfo_reqheight()
        # retrieve screen width and height
        screen_width, screen_height = self.winfo_screenwidth() + offset_width, self.winfo_screenheight() + offset_height
        # calculate x,y- coordinates of the window
        x, y = int((screen_width - width)/2), int((screen_height - height)/2)        
        # place the window at the required position
        self.geometry(f"{width}x{height}+{x}+{y}")
        # set window minimum size
        self.minsize(width, height) 
        
        # display window
        self.deiconify()
        
    ##########################################
    ###    GAME SELECTION SETUP METHODS    ###
    ##########################################        
    def _instantiate_gui(self, frame_name):
        """Instantiates and allocates widgets and 
        views of the application window."""
        
        # grid remove previously grid widget and frame
        self.header.grid_remove()
        self.bottom_frame.grid_forget()
        
        for frame in ('Selection Mode', 'Study New Words', 'Writing Word', 'Multiple Choice'):
            # check which frame is active from previous run
            if bool(self.middle_frame[frame].grid_info()):
                # Remove the view from the grid manager
                self.middle_frame[frame].grid_forget()
                # if prevous run is multiple choice game
                if frame == 'Multiple Choice':
                    # remove the binding events from toplevel
                    for idx in range(4):
                        self.unbind(f'{idx}')
                # one out of four views can be alive at a 
                # time therefore it is unnecessary to check all
                break
        
        if frame_name == 'Selection Mode':
            # define header text
            header_text = 'Welcome to the word game'
            # initiate callback for selection mode
            self.middle_frame[frame_name].widgets['Study'].config(command=self.on_study_btn)
            self.middle_frame[frame_name].widgets['Game'].config(command=self.on_game_btn)
            self.middle_frame[frame_name].widgets['Group'].config(values=self.unique_group)
            self.middle_frame[frame_name].widgets['Group'].current(1)
            # initiate binds for selection mode
            self.middle_frame[frame_name].widgets['Study'].bind('<Return>', self.on_study_btn)
            self.middle_frame[frame_name].widgets['Game'].bind('<Return>', self.on_game_btn)
        
        elif frame_name == 'Study New Words':
            # get specific dict from word_list
            word_dict = self.word_list[self._index]
            
            if not self.flip_state:                 # while the card is in 'word showing' state
                # set heading
                header_text = 'Click to see definition'            
                len_header = len(header_text)
                # display word in the card
                text = word_dict['Word']
            else:                                   # while the card is in 'definition showing' state
                # set heading
                header_text = 'Click to see term'
                len_header = len(header_text)
                # wrap the displaying text based on header length
                buf_list = ["\n".join(wrap(value, 2*len_header)) for key, value in word_dict.items() if key in ('Meaning', 'Parts of speech', 'Sentence')]
                # display the meaning, parts of speech and sentence in the card
                text = '\n\n'.join(buf_list)
                
            # display text in the middle frame
            self.middle_frame[frame_name].set_varible(text=text)
            
            # initiate binds for study mode
            self.middle_frame[frame_name].widgets['Right'].bind('<Button-1>', lambda event, btn='Right': self.on_move_lbl(btn))
            self.middle_frame[frame_name].widgets['Left'].bind('<Button-1>', lambda event, btn='Left': self.on_move_lbl(btn))
            self.middle_frame[frame_name].widgets['Text'].bind('<Button-1>', self.on_flip)
        
        elif frame_name == 'Writing Word':
            # set heading
            header_text = 'Can you guess the correct word for the following meaning?'
            len_header = len(header_text)
            
            # choose a random word from the list
            self._index = random.choice(self.index_list)
            # provide priority for unlearned word
            self.prefer_unlearned()
            # get the definition of the word
            text = self.word_list[self._index]['Meaning']
            # make text adjustment according to header length
            if len(text)>= len_header:
                text = "\n".join(wrap(text, len_header-5))
            # set the text in the frame
            self.middle_frame[frame_name].set_varible(text=text)
            
            # initiate binds for writing game entry widget
            self.middle_frame[frame_name].widgets['Word Entry'].bind('<Return>', self.on_writing_check)
        
        elif frame_name == 'Multiple Choice':
            if randint(0, 1) == 0:                      # ask the definition of a word
                header_text = 'What is the meaning of the following word?'
                ans_choice = 'Meaning'
                question = 'Word'
            else:                                       # guess the word from definition
                header_text = 'What is the word that means as follows?'
                ans_choice = 'Word'
                question = 'Meaning'
    
            len_header = len(header_text)

            # holds the text for multiple choice options
            choice_text = []
            while(len(choice_text) != 4):
                if len(self.index_tested) > 4:
                    self._index = random.choice(self.index_tested)
                else:
                    self._index = random.choice(self.index_list)

                if len(choice_text) == 3:  # last choice will be asked as question
                    self._index = random.choice(self.index_list)
                    # provide priority for unlearned word
                    self.prefer_unlearned()
                # get desire text (word/definition) from word list
                buf_text = self.word_list[self._index][ans_choice]
                buf_text = "\n".join(wrap(buf_text, len_header-5))
                # prevent repetition in answer choice
                if buf_text not in choice_text:  
                    # wrap text based on header 
                    choice_text.append(buf_text)
            # get the index where the answer will be displayed
            self.multi_choice_ans = randint(0, 3)
            # get the question text
            ques_text = "\n".join(wrap(self.word_list[self._index][question], len_header-5))
            # set the question and choices in the frame
            self.middle_frame[frame_name].set_varible(ques_text = ques_text, choice_text=choice_text, answer=self.multi_choice_ans)

            # initiate btn callback
            for idx, widget in self.middle_frame[frame_name].widgets.items():
                # select by clicking 
                widget.config(command=lambda m=idx: self.on_multi_selection(m))
                # select choice by key board navigation and press enter
                widget.bind('<Return>', lambda event, m=idx: self.on_multi_selection(m))
                # select choice by pressing (1, 2, 3, 4) button in key board
                self.bind(f'{idx+1}', lambda event, m=idx: self.on_multi_selection(m))

        if self._index is not None and self._index not in self.index_tested:
            # keep track of tested word
            self.index_tested.append(self._index)
        
        # set the window title.
        self.title_str = frame_name
        self.title(self.title_str)
        # set header text 
        self.header.config(text=header_text)

        # grid header
        self.header.grid(row = 0, column = 0, padx = 20, pady = (20, 10), sticky = 'nw')

        self.update_idletasks()
        # grid middle frame by placing appropriate padding
        padding = (self.winfo_reqwidth() - self.middle_frame[frame_name].winfo_reqwidth())//2
        padding = padding if padding>0 else 10
        self.middle_frame[frame_name].grid(row=1, column=0, padx = padding, pady = 10, sticky='ns')
        # grid bottom frame by placing appropriate padding
        padding = (self.winfo_reqwidth() - self.bottom_frame.winfo_reqwidth())//2
        padding = padding if padding>0 else 10
        self.bottom_frame.grid(row=2, column=0, padx = padding, pady = 10, sticky = 'ns')
         
    def run_game(self):
        ''' defines which game will initiate'''
        if self.game_count < self.chunk:
            if randint(0, 1) > 0:                       # 50% chance to writing game
                # initiate writing game
                self._instantiate_gui(frame_name='Writing Word')
            else:                                       # 50% chance to multiple choice game
                # initiate multiple choice game
                self._instantiate_gui(frame_name='Multiple Choice')
            # set window in the middle of screen
            self._set_window_geometry()
            self.game_count += 1
        else:
            # when one session is finished
            result = mb.askokcancel('Well done', f'You have reviewed {self.chunk} words. Would you like to review more words?', parent=self)
            # when one session is finish and user wants to review more
            if result:
                # user wants to review more words
                self._initiate_variable()
                self.on_game_btn()
            else:
                self.on_delete_window()                

    def prefer_unlearned(self):
        ''' Focus more on low rated word'''
        while(True):
#             print('in infinite loop')
            if self._index in self.index_tested:
                self.index_list.remove(self._index)
                self._index = random.choice(self.index_list)
                continue
            
            if int(self.word_list[self._index]['Rating']) < 7:
                break
            else:                
                # if word rating is high
                if randint(-2, 1) > 0:
                    # 25% chance of accepting a high rated word
                    break
                else:
                    # pick another word
                    self._index = random.choice(self.index_list)
    
    ##############################
    ###    CALLBACK METHODS    ###
    ##############################
    def on_bottom_btn(self, btn):
        '''define action on pressing any of the
        button (new, edit, delete) in the bottom frame'''
        if btn == 'New':
            # call edit window without index
            self.app_callbacks['edit_window'](word_list=self.word_list, mode=btn, index=None)
        else:
            # call edit window with index and display content in the widgets of the window
            self.app_callbacks['edit_window'](word_list=self.word_list, mode=btn, index=self._index)

    def on_study_btn(self, event=None):
        '''when "Study New Words" button is pressed'''
        # start from the 1st dict of the word group
        self.counter = 0
        # show word initially
        self.flip_state = False
        # get which group to study
        current_study_group = self.middle_frame['Selection Mode'].widgets['Group'].get()
        if current_study_group == '':
            # without selecting group; program selects all previously studied words
            studied_word_index = [self.word_list.index(item) for item in self.word_list if item['Studied'] in ('1')] 
            if len(studied_word_index) < self.chunk:
                # when a few words have studied (<25) then program will not run
                message = f'You have studied less than {self.chunk} words. Please study more words'
                mb.showerror('Group Select', message, parent=self)
                return
            self.index_list = random.choices(studied_word_index, self.chunk)
        else:
            # get the index of the dicts of the group and place them in a list
            self.index_list = [self.word_list.index(item) for item in self.word_list if item['Group'] == current_study_group]
            if [self.word_list[idx]['Studied'] for idx in self.index_list].count('1') == len(self.index_list):
                result = mb.askokcancel('Group studied', 'You have studied this group. Would you like to study again?')
                if not result:
                    return
        # get the current word index
        self._index = self.index_list[self.counter]
        # initiate study gui
        self._instantiate_gui(frame_name='Study New Words')
        # place the window in the middle of the screen
        self._set_window_geometry()

    def on_flip(self, event=None):
        '''when user presses on the card'''
        # toggle the state of word and definition
        self.flip_state = not self.flip_state
        # make a copy of the current dict
        data = self.word_list[self.index_list[self.counter]].copy()
        if data['Studied'] == '0':
            # change the studied key to 1
            data['Studied'] = '1'
            # change the rating to -2
            data['Rating'] = '-8'
        # save the updated word list
        self.word_game_model.save_word_list(window='Edit Window', index=self._index, data=data, word_list=self.word_list)
        # show the definition card
        self._instantiate_gui(frame_name='Study New Words')
        # place the window in the middle of the window
        self._set_window_geometry()

    def on_move_lbl(self, btn=None, event=None):
        '''when user presses left or right in the study window'''
        if btn == 'Right':
            # if user presses right
            if self.counter == len(self.index_list)-1:
                # if current item is the last item of
                # the list then show the 1st item
                self.counter = 0
            else:
                self.counter += 1
        else:
            if self.counter == 0:
                # if current item is the first item of
                # the list then show the last item
                self.counter = len(self.index_list)-1
            else:
                self.counter -= 1
        # show word
        self.flip_state = False
        # get the index of the current word
        self._index = self.index_list[self.counter]
        # show the word card
        self._instantiate_gui(frame_name='Study New Words')
        self._set_window_geometry()

    def on_game_btn(self, event=None):
        '''when user presses "play word game" btn'''
        # get which group to study
        current_study_group = self.middle_frame['Selection Mode'].widgets['Group'].get()
        # get the index of hard words (which rating is less than -3)
        hard_word_index = [self.word_list.index(item) for item in self.word_list if int(item['Rating']) < -3]
        # get the index of studied word
        studied_word_index = [self.word_list.index(item) for item in self.word_list if item['Studied'] in ('1')]

        if len(hard_word_index) >= 25:
            # when the number of hard word is more then 24
            self.index_list = hard_word_index
            # update chuck size
            self.chunk = len(self.index_list)
        elif current_study_group != '':
            # when user wants to review a particular group
            self.index_list = [self.word_list.index(item) for item in self.word_list if item['Group'] == current_study_group]
            if [self.word_list[idx]['Studied'] for idx in self.index_list].count('0') == len(self.index_list):
                mb.showinfo('Did not study', 'You have not studied this group. Please study this group before playing.')
                return
            # update chunk size
            self.chunk = len(self.index_list)
        elif len(studied_word_index) >= 25:
            # when user wants to review the studied words
            self.index_list = studied_word_index
            # update chuck size (take 30% of studied word)
            self.chunk = len(self.index_list)*3//10
        else:
            # if user have not studied more then 25 words
            mb.showinfo('Study more', 'Please study more words before play.', parent=self)
            return
        # shuffle the list to get a true randomize game play
        random.shuffle(self.index_list)
        # start game 
        self.run_game()

    def on_multi_selection(self, button = None, event=None):
        '''when user select an answer from the options'''
        # copy the dict of the target word
        data = self.word_list[self._index].copy()
        # if user chooses the right answer
        if button == self.multi_choice_ans:
            if data['Rating'] != '10':
                # increase rating by one when the rating of the word is not highest
                data['Rating'] = str(int(data['Rating'])+1)
        else:           # user chooses the wrong answer
            if self.index_tested and self.index_tested[-1] == self._index:  # list is not empty and last item is index
                # remove the index from the test list therefore it can be check again
                self.index_tested.pop()
                self.game_count -= 1
            message = [f'{key}: {value}\n' for key, value in data.items() if value != '']
            result = mb.askyesno('Word', '\n'.join(message), parent=self)
            if not result:
                return
            if data['Rating'] == '-9':
                # if the rating is '-9' decrease rating by 1
                data['Rating'] = str(int(data['Rating'])-1)
            elif data['Rating'] != '-10':
                # decease rating by 2
                data['Rating'] = str(int(data['Rating'])-2)
        # save modified rating
        self.word_game_model.save_word_list(window='Edit Window', index=self._index, data=data, word_list=self.word_list)
        # run next game
        self.run_game()

    def on_writing_check(self, event=None):
        '''when user types word in the entry field and press entry'''
        # get user input
        user_input = self.middle_frame['Writing Word'].get_variable().lower()
        # copy the dict of the target word
        data = self.word_list[self._index].copy()
        # if user chooses the right answer
        if user_input == data['Word'].lower():
            if data['Rating'] != '10':
                # increase rating by one when the rating of the word is not highest
                data['Rating'] = str(int(data['Rating'])+1)
        elif user_input != '' and user_input in data['Synonym']:
            # if user ans is a synonym of the asked word
            mb.showinfo('Not the word', 'You wrote a synonym. Please guess again.', parent=self)
            return
        else:
            if self.index_tested and self.index_tested[-1] == self._index:  # list is not empty and last item is index
                # remove the index from the test list therefore it can be check again
                self.index_tested.pop()
                self.game_count -= 1
            message = [f'{key}: {value}\n' for key, value in data.items() if value != '']
            result = mb.askyesno('Word', '\n'.join(message), parent=self)
            if not result:
                return
            # user gave incorrect ans
            if data['Rating'] == '-9':
                # if the rating is '-9' decrease rating by 1
                data['Rating'] = str(int(data['Rating'])-1)
            elif data['Rating'] != '-10':
                # increase rating by two
                data['Rating'] = str(int(data['Rating'])-2)
        # clear entry field
        self.middle_frame['Writing Word'].clear_field()
        # save updated rating
        self.word_game_model.save_word_list(window='Edit Window', index=self._index, data=data, word_list=self.word_list)
        # run next game
        self.run_game()

    ##############################
    ###    PROTOCOL METHODS    ###
    ##############################
    def on_delete_window(self):
        """Executes the 'quit_application' callback method 
        of the application instance."""

        # quit application via callback or by self.quit()
        if self.title_str in ('Study New Words', 'Writing Word', 'Multiple Choice'):
            self.game_count = 0
            self._index = None
            self.index_tested = []
            self.destroy()
            self.app_callbacks['game_window']()
        elif self.title_str == 'Selection Mode':
            result = mb.askokcancel('Quit', 'Do you want to terminate the program?', parent=self)
            if result:
                # destroy controller instance
                self.destroy()
                self.app_callbacks['quit_application']()  
        else:
            self.quit()  