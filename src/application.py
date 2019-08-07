import tkinter as tk

from .game_window.controller import GameWindowController
from .form_window.controller import FormWindowController


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        # hide root window
        self.withdraw()

        # instantiate a dictionary of application-specific callback references 
        self.app_callbacks = {
            'game_window': self.run_game_window,
            'edit_window': self.run_edit_window,
            'quit_application': self.quit_application 
            }

        # instantiate game window controller
        self.run_game_window()
        
    ##############################
    ###    CALLBACK METHODS    ###
    ##############################
    def run_game_window(self):
        """Instantiates game selection application."""
        self.game_window = GameWindowController(self.app_callbacks)

    def run_edit_window(self, word_list, mode=None, index=None):
        '''instantiates edit form'''
        self.form_window = FormWindowController(self.app_callbacks, word_list=word_list, mode=mode, index=index)
    
    def quit_application(self):
        """Quits the application by 
        destroying the root instance."""
        # destroy root instance
        self.destroy()