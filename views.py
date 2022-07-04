import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from collections import defaultdict





class DbRecList(tk.Frame):
    column_defs = {
    }
    default_width = 100
    default_minwidth = 10
    default_anchor = tk.CENTER

    def __init__(self, parent, callbacks,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.treeview = ttk.Treeview(
            self,
            columns=[],
            selectmode='browse'
        )
        # hide first column
        self.treeview.config(show='headings')


        
        


    def populate_col(self, colname):
        """Clear the treeview and write the supplied data rows to it."""
        self.column_defs = {}
        for x in colname:
            keytemp = x
            for y in keytemp:
                self.column_defs[y] = y


        for row in self.treeview.get_children():
            self.treeview.delete(row)
            

        l=len(self.treeview["columns"])
        if l>0:
            for t in range(0,l):        
                strt = '%d'%(t)
                print("range0",strt)
                self.treeview.column(strt,width=0, stretch = 'no')
                

        cl=len(self.column_defs.values())

                

        cnt = 0
        self.treeview["columns"] = list(self.column_defs.keys())[0:]
        for v in self.column_defs.values():
            strt = '%d'%(cnt)
            print('coldef: ',strt)
            self.treeview.column(strt,width=100,stretch='yes')
            cnt = cnt + 1
            self.treeview.heading(v, text=v)
 

        valuekeys = list(self.column_defs.keys())[1:]

                
                
    def populate_rec(self, records):

        for row in self.treeview.get_children():
            self.treeview.delete(row)

        for rowdata in records:
            print("record:",rowdata)
            values = rowdata
            self.treeview.insert(
                '', 'end',  values=values)
        self.scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.treeview.yview
        )
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.treeview.grid(row=0, column=0, sticky='NSEW')
        self.scrollbar.grid(row=0, column=1, sticky='NSW')





class TableList(tk.Frame):
    column_defs = {
#        '#0': {'label': 'Row', 'anchor': tk.W},
        'Talbe': {'label': 'tbl_name', 'width': 150, 'stretch': True}
    }
    default_width = 100
    default_minwidth = 10
    default_anchor = tk.CENTER

    def __init__(self, parent, callbacks,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.treeview = ttk.Treeview(
            self,
            columns=list(self.column_defs.keys())[0:],
            selectmode='browse'
        )
        self.treeview.config(show='headings')

        # configure scrollbar for the treeview
        self.scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.treeview.yview
        )
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.treeview.grid(row=0, column=0, sticky='NSEW')
        self.scrollbar.grid(row=0, column=1, sticky='NSW')

        # Configure treeview columns
        for name, definition in self.column_defs.items():
            label = definition.get('label', '')
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)
            self.treeview.heading(name, text=label)
            self.treeview.column(name, width=width, stretch=stretch)


        # Bind double-clicks
        self.treeview.bind('<<TreeviewOpen>>', self.on_open_record)
        self.treeview.bind('<Double-1>', self.OnDoubleClick)

    def populate(self, rows):
        """Clear the treeview and write the supplied data rows to it."""

        for row in self.treeview.get_children():
            self.treeview.delete(row)

        valuekeys = list(self.column_defs.keys())[1:]
        for rowdata in rows:
            print(rowdata)
            values = rowdata
            self.treeview.insert(
                '', 'end',  values=values)

    def OnDoubleClick(self, event):
        sel_item = self.treeview.selection()[0]
        x = self.treeview.item(sel_item)
        print("x:",x)
        print("you click on",x.get('values',''))
        #for t in x.get('values',''):
        t = x.get('values','')[0]
        print("tbl",t)

    def getTable(self):
        sel_item = self.treeview.selection()[0]
        x = self.treeview.item(sel_item)
        t = x.get('values','')[0]
        return t

    def on_open_record(self, *args):
        selected_id = self.treeview.selection()[0]
        self.callbacks['on_open_record'](selected_id.split('|'))

