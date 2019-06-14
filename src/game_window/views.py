import tkinter as tk
from tkinter import ttk


class SelectModeFrame(ttk.Labelframe):
    ''' '''    
    def __init__(self, master):
        super().__init__(master, text = 'Select Mode')
        
        self.selection_widgets = {}
        
        selectmode_widget_keys = ('Group', 'Study', 'Game')
        selectmode_widget_texts = ('', 'Study new words', 'Play word game')
        
        for idx, key in enumerate(selectmode_widget_keys):
            if key in ('Group'):
                self.selection_widgets[key] = ttk.Combobox(self)
            else:
                self.selection_widgets[key] = ttk.Button(self, text = selectmode_widget_texts[idx])
            
        for idx, (_, widget) in enumerate(self.selection_widgets.items()):
            widget.grid(row = idx, column = 0, padx = 15, pady = 5, sticky='nsew') 
            
#     def get_variable(self):


class StudyFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.move_lbl = {}
        move_lbl_keys = {'Right':'>', 'Left':'<'}
        
        self.text_lbl = ttk.Label(self, cursor='hand2')
        for key, value in move_lbl_keys.items():
            self.move_lbl[key] = ttk.Label(self, text=value, cursor='hand2')

        
        self.text_lbl.grid(row=0, column=0, columnspan=2, ipady=25, sticky='ns')
        self.move_lbl['Left'].grid(row=1, column=0, padx=(0, 99), sticky='nw')
        self.move_lbl['Right'].grid(row=1, column=1, padx=(99, 0), sticky='ne')
        
    def set_varible(self, mode=None, text=''):
        self.text_lbl.config(text=text)


class WritingGameFrame(ttk.Frame):
    ''' '''    
    def __init__(self, master):
        super().__init__(master)
        
        self.entry_var = tk.StringVar()
        
        self.meaning_lbl = ttk.Label(self, text='')
        self.word_input = ttk.Entry(self, textvariable=self.entry_var)
        
        self.meaning_lbl.grid(row=0, column=0, pady=5, sticky='ns')
        self.word_input.grid(row=1, column=0, pady=5, sticky='ns')
        
    def set_varible(self, text=''):
        self.meaning_lbl.config(text=text)
    
    def get_variable(self):
        return self.entry_var.get()
    
    def clear_field(self):
        self.word_input.delete(0, tk.END)

class MultiChoiceGame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.choice_btn = {}
                
        self.ques_lbl = ttk.Label(self, text='')
        for idx in range(4):
            self.choice_btn[idx] = ttk.Button(self)
        
        self.ques_lbl.grid(row=0, column=0, pady=(0, 10), sticky='nw')
        for idx, widget in enumerate(self.choice_btn.values()):
            widget.grid(row=idx+1, column=0, pady=5, sticky='nsew')
        
    def set_varible(self, ques_text = '', choice_text=[], answer=0):
#         print('ans', answer)
        seq = [0, 1, 2, 3]
        self.ques_lbl.config(text=ques_text)
        while seq:
            if answer in seq:
                self.choice_btn[answer].config(text = choice_text.pop())
                seq.pop(answer)
            else:
                self.choice_btn[seq[-1]].config(text = choice_text.pop())
                seq.pop()
#         for idx in seq:
#             self.choice_btn[idx].config(text = choice_text.pop())

            
class BottomFrame(ttk.Frame):
    ''' '''
    def __init__(self, master):
        super().__init__(master)
        
        self.button_widgets = {}
        
        button_widget_keys = ('New', 'Edit', 'Delete')
        for key in button_widget_keys:
            self.button_widgets[key] = ttk.Button(self, text = key)
            
        ## - button frame
        for idx, (_, widget) in enumerate(self.button_widgets.items()):
            widget.grid(row = 0, column = idx, padx = (0, 5), pady = 0, sticky='nsew') 
            
        self.rowconfigure(0)
        self.columnconfigure(0)
