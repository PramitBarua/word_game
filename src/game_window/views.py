import tkinter as tk
from tkinter import ttk


class SelectModeFrame(ttk.Labelframe):
    ''' widgets for select mode frame'''    
    def __init__(self, master):
        super().__init__(master, text = 'Select Mode')

        self.widgets = {}

        selectmode_widget_keys = ('Group', 'Study', 'Game')
        selectmode_widget_texts = ('', 'Study new words', 'Play word game')

        for idx, key in enumerate(selectmode_widget_keys):
            if key in ('Group'):
                self.widgets[key] = ttk.Combobox(self)
            else:
                self.widgets[key] = ttk.Button(self, text = selectmode_widget_texts[idx])
            
        for idx, (_, widget) in enumerate(self.widgets.items()):
            widget.grid(row = idx, column = 0, padx = 15, pady = 5, sticky='nsew') 


class StudyFrame(ttk.Frame):
    '''widgets for study frame'''
    def __init__(self, master):
        super().__init__(master)

        self.widgets = {}
        lbl_keys = {'Text':'', 'Right':'>', 'Left':'<'}

        for key, value in lbl_keys.items():
            self.widgets[key] = ttk.Label(self, text=value, cursor='hand2')

        self.widgets['Text'].grid(row=0, column=0, columnspan=2, ipady=25, sticky='ns')
        self.widgets['Left'].grid(row=1, column=0, padx=(0, 100), sticky='nw')
        self.widgets['Right'].grid(row=1, column=1, padx=(100, 0), sticky='ne')

    def set_varible(self, mode=None, text=''):
        self.widgets['Text'].config(text=text)


class WritingGameFrame(ttk.Frame):
    '''widgets for writting game frame'''
    def __init__(self, master):
        super().__init__(master)

        self.entry_var = tk.StringVar()

        self.widgets = {}

        self.widgets['Meaning lbl'] = ttk.Label(self, text='')
        self.widgets['Word Entry'] = ttk.Entry(self, textvariable=self.entry_var)

        self.widgets['Meaning lbl'].grid(row=0, column=0, pady=5, sticky='ns')
        self.widgets['Word Entry'].grid(row=1, column=0, pady=5, sticky='ns')

    def set_varible(self, text=''):
        '''set the text for question'''
        self.widgets['Meaning lbl'].config(text=text)

    def get_variable(self):
        '''get the value in the entry widget'''
        return self.entry_var.get()

    def clear_field(self):
        '''clear the entry field'''
        self.widgets['Word Entry'].delete(0, tk.END)


class MultiChoiceGame(ttk.Frame):
    '''widgets for multiple choice game frame'''
    def __init__(self, master):
        super().__init__(master)

        self.widgets = {}

        self.ques_lbl = ttk.Label(self, text='')
        for idx in range(4):
            self.widgets[idx] = ttk.Button(self)

        # place widgets
        self.ques_lbl.grid(row=0, column=0, pady=(0, 10), sticky='nw')
        for idx, widget in enumerate(self.widgets.values()):
            widget.grid(row=idx+1, column=0, pady=5, sticky='nsew')
        
    def set_varible(self, ques_text = '', choice_text=[], answer=0):
        '''sets options for multiple choice'''
        seq = [0, 1, 2, 3]
        # set the question 
        self.ques_lbl.config(text=ques_text)
        # set the choices
        while seq:
            if answer in seq:
                # place correct ans in answer index
                self.widgets[answer].config(text=f'{answer+1}. {choice_text.pop()}')
                seq.pop(answer)
            else:
                # place rest of the answer choices
                self.widgets[seq[-1]].config(text=f'{seq[-1]+1}. {choice_text.pop()}')
                seq.pop()


class BottomFrame(ttk.Frame):
    '''widgets for bottom frame (new edit and delete button)'''
    def __init__(self, master):
        super().__init__(master)

        self.widgets = {}

        widget_keys = ('New', 'Edit', 'Delete')
        for key in widget_keys:
            self.widgets[key] = ttk.Button(self, text = key)

        # place the bottom widgets
        for idx, (key, widget) in enumerate(self.widgets.items()):
            padding = 5 if key == 'Edit' else 0 
            widget.grid(row = 0, column = idx, padx = padding, pady = 0, sticky='ns') 
