import tkinter as tk

from .game_window.controller import GameWindowController
from .form_window.controller import FormWindowController


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        # hide root window
        self.withdraw()
        self.game_count = 0
        self.app_callbacks = {
            'mode_selection': self.run_mode_selection,
            'edit_window': self.run_edit_window,
            'quit_application': self.quit_application 
            }
        self.run_mode_selection()
        
    ##############################
    ###    CALLBACK METHODS    ###
    ##############################
    def run_mode_selection(self):
        """Instantiates game selection application."""
        self.game_window = GameWindowController(self.app_callbacks)

    def run_edit_window(self, index=None):
        self.form_window = FormWindowController(self.app_callbacks, index=index)
    
    def quit_application(self):
        """Quits the application by 
        destroying the root instance."""
        # destroy root instance
        self.destroy()