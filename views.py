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
        for x in colname:
            keytemp = x
            print("key",keytemp)
            lentemp = len(keytemp)
            print("key len",lentemp)
            for y in keytemp:
                valuetemp = "test"
                self.column_defs[y] = y

        testlen = len(self.column_defs)
        print("col_def len:", testlen)

        for row in self.treeview.get_children():
            self.treeview.delete(row)
            
#        for t in self.treeview["columns"]:
        #for t in self.treeview.column():        
            #self.treeview.heading = ''
#            self.treeview.column(t,width=0, stretch = 'no')

        l=len(self.treeview["columns"])
        if l>0:
            for t in range(0,l):        
                strt = '%d'%(t)
                print("range0",strt)
                self.treeview.column(strt,width=0, stretch = 'no')

        cl=len(self.column_defs.values())
        print("old len",l)

        #if cl>l:
       #     for t in range(l,cl):        
       #         strt = '%d'%(t)
       #         print("rangecl",strt)
       #         self.treeview.column(strt)
                

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
        """Clear the treeview and write the supplied data rows to it."""

        for row in self.treeview.get_children():
            self.treeview.delete(row)

        for rowdata in records:
            print(rowdata)
            values = rowdata
            self.treeview.insert(
                '', 'end',  values=values)
        self.treeview.pack()        
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
        '#0': {'label': 'Row', 'anchor': tk.W},
        'Talbe': {'label': 'tbl_name', 'width': 150, 'stretch': True}
    }
    default_width = 100
    default_minwidth = 10
    default_anchor = tk.CENTER

    def __init__(self, parent, callbacks,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        #self.inserted = inserted
        #self.updated = updated
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.treeview = ttk.Treeview(
            self,
            columns=list(self.column_defs.keys())[1:],
            selectmode='browse'
        )
        # hide first column
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

        # configure row tags
    #    self.treeview.tag_configure('inserted', background='lightgreen')
    #    self.treeview.tag_configure('updated', background='lightblue')

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
        item = self.treeview.selection()[0]
        print("you click on",item)

    def getTable(self, event):
        item = self.treeview.selection()[0]
        return item

    def on_open_record(self, *args):
        selected_id = self.treeview.selection()[0]
        self.callbacks['on_open_record'](selected_id.split('|'))

