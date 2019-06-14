import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

from .. import models as m
from . import views as v


class FormWindowController(tk.Toplevel):
    def __init__(self, app_callbacks, index=None):
        super().__init__()
        # hide window until the application is set up
        self.withdraw()
        
        self.grab_set()
        self.title('Add/Edit window')
        
        #initiate model
        self.word_game_model = m.WordGameModel()
        
        # instantiate variables
        self.app_callbacks = app_callbacks
        self.word_list = self.word_game_model.get_word_list()
        self.index = index
        
        #initiate GUI
        self._instantiate_gui()
        
#         setup callback methods
        self._setup_callbacks()

        # populate form when index is given
        if self.index is not None:
            self.populate_form()
        else:
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
        
        # select game callbacks
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
        target_item = self.word_list[self.index]
        self.edit_form.populate_widget(target_item)

    ##############################
    ###    CALLBACK METHODS    ###
    ##############################
    def on_ok_btn(self):
#         print('Ok btn is pressed')
        input_value = self.edit_form.get_input_values()
#         print(input_value)
        if all([input_value['Word'], input_value['Meaning'],  input_value['Parts of speech']]):
            self.word_game_model.save_word_list(index=self.index, data=input_value)
            # destroy window
            self.grab_release()
            self.destroy()
        else:
            mb.showerror('Error', 'Any of the three field (Word, Meaning, Part of speech) is empty.')
    
    ##############################
    ###    PROTOCOL METHODS    ###
    ##############################
    def on_delete_window(self):
        """Executes the 'quit_application' callback method 
        of the application instance."""
        # make the bottom top level workable
        self.grab_release()
        
        # destroy controller instance
        self.destroy()
        
#         # quit application via callback or by self.quit()
#         if 'quit_application' in self.app_callbacks:
#             self.app_callbacks['quit_application']()  
#         else:
#             self.quit()  