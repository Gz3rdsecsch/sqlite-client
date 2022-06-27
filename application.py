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

sqlite_file = '/Users/jy3.8.31.db'  #you may modify this sqlite file name


class Application(tk.Tk):
    """Application root window"""


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("sqlite client entry")

        self.taskbar_icon = tk.PhotoImage(file=LOGO_64)
        self.call('wm', 'iconphoto', self._w, self.taskbar_icon)
        

        self.logo = tk.PhotoImage(file=LOGO_32)
        tk.Label(self, image=self.logo).grid(row=0)

        #self.mySQL = ttk.LabelFrame(text=' Sqlite Database Frame')
        self.mySQL = LabelFrame(text=' Sqlite table Frame', borderwidth=1, relief='raised')
        self.mySQL.grid(column=0, row=0, padx=8, pady=4)

        self.toolBar = [
            ('Save',  self.onSave,   {'side': LEFT}),
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
            'new_record': self.open_record,
            'on_open_record': self.open_record,
            'on_save': self.onSave,
            'show_dropdownlist': self.show_dropdownlist,
        }
        #menu_class = get_main_menu_for_os(platform.system())
        menu_class = get_main_menu_for_os('Darwin')
        #menu = menu_class(self, self.settings, self.callbacks)
        menu = menu_class(self, self.callbacks)
        self.config(menu=menu)

        fields=self.data_model.get_all_record('others')
        cols = []
        coln = self.data_model.get_field_names('others')
        cols.append(coln)

 #       self.recordform = v.DataRecordForm(
#           self, self.data_model.fields, self.settings, self.callbacks)
        self.recordform = v.DataRecordForm(self.mySQL, cols, fields, self.callbacks)
   #     self.recordform = v.DataRecordForm(self.mySQL, cols, fields, self.settings, self.callbacks)
        self.recordform.grid(row=1, padx=10, sticky='WE')  #NSEW
        
        quoteFrame = ttk.LabelFrame(self.mySQL, text=' SQL statements ')
        quoteFrame.grid(row=2, padx=4, pady=4)
        
        
        quoteW  = 40; quoteH = 6
        self.statmt = scrolledtext.ScrolledText(quoteFrame, width=quoteW, height=quoteH, wrap=tk.WORD)
        self.statmt.grid(column=0, row=3, sticky='W', columnspan=1)
        
        self.datalist = v.DbRecList(self.mySQL, cols, fields, self.callbacks)
        self.datalist.grid(row=3, padx=10, sticky='WE')
        
        self.recordlist = v.TableList(
            self.mySQL,
            self.callbacks
        )
        self.recordlist.grid(row=4, padx=10, sticky='WE') #NSEW
        self.populate_recordlist()



        # status bar
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self.mySQL, textvariable=self.status)
        self.statusbar.grid(sticky="we", row=4, padx=10)

        self.records_saved = 0

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
            
    def show_dropdownlist(self):
        self.dropdownlist.tkraise()

    def populate_dropdownlist(self):
        try:
            rows = self.data_model.get_tables()
        except Exception as e:
            messagebox.showerror(
                title='Error',
                message='Problem reading file',
                detail=str(e)
            )
        else:
            self.dropdownlist.populate(rows)
            

    def open_record(self, rownum=None):
        if rownum is None:
            record = None
        else:
            rownum = int(rownum)
            try:
                if self.modeltype == "sql":
                    record = self.data_model.get_record(rownum)
                else:
                    record = self.data_model.get_csvrecord(rownum)
            except Exception as e:
                messagebox.showerror(
                    title='Error',
                    message='Problem reading file',
                    detail=str(e)
                )
                return
        self.recordform.load_record(rownum, record)
        self.recordform.tkraise()



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
            
    def onQuit(self):
        """
        on Quit menu/toolbar select and wm border X button in toplevel windows;
        2.1: don't exit app if others changed;  2.0: don't ask if self unchanged;
        moved to the top-level window classes at the end since may vary per usage:
        a Quit in GUI might quit() to exit, destroy() just one Toplevel, Tk, or 
        edit frame, or not be provided at all when run as an attached component;
        check self for changes, and if might quit(), main windows should check
        other windows in the process-wide list to see if they have changed too; 
        """
        assert False, 'onQuit must be defined in window-specific sublass' 
        
    def help(self):
        showinfo('About PyEdit', helptext % ((Version,)*2))
        







            



