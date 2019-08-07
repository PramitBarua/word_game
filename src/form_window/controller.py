import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

from .. import models as m
from . import views as v


class FormWindowController(tk.Toplevel):
    def __init__(self, app_callbacks, word_list, mode=None, index=None):
        super().__init__()
        # hide window until the application is set up
        self.withdraw()
        
        if mode in ('Edit', 'Delete') and index is None:
            mb.showerror('Error', f'{mode} word is not possible from selection window')
            self.on_delete_window()
            return
        
        # place the edit window on top 
        self.grab_set()
        
        # set title
        self.title_str = mode + ' Window'
        self.title(self.title_str)
        
        #initiate model
        self.word_game_model = m.WordGameModel()
        
        # instantiate variables
        self.app_callbacks = app_callbacks
        self.word_list = word_list
        self.index = index
        
        #initiate GUI
        self._instantiate_gui()
        
#         setup callback methods
        self._setup_callbacks()

        # populate the form when the index is given
        if self.index is not None:
            self.populate_form()
        if mode == 'New':
            self.index = len(self.word_list)  

        # set window geometry
        self._set_window_geometry() 
        
        # create a protocol on deleting the window
        self.protocol("WM_DELETE_WINDOW", self.on_delete_window)
        
        # display window
        self.deiconify()
        
    #######################################
    ###    APPLICATION SETUP METHODS    ###
    #######################################        
    def _instantiate_gui(self):
        """Instantiates and allocates widgets and 
        views of the application window."""
        # instantiate widgets and views
        self.header = ttk.Label(self, text = 'Add or modify')
        self.edit_form = v.EditForm(self)
        
        # allocate widgets and views   
        self.header.grid(row = 0, column = 0, padx = (10, 10), pady = (15, 0), sticky = 'nw')
        self.edit_form.grid(row=1, column=0, padx = (0, 0), pady = (15, 15), sticky = 'nsew')

    def _setup_callbacks(self):
        """Configures widgets of the application 
        view instances to enable their functionality."""
        # bind callbacks 
        self.edit_form.ok_btn.config(command = self.on_ok_btn)
        self.edit_form.cancel_btn.config(command = self.on_delete_window) 
        
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
        
    def populate_form(self):
        '''populates widgets with values'''
        # get values of target word
        target_item = self.word_list[self.index]
        # place them in the widgets
        self.edit_form.populate_widget(target_item)

    ##############################
    ###    CALLBACK METHODS    ###
    ##############################
    def on_ok_btn(self):
        input_value = self.edit_form.get_input_values()
        if self.title_str == 'New Window':
            if input_value['Word'].lower() in [item['Word'].lower() for item in self.word_list]:
                mb.showerror('Word exist', f'"{input_value["Word"]}" exists in the list.', parent=self)
                return
            if all([input_value['Word'], input_value['Meaning'],  input_value['Parts of speech']]): pass
            else:
                field = 'Word' if input_value['Word'] == '' else 'Meaning' if input_value['Meaning'] == '' else 'Parts of speech'
                mb.showerror('Error', f'{field} field is empty.')
                return
        elif self.title_str == 'Edit Window':                
            # check if word, meaning, and parts of speech widgets are filled
            if all([input_value['Word'], input_value['Meaning'], input_value['Parts of speech']]): pass
            else:
                field = 'Word' if input_value['Word'] == '' else 'Meaning' if input_value['Meaning'] == '' else 'Parts of speech'
                mb.showerror('Error', f'{field} field is empty.')
                return
            input_value['Group'] = self.word_list[self.index]['Group']

        else:  # user pressed delete button 
            if self.index is None:
                mb.showerror(f'Deleting is not possible from selection window')
                return
            input_value['Group'] = self.word_list[self.index]['Group']
            # get the index which will be deleted
            index = [idx for idx, item in enumerate(self.word_list)
                     if item['Word'].lower() == input_value['Word'].lower()]
            if index:
                # make a final check up
                result = mb.askokcancel('Delete', f'Do you really want to delete {input_value["Word"]}?')
                if result:
                    self.index = index[0]
                    input_value = None
                else: return  # user changes mind 
            
            else:  # word does not exist in the list
                message = f'{input_value["Word"]} does not exist in the list' if input_value['Word'] !='' else 'Word field is empty'
                mb.showerror('Invalid Input', message)
                return
        # execute word removal action
        self.word_game_model.save_word_list(window = self.title_str, index=self.index, data=input_value, word_list=self.word_list)
        # destroy window
        self.on_delete_window()
    
    ##############################
    ###    PROTOCOL METHODS    ###
    ##############################
    def on_delete_window(self):
        """Executes the 'quit_application' callback method 
        of the application instance."""
        # make the bottom top-level workable
        self.grab_release()
        
        # destroy controller instance
        self.destroy()
