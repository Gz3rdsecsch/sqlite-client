import platform
from os import environ
import sys, os
import tkinter as tk
from tkinter import ttk
#from tkinter import filedialog
from tkinter.filedialog   import Open, SaveAs
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
    startfiledir = '.'                   # for dialogs

    ftypes = [('All files',     '*'),                 # for file open dialog
              ('Text files',   '.txt'),               # customize in subclass
              ('Sql files',   '.sql'),
              ('Python files', '.py')]                # or set in each instance


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
            ('Save',  self.onSaveAs,   {'side': LEFT}),
            ('Change Table',   self.onChangeTbl,    {'side': LEFT}),    
            ('Execute SQL(no commit)',   self.onExeStatemnt,    {'side': LEFT}),        
            ('Help',  self.help,     {'side': RIGHT}),
            ('Quit',  self.onQuit,   {'side': RIGHT})]



        datestring = datetime.today().strftime("%Y-%m-%d")
        default_filename = "sqlite_record_{}.txt".format(datestring)
        self.filename = tk.StringVar(value=default_filename)

        self.data_model = m.SQLModel(sqlite_file)
        self.knownEncoding = sys.getdefaultencoding()
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
        self.openDialog = None
        self.saveDialog = None


       
        stmtFrame = ttk.LabelFrame(self.mySQL, text=' SQL statements ')
        stmtFrame.grid(column=0, row=1, padx=4, pady=4, sticky='WE')

        resultFrame = ttk.LabelFrame(self.mySQL, text=' SQL results ')
        resultFrame.grid(column=1,row=1, padx=4, pady=4, sticky='WE')
        
        
        stmtW  = 50; stmtH = 6
        self.sqlresult = scrolledtext.ScrolledText(resultFrame, width=stmtW, height=stmtH, wrap=tk.WORD)
        #self.statmt.grid(column=0, row=3, sticky='W', columnspan=1)
        self.text  = tk.Text(stmtFrame, width=stmtW, height=stmtH, padx=5, wrap='none')        # disable line wrapping
        #self.text.grid(column=0, row=3, sticky='W', columnspan=1)
        self.text.grid(column=0, row=3, sticky='WE')
        #self.sqlresult.grid(column=1, row=3, sticky='W', columnspan=1)
        self.sqlresult.grid(column=1, row=3, sticky='WE')

        self.frametext = tk.StringVar()
        self.frametext.set(' Table : %s' % self.current_table)
        
        #self.recFrame = ttk.LabelFrame(self.mySQL, text=self.frametext)
        self.recFrame = ttk.LabelFrame(self.mySQL)
        self.recFrame.configure(text=self.frametext.get())
        self.recFrame.grid(row=2, padx=4, pady=4, sticky='WE', columnspan=2)
        
        
        self.datalist = v.DbRecList(self.recFrame, self.callbacks)
        self.updateDatalist()
        
        self.datalist.grid(column=0, padx=10, pady=4, sticky='WE', columnspan=2)
        
        
        
        
        
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





    def on_file_select(self):

            
        if self.text_edit_modified():    # 2.0
            if not askyesno('sqlite Client', 'Text has changed: discard changes?'):
                return

        file = self.my_askopenfilename()
        if not file: 
            return
        
        if not os.path.isfile(file):
            showerror('sqlite Client', 'Could not open file ' + file)
            return

        # try known encoding if passed and accurate (e.g., email)
        text = None     # empty file = '' = False: test for None!
        try:
            text = open(file, 'r', encoding=self.knownEncoding).read()
        except (UnicodeError, LookupError, IOError):         # lookup: bad name
            pass



        # try platform default (utf-8 on windows; try utf8 always?)
        if text == None:
            try:
                text = open(file, 'r', encoding=sys.getdefaultencoding()).read()
                
            except (UnicodeError, LookupError, IOError):
                pass

        # last resort: use binary bytes and rely on Tk to decode
        if text == None:
            try:
                text = open(file, 'rb').read()         # bytes for Unicode
                text = text.replace(b'\r\n', b'\n')    # for display, saves
#                self.knownEncoding = None
            except IOError:
                pass

        if text == None:
            showerror('sqlite client', 'Could not decode and open file ' + file)
        else:
            self.setAllText(text)
            #self.statmt.configure(text=
            #self.setFileName(file)
            #self.text.edit_reset()             # 2.0: clear undo/redo stks
            #self.statmt.ScrolledText.ScrolledText.text.edit_modified(0)         # 2.0: clear modified flag
            self.text.edit_modified(0)

    def getAllText(self):
        return self.text.get('1.0', END+'-1c')    # extract text as str string
    def setAllText(self, inputext):
        """
        caller: call self.update() first if just packed, else the
        initial position may be at line 2, not line 1 (2.1; Tk bug?)
        """
        self.text.delete('1.0', END)              # store text string in widget
        self.text.insert(END, inputext)
        #self.statmt.text.insert(END, text)               # or '1.0'; text=bytes or str
        #self.statmt.text.mark_set(INSERT, '1.0')         # move insert point to top
        self.text.see(INSERT)                     # scroll to top, insert set
        
    def clearAllText(self):
        self.text.delete('1.0', END)              # clear text in widget

    def getFileName(self):
        return self.currfile
    def setFileName(self, name):                  # see also: onGoto(linenum)
        #self.currfile = name  # for save
        self.filename.set(name)
        #self.filelabel.config(text=str(name))



    def onExeStatemnt(self):
        """Handle the file->select action from the menu"""

        sqlstmt = self.getAllText()
        result_txt = self.data_model.exe_sql(sqlstmt)
        self.sqlresult.delete('1.0', END) 
        self.sqlresult.insert(tk.INSERT, result_txt)

            
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

    def text_edit_modified(self):
        """
        2.1: this now works! seems to have been a bool result type issue in tkinter;
        2.0: self.text.edit_modified() broken in Python 2.4: do manually for now; 
        """
        #return self.statmt.ScrolledText.ScrolledText.text.edit_modified()
        return self.text.edit_modified()
        
        
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

    def onSave(self):
        self.onSaveAs(self.currfile)  # may be None

    def onSaveAs(self, forcefile=None):
        filename = forcefile or self.my_asksaveasfilename()
        if not filename:
            return

        text = self.getAllText()      # 2.1: a str string, with \n eolns,
        encpick = None                # even if read/inserted as bytes 

        # try known encoding at latest Open or Save, if any
        if self.knownEncoding:     # on SaveAs?
            try:
                text.encode(self.knownEncoding)
                encpick = self.knownEncoding
            except UnicodeError:
                pass


            try:
                file = open(filename, 'w', encoding=encpick)
                file.write(text)
                file.close()
            except:
                showerror('sqlite client', 'Could not write file ' + filename)
            else:
                self.setFileName(filename)          # may be newly created
                self.text.edit_modified(0)          # 2.0: clear modified flag
                self.knownEncoding = encpick        # 2.1: keep enc for next save

    def my_asksaveasfilename(self):    # objects remember last result dir/file
        if not self.saveDialog:
           self.saveDialog = SaveAs(initialdir=self.startfiledir,
                                    filetypes=self.ftypes)
        return self.saveDialog.show()
                







            



