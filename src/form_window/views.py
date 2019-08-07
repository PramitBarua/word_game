import tkinter as tk
from tkinter import ttk


class EditForm(ttk.Frame):
    '''widgets for edit window'''    
    def __init__(self, master):
        super().__init__(master)

        lbl_widget = {}         # contains the labels in the form
        self.input_widget = {}  # contains the wigets in the form

        combo_widget_frame = ttk.Frame(self)  # contians combo widgets

        # define entry widgets
        entry_widget_keys = ('Word', 'Parts of speech', 'Root')
        # define text widgets
        text_widget_keys = ('Meaning', 'Sentence', 'Synonym', 'Antonym', 'Notes')
        # define combobox widgets
        comb_widget_keys = ('Rating', 'Star', 'Studied')

        # define options for various widgets
        opts = {'Parts of speech':{"values": ['Noun', 'Verb', 'Adjective', 'Adverb',
                                             'Pronoun', 'Preposition', 'Conjunction', 'Interjection']},
                'Rating':         {'values': list(range(-10, 11)), 'width': 26},
                'Star':           {'values': list(range(0, 2)), 'width': 28},
                'Studied':        {'values': list(range(0, 2)), 'width': 26}
                }
        # iterate over the widgets
        for key in entry_widget_keys+text_widget_keys+comb_widget_keys:
            if key in entry_widget_keys:
                lbl_widget[key] = ttk.Label(self, text = key)
                self.input_widget[key] = ttk.Entry(self, textvariable=tk.StringVar())
            if key in text_widget_keys:
                lbl_widget[key] = ttk.Label(self, text = key)
                self.input_widget[key] = tk.Text(self, width=35, height=3, wrap="word")  
            if key in comb_widget_keys:
                lbl_widget[key] = ttk.Label(combo_widget_frame, text = key)
                self.input_widget[key] = ttk.Combobox(combo_widget_frame, **opts[key])  

        # define ok and cancel button
        self.ok_btn = ttk.Button(self, text='Ok')
        self.cancel_btn = ttk.Button(self, text='Cancel')

        # place labels in the grid
        opts = {'padx':10, 'pady':(10, 0)}
        lbl_widget['Word'].grid(row=0, column=0, sticky='nw', **opts)
        lbl_widget['Parts of speech'].grid(row=0, column=2, sticky='nw', **opts)
        lbl_widget['Root'].grid(row=0, column=3, sticky='nw', **opts)
        lbl_widget['Meaning'].grid(row=2, column=0, sticky='nw', **opts)
        lbl_widget['Sentence'].grid(row=4, column=0, sticky='nw', **opts)

        lbl_widget['Synonym'].grid(row=8, column=0, sticky='nw', **opts)
        lbl_widget['Antonym'].grid(row=8, column=2, sticky='nw', **opts)
        lbl_widget['Notes'].grid(row=10, column=0, sticky='nw', **opts)

        # place widgets in the grid
        opts = {'padx':10, 'pady':0}
        self.input_widget['Word'].grid(row=1, column=0, columnspan=2, sticky='ew', **opts)
        self.input_widget['Root'].grid(row=1, column=3, sticky='ew', **opts)
        self.input_widget['Parts of speech'].grid(row=1, column=2, sticky='ew', **opts)

        combo_widget_frame.grid(row=7, column=0, columnspan=4, sticky='ew')
        for idx, key in enumerate(comb_widget_keys):
            lbl_widget[key].grid(row=0, column=idx, padx=10, pady=(10, 0), sticky='nw')
            self.input_widget[key].grid(row=1, column=idx, padx=10, pady=(0, 0), sticky='ew')

        self.input_widget['Meaning'].grid(row=3, column=0, columnspan=4, sticky='nsew', **opts)
        self.input_widget['Sentence'].grid(row=5, column=0, columnspan=4, sticky='nsew', **opts)
        self.input_widget['Synonym'].grid(row=9, column=0, columnspan=2, sticky='nsew', **opts)
        self.input_widget['Antonym'].grid(row=9, column=2, columnspan=2, sticky='nsew', **opts)
        self.input_widget['Notes'].grid(row=11, column=0, columnspan=4, sticky='nsew', **opts)

        self.cancel_btn.grid(row=12, column=0, columnspan=2, padx=(0, 10), pady=10, sticky='ne')
        self.ok_btn.grid(row=12, column=2, columnspan=2, padx=(0, 0), pady=10, sticky='nw')

    def populate_widget(self, widget_value_dict):
        '''populates widgets in the form'''
        for key, value in widget_value_dict.items():
            if isinstance(value, list):
                value = ', '.join(value)

            if key in ('Group', 'Visited'):
                continue

            if self.input_widget[key].winfo_class() in ('TEntry'):
                self.input_widget[key].insert(0, value)
            elif self.input_widget[key].winfo_class() in ('Text'):
                self.input_widget[key].insert('0.1', value)
            elif self.input_widget[key].winfo_class() in ('TCombobox'):
                self.input_widget[key].set(value)

    def get_input_values(self):
        '''returns value from widgets'''
        # instantiate an empty dictionary to pack values
        input_values = {}

        # iterate over input widgets to obtain values
        for widget_key, widget in self.input_widget.items():
            if widget.winfo_class() in ('TEntry', 'TCombobox'):
                input_values[widget_key] = widget.get().strip()
            elif widget.winfo_class() in ('Text',):
                if widget_key in ('Synonym', 'Antonym'):
                    input_values[widget_key] = widget.get("1.0", tk.END).strip().split(', ')
                else:
                    input_values[widget_key] = widget.get("1.0", tk.END).strip() 
                
        return input_values            