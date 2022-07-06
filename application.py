import platform
from os import environ
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.messagebox   import showinfo, showerror, askyesno
from tkinter import scrolledtext
from tkinter.font import nametofont
from datetime import datetime
import views as v
import models as m
from mainmenu import *
from tkinter import *
from images import LOGO_32, LOGO_64

sqlite_file = '/Users/test.db'  #you may modify this sqlite file name

Version = '1.0.1'

helptext = """Sqlite Client version %s
June, 2022, Shan Yeung

Thanks to books from O'Reilly Packtpub

You can browse the records of a table by selecting the table name and click the button "Change Table".

You may execute the sql statements and save the sql statements to a text file
"""

class Application(tk.Tk):
    """Application root window"""
    toolBar    = []                       # change per instance in subclasses
    helpButton = True                     # set these in start() if need self


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("sqlite client window")

        self.taskbar_icon = tk.PhotoImage(file=LOGO_64)
        self.call('wm', 'iconphoto', self._w, self.taskbar_icon)
        

        self.logo = tk.PhotoImage(file=LOGO_32)
        tk.Label(self, image=self.logo).grid(row=0)

        #self.mySQL = ttk.LabelFrame(text=' Sqlite Database Frame')
        self.mySQL = LabelFrame(text=' Sqlite Client Frame', borderwidth=1, relief='raised')
        self.mySQL.grid(column=0, row=0, padx=4, pady=4)

        self.toolBar = [
            ('Save',  self.onSave,   {'side': LEFT}),
            ('Change Table',   self.onChangeTbl,    {'side': LEFT}),            
            ('Help',  self.help,     {'side': RIGHT}),
            ('Quit',  self.onQuit,   {'side': RIGHT})]



        datestring = datetime.today().strftime("%Y-%m-%d")
        default_filename = "sqlite_record_{}.txt".format(datestring)
        self.filename = tk.StringVar(value=default_filename)
        self.data_model = m.SQLModel(sqlite_file)
#        self.modeltype = "sql"
        if not hasattr(self, 'data_model'):
            self.destroy()
            return


        style = ttk.Style()
        self.callbacks = {
            'file->select': self.on_file_select,
            'file->quit': self.quit,
            'show_recordlist': self.show_recordlist,
            'change_table': self.onChangeTbl,
            'on_save': self.onSave,
        }
        #menu_class = get_main_menu_for_os(platform.system())
        menu_class = get_main_menu_for_os('Darwin')
        #menu = menu_class(self, self.settings, self.callbacks)
        menu = menu_class(self, self.callbacks)
        self.config(menu=menu)
        
        self.current_table = 'sqlite_sequence'


       
        stmtFrame = ttk.LabelFrame(self.mySQL, text=' SQL statements ')
        stmtFrame.grid(row=1, padx=4, pady=4, sticky='WE')
        
        
        stmtW  = 50; stmtH = 6
        self.statmt = scrolledtext.ScrolledText(stmtFrame, width=stmtW, height=stmtH, wrap=tk.WORD)
        self.statmt.grid(column=0, row=3, sticky='W', columnspan=1)

        self.frametext = tk.StringVar()
        self.frametext.set(' Table : %s' % self.current_table)
        
        #self.recFrame = ttk.LabelFrame(self.mySQL, text=self.frametext)
        self.recFrame = ttk.LabelFrame(self.mySQL)
        self.recFrame.configure(text=self.frametext.get())
        self.recFrame.grid(row=2, padx=4, pady=4, sticky='WE')
        
        
        self.datalist = v.DbRecList(self.recFrame, self.callbacks)
        self.updateDatalist()
        
        self.datalist.grid(column=0, padx=10, pady=4, sticky='WE')
        
        
        
        
        
        self.recordlist = v.TableList(
            self.mySQL,
            self.callbacks
        )
        self.recordlist.grid(row=3, padx=10, sticky='WE') #NSEW
        self.populate_recordlist()



        # status bar
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self.mySQL, textvariable=self.status)
        self.statusbar.grid(sticky="we", row=4, padx=10)

        btnFrame = ttk.LabelFrame(self.mySQL)
        btnFrame.grid(row=4, padx=1, pady=1, sticky='WE')
        
       

        self.makeToolBar(btnFrame)                      # done here: build toolbar
        
        #if self.text_edit_modified():    
        #    if not askyesno('sqlite client', 'Text has changed: discard changes?'):
        #        return



    def show_recordlist(self):
        self.recordlist.tkraise()

    def populate_recordlist(self):
        try:
            rows = self.data_model.get_tables()
        except Exception as e:
            messagebox.showerror(
                title='Error',
                message='Problem reading file',
                detail=str(e)
            )
        else:
            self.recordlist.populate(rows)
            
#    def populate_tbl_record(self):



    def getCurrentTable(self):
 
        self.current_table=self.recordlist.getTable()

    def onChangeTbl(self):
        self.getCurrentTable()
        self.updateDatalist()
        self.updateTblName()
        
    def updateTblName(self):        
        #self.recFrame.text = ' Table : %s' % self.current_table
        self.frametext.set(' Table : %s' % self.current_table)
        self.recFrame.configure(text=self.frametext.get())


    def updateDatalist(self):        
        cols = []
        coln = self.data_model.get_field_names(self.current_table)
        cols.append(coln)
        try:
            fields=self.data_model.get_all_record(self.current_table)
            
        except Exception as e:
            messagebox.showerror(
                title='Error',
                message='Problem reading file',
                detail=str(e)
            )
        else:
            self.datalist.populate_col(cols)
            self.datalist.populate_rec(fields)
        
      #          self.recordform.load_record(rownum, record)
      #  self.recordform.tkraise()



    def onSave(self):
        """Handles save button clicks"""

        # Check for errors first
        errors = self.recordform.get_errors()
        if errors:
            message = "Cannot save record"
            detail = "The following fields have errors: \n  * {}".format(
                '\n  * '.join(errors.keys())
            )
            self.status.set(
                "Cannot save, error in fields: {}"
                .format(', '.join(errors.keys()))
            )
            messagebox.showerror(title='Error', message=message, detail=detail)

            return False

        data = self.recordform.get()
        rownum = self.recordform.current_record
        try:
            if self.modeltype == "sql":
                self.data_model.save_record(data, rownum)
            else:
                self.data_model.save_csvrecord(data, rownum)
        except IndexError as e:
            messagebox.showerror(
                title='Error',
                message='Invalid row specified',
                detail=str(e)
            )
            self.status.set('Tried to update invalid row')

        except Exception as e:
            messagebox.showerror(
                title='Error',
                message='Problem saving record',
                detail=str(e)
            )
            self.status.set('Problem saving record')

        else:
            self.records_saved += 1
            self.status.set(
                "{} records saved this session".format(self.records_saved)
            )
            if rownum is not None:
                self.updated_rows.append(rownum)
            else:
                # we just inserted row number equal to one less than
                # the number of rows in the CSV
                rownum = len(self.data_model.get_all_records()) - 1
                self.inserted_rows.append(rownum)
            self.populate_recordlist()
            # Only reset the form when we're appending records
            if self.recordform.current_record is None:
                self.recordform.reset()


    def on_file_select(self):
        """Handle the file->select action from the menu"""

        filename = filedialog.asksaveasfilename(
            title='Select the target file for saving records',
            defaultextension='.csv',
            filetypes=[('CSV', '*.csv *.CSV')]
        )
        if filename:
            self.filename.set(filename)
            self.data_model = m.CSVModel(filename=self.filename.get())
            self.populate_recordlist()
            self.inserted_rows = []
            self.updated_rows = []
            
    def onQuit(self):                              # on a Quit request in the GUI
        #close = not self.text_edit_modified()      # check self, ask?, check others
        #if not close:
        #    close = askyesno('PyEdit', 'Text changed: quit and discard changes?')
        #if close:
        #    windows = TextEditor.editwindows
        #    changed = [w for w in windows if w != self and w.text_edit_modified()]
        #    if not changed:
        #        GuiMaker.quit(self) # quit ends entire app regardless of widget type
        #    else:
        #        numchange = len(changed)
        #        verify = '%s other edit window%s changed: quit and discard anyhow?'
        #        verify = verify % (numchange, 's' if numchange > 1 else '')
         #       if askyesno('PyEdit', verify):
        #            GuiMaker.quit(self)
        self.destroy()
        
        
    def help(self):
        showinfo('About Sqlite Client', helptext % Version)
        
    def makeToolBar(self, parent):
        """
        make button bar at bottom, if any
        expand=no, fill=x so same width on resize
        this could support images too: see Chapter 9,
        would need prebuilt gifs or PIL for thumbnails
        """
        if self.toolBar:
            toolbar = Frame(parent, cursor='hand2', relief=SUNKEN, bd=2)
            toolbar.pack(side=BOTTOM, fill=X)
            for (name, action, where) in self.toolBar:
                Button(toolbar, text=name, command=action).pack(where)







            



