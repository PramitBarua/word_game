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
        self.header = ttk.Label(self)
        self.mode_selection = v.SelectModeFrame(self)
        self.study_frame = v.StudyFrame(self)
        self.writing_game = v.WritingGameFrame(self)
        self.multi_choice_game = v.MultiChoiceGame(self)
        self.bottom_frame = v.BottomFrame(self)

        # instantiate variables
        self.app_callbacks = app_callbacks
        self.word_list = self.word_game_model.get_word_list()
        self._index = None
        self.game_count = 0

        self.unique_group = ['']
        for item in self.word_list:
            if item['Group'] not in self.unique_group:
                self.unique_group.append(item['Group'])
                        
        # create a protocol on deleting the window
        self.protocol("WM_DELETE_WINDOW", self.on_delete_window)
        
        self._instantiate_mode_selection()
        self._setup_callbacks_bottom_frame()
        self._set_window_geometry()
        
    ##################################
    ###    COMMON SETUP METHODS    ###
    ##################################    
    def _setup_callbacks_bottom_frame(self):
        """Configures widgets of the application 
        view instances to enable their functionality."""
        # add edit and delete callback
        self.bottom_frame.button_widgets['New'].config(command=self.on_new_btn)
        self.bottom_frame.button_widgets['Edit'].config(command=self.on_edit_btn)
        self.bottom_frame.button_widgets['Delete'].config(command=self.on_delete_btn)
        
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
        
    def _grid_check(self):
        if bool(self.mode_selection.grid_info()):
            self.mode_selection.grid_forget()
        elif bool(self.study_frame.grid_info()):
            self.study_frame.grid_forget()
        elif bool(self.writing_game.grid_info()):
            self.writing_game.grid_forget()
        elif bool(self.multi_choice_game.grid_info()):
            self.multi_choice_game.grid_forget()
        
    ##########################################
    ###    GAME SELECTION SETUP METHODS    ###
    ##########################################        
    def _instantiate_mode_selection(self):
        """Instantiates and allocates widgets and 
        views of the application window."""
        
        self._grid_check()
        
        # set the title of the window
        self.title_str = 'Mode Selection'
        self.title(self.title_str)
        # instantiate widgets and views
        self.header.config(text = 'Welcome to the word game')
        
        # allocate widgets and views   
        self.header.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = 'nw')
        self.mode_selection.grid(row=1, column=0)
        self.bottom_frame.grid(row=2, column=0, padx = (20, 10), pady = (20, 15), sticky = 'ns')

        # initiate game callback
        for key, widget in self.mode_selection.selection_widgets.items():
            if widget.winfo_class() in ('TButton'):
                widget.config(command=lambda mode=key: self.mode_controller(mode))
            elif widget.winfo_class() in ('TCombobox'):
                widget.config(values=self.unique_group)
                widget.current(1)
                
    def mode_controller(self, mode=None):
        self._index = 0
        self.flip_state = False
        current_study_group = self.mode_selection.selection_widgets['Group'].get()
        if mode == 'Study':   
            if current_study_group == '':
                mb.showerror('Group Select', 'Please select a group to study')  
            else:              
                self.index_list = [self.word_list.index(item) for item in self.word_list if item['Group'] == current_study_group]
                self._instantiate_study_mode()
                self._set_window_geometry()
        else:
            hard_word_index = [self.word_list.index(item) for item in self.word_list if item['Rating'] in ('-2', '-3', '-4', '-5')]
            studied_word_index = [self.word_list.index(item) for item in self.word_list if item['Studied'] in ('1')]
        
            if len(hard_word_index) >= 25:
                self.index_list = hard_word_index
                self.run_game()
            elif current_study_group != '':
                self.index_list = [self.word_list.index(item) for item in self.word_list if item['Group'] == current_study_group]
                self.run_game()
            elif len(studied_word_index) >= 25:
#                 self.selected_game = 'random'
                self.index_list = studied_word_index
                self.run_game()
            else:
                mb.showinfo('Study more', 'Please study more words before play.')
         
    def run_game(self):        
        if self.game_count < 14:
            if randint(-9, 5) > 0:
                self._instantiate_writing_game()
            else:
                self._instantiate_multi_choice_game()
            self._set_window_geometry()
            self.game_count += 1
        else:
            self.game_count = 0
            self._instantiate_mode_selection()
            self._set_window_geometry()

    ######################################
    ###    STUDY MODE SETUP METHODS    ###
    ######################################    
    def _instantiate_study_mode(self):
        self._grid_check()
        
        # set the title of the window
        self.title_str = 'Study New Words'
        self.title(self.title_str)

        # set label text
        word_dict = self.word_list[self.index_list[self._index]]
        if not self.flip_state:
            # set heading
            header_text = 'Click to see definition'            
            self.len_header = len(header_text)
            text = word_dict['Word']
        else:
            header_text = 'Click to see term'
            self.len_header = len(header_text)
            buf_list = ["\n".join(wrap(value, self.len_header)) for key, value in word_dict.items() if key in ('Meaning', 'Parts of speech')]
            text = '\n\n'.join(buf_list)

        # instantiate widgets and views
        self.header.config(text=header_text)
        self.study_frame.set_varible(text=text)
 
        # allocate header and bottom frame
        self.header.grid(row = 0, column = 0, padx = 20, pady = (20, 0), sticky = 'nw')
        self.bottom_frame.grid(row=2, column=0, padx = 10, pady = (20, 15), sticky = 'nsew')
        self.study_frame.grid(row=1, column=0, padx = 20, sticky='nsew')
        
        self.study_frame.text_lbl.bind('<Button-1>', self.on_flip)
        for key, widget in self.study_frame.move_lbl.items():
            widget.bind('<Button-1>', lambda event, btn=key: self.on_move_lbl(btn))

    ######################################
    ###   WRITING GAME SETUP METHODS   ###
    ######################################        
    def _instantiate_writing_game(self):
        """Instantiates and allocates widgets and 
        views of the application window."""
        
        self._grid_check()
        
        # set the title of the window
        self.title_str = 'Writing Word'
        self.title(self.title_str)

        # set heading
        header_text = 'Can you guess the correct word for the following meaning?'
        self.len_header = len(header_text)
        
        # instantiate widgets and views
        self.header.config(text=header_text)
        
        # allocate header and bottom frame
        self.header.grid(row = 0, column = 0, padx = (20, 10), pady = (20, 15), sticky = 'nw')
        self.bottom_frame.grid(row=2, column=0, padx = (55, 10), pady = (20, 15), sticky = 'nsew')
        
        # set label text
        self._index = random.choice(self.index_list)
        text = self.word_list[self._index]['Meaning']
        if len(text)>= self.len_header:
            text = "\n".join(wrap(text, self.len_header-5))

        self.writing_game.set_varible(text=text)
        
        # grid writing game in the middle of the window
        self.update_idletasks()
        padding = (self.winfo_reqwidth() - self.writing_game.winfo_reqwidth())//2
        
        # allocate middle frame
        self.writing_game.grid(row=1, column=0, padx = (padding, 0), sticky='nsew')
        
        self.writing_game.word_input.bind('<Return>', self.on_writing_check)
        
    ###########################################
    ###   MULTI CHOICE GAME SETUP METHODS   ###
    ###########################################        
    def _instantiate_multi_choice_game(self):
        """Instantiates and allocates widgets and 
        views of the application window."""
        
        self._grid_check()
        
        # set the title of the window
        self.title_str = 'Multiple Choice'
        self.title(self.title_str)
        
        if randint(0, 1) == 0:
            header_text = 'What is the meaning of the following word?'
            ans_choice = 'Meaning'
            question = 'Word'
        else:
            header_text = 'What is the word that means as follows?'
            ans_choice = 'Word'
            question = 'Meaning'

        self.len_header = len(header_text)
        
        # instantiate widgets and views
        self.header.config(text=header_text)
        
        # allocate header and bottom frame
        self.header.grid(row = 0, column = 0, padx = (20, 20), pady = (20, 10), sticky = 'nw')
        self.bottom_frame.grid(row=2, column=0, padx = (20, 20), pady = (20, 15), sticky = 'nsew')
        
        # set label text
        choice_text = []
        for idx in range(4):
            self._index = random.choice(self.index_list)
            buf_text = self.word_list[self._index][ans_choice]
            choice_text.append("\n".join(wrap(buf_text, self.len_header-5)))
                
        self.multi_choice_ans = randint(0, 3)
        ques_text = "\n".join(wrap(self.word_list[self._index][question], self.len_header-5))
        self.multi_choice_game.set_varible(ques_text = ques_text, choice_text=choice_text, answer=self.multi_choice_ans)
        
        # grid writing game in the middle of the window
        self.update_idletasks()
        padding = (self.winfo_reqwidth() - self.multi_choice_game.winfo_reqwidth())//2
        
        # allocate middle frame
        self.multi_choice_game.grid(row=1, column=0, padx = (padding, 0), sticky='nsew')

        # initiate btn callback
        for idx, widget in self.multi_choice_game.choice_btn.items():
            widget.config(command=lambda m=idx: self.on_multi_selection(m))
        
    ##############################
    ###    CALLBACK METHODS    ###
    ##############################
    def on_new_btn(self):
        self.app_callbacks['form_window']()
        
    def on_edit_btn(self):
        self.app_callbacks['form_window'](index=self._index)
        
    def on_delete_btn(self):
        self.app_callbacks['form_window'](index=self._index)
        
    def on_flip(self, event=None):
        self.flip_state = not self.flip_state
        data = self.word_list[self.index_list[self._index]].copy()
        data['Studied'] = '1'
        self.word_game_model.save_word_list(index=self.index_list[self._index], data=data)
        self._instantiate_study_mode()
        self._set_window_geometry()
        
    def on_move_lbl(self, btn=None, event=None):
        if btn == 'Right':
            if self._index == len(self.index_list)-1:
                self._index = 0
            else:
                self._index += 1
        else:
            if self._index == 0:
                self._index = len(self.index_list)-1
            else:
                self._index -= 1
        self.flip_state = False
        self._instantiate_study_mode()
        self._set_window_geometry()
        
    def on_multi_selection(self, button = None):
#         print(button)
        data = self.word_list[self._index].copy()
#         self.word_game_model.save_word_list(index=self._index, data=data)
        if button == self.multi_choice_ans:
            if data['Rating'] != 5:
                data['Rating'] = str(int(data['Rating'])+1)
        else:
            if data['Rating'] != -5:
                data['Rating'] = str(int(data['Rating'])-1)
            result = mb.askokcancel('Question', 'The answer is incorrect. Would you like to review the answer?', default='ok')
            if result:
                message = [f'{key}: {value}\n' for key, value in data.items() if value != '']
                mb.showinfo('Word', '\n'.join(message))
        self.word_game_model.save_word_list(index=self._index, data=data)
        self.run_game()
        
    def on_writing_check(self, event=None):
        user_input = self.writing_game.get_variable()
        data = self.word_list[self._index].copy()
        if user_input.lower() == data['Word'].lower():
            if data['Rating'] != 5:
                data['Rating'] = str(int(data['Rating'])+1)
        else:
            if data['Rating'] != -5:
                data['Rating'] = str(int(data['Rating'])-1)
            result = mb.askokcancel('Question', 'The answer is incorrect. Would you like to review the answer?', default='ok')
            if result:
                message = [f'{key}: {value}\n' for key, value in data.items() if value != '']
                mb.showinfo('Word', '\n'.join(message))
        self.writing_game.clear_field()
        self.word_game_model.save_word_list(index=self._index, data=data)
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
            self._instantiate_mode_selection()
            self._set_window_geometry()
        elif self.title_str == 'Game Selection':
            result = mb.askokcancel('Quit', 'Do you want to terminate the program?')
            if result:
                # destroy controller instance
                self.destroy()
                self.app_callbacks['quit_application']()  
        else:
            self.quit()  