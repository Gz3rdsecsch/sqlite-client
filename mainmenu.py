import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import sys
from tkinter import *                     # widget classes
from tkinter.messagebox import showinfo


class GenericMainMenu(tk.Menu):
    """The Application's main menu"""

    def __init__(self, parent, callbacks, **kwargs):
#    def __init__(self, parent, settings, callbacks, **kwargs):
        """Constructor for MainMenu

        arguments:
          parent - The parent widget
          settings - a dict containing Tkinter variables
          callbacks - a dict containing Python callables
        """
        super().__init__(parent, **kwargs)
        #self.settings = settings
        self.callbacks = callbacks
        self._build_menu()
        self._bind_accelerators()

    def _build_menu(self):
        # The file menu
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(
            label="Select file…",
            command=self.callbacks['file->select'],
            accelerator='Ctrl+O'
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Quit",
            command=self.callbacks['file->quit'],
            accelerator='Ctrl+Q'
        )
        self.add_cascade(label='File', menu=file_menu)


        # switch from recordlist to recordform
        go_menu = tk.Menu(self, tearoff=False)
        go_menu.add_command(
            label="Record List",
            command=self.callbacks['show_recordlist'],
            accelerator='Ctrl+L'
        )
        #jy:

        
        
        go_menu.add_command(
            label="New Record",
            command=self.callbacks['new_record'],
            accelerator='Ctrl+N'
        )
        self.add_cascade(label='Go', menu=go_menu)

        # The help menu
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label='About…', command=self.show_about)
        self.add_cascade(label='Help', menu=help_menu)

    def get_keybinds(self):
        return {
            '<Control-o>': self.callbacks['file->select'],
            '<Control-q>': self.callbacks['file->quit'],
            '<Control-n>': self.callbacks['new_record'],
            '<Control-l>': self.callbacks['show_recordlist'],
        }

    @staticmethod
    def _argstrip(function, *args):
        return function()

    def _bind_accelerators(self):
        keybinds = self.get_keybinds()
        for key, command in keybinds.items():
            self.bind_all(
                key,
                partial(self._argstrip, command)
            )

    def on_theme_change(self, *args):
        """Popup a message about theme changes"""
        message = "Change requires restart"
        detail = (
            "Theme changes do not take effect"
            " until application restart")
        messagebox.showwarning(
            title='Warning',
            message=message,
            detail=detail)

    def show_about(self):
        about_message = 'Sqlite Client'
        about_detail = (
            'by ShanYeung\n'
            'For assistance please contact the authors.'
        )
        messagebox.showinfo(
            title='About',
            message=about_message,
            detail=about_detail
        )




class MacOsMainMenu(GenericMainMenu):
    """
    Differences for MacOS:

      - Create App Menu
      - Move about to app menu, remove 'help'
      - Remove redundant quit command
      - Change accelerators to Command-[]
      - Add View menu for font & theme options
      - Add Edit menu for autofill options
      - Add Window menu for navigation commands
    """

    def _build_menu(self):
        app_menu = tk.Menu(self, tearoff=False, name='apple')
        app_menu.add_command(
            label='About sqlite client',
            command=self.show_about
        )
        self.add_cascade(label='sqlite client', menu=app_menu)
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(
            label="Select file…",
            command=self.callbacks['file->select'],
            accelerator="Cmd-O"
        )
        self.add_cascade(label='File', menu=file_menu)



        # Window Menu
        window_menu = tk.Menu(self, name='window', tearoff=False)

        #self.add_cascade(label='Window', menu=window_menu)
        self.add_cascade(label='Sqlite', menu=window_menu)


    def get_keybinds(self):
        return {
            '<Command-o>': self.callbacks['file->select'],
      #      '<Command-n>': self.callbacks['new_record'],
      #      '<Command-l>': self.callbacks['show_recordlist']
        }


def get_main_menu_for_os(os_name):
    menus = {
        'Darwin': MacOsMainMenu
    }

    return menus.get(os_name, GenericMainMenu)
    
class GuiMaker(Frame):
    menuBar    = []                       # class defaults
    toolBar    = []                       # change per instance in subclasses
    helpButton = True                     # set these in start() if need self

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)        # make frame stretchable
        self.start()                            # for subclass: set menu/toolBar
        self.makeMenuBar()                      # done here: build menu bar
        self.makeWidgets()                      # for subclass: add middle part

    def makeMenuBar(self):
        """
        make menu bar at the top (Tk8.0 menus below)
        expand=no, fill=x so same width on resize
        """
        menubar = Frame(self, relief=RAISED, bd=2)
        menubar.pack(side=TOP, fill=X)

        for (name, key, items) in self.menuBar:
            mbutton  = Menubutton(menubar, text=name, underline=key)
            mbutton.pack(side=LEFT)
            pulldown = Menu(mbutton)
            self.addMenuItems(pulldown, items)
            mbutton.config(menu=pulldown)

        if self.helpButton:
            Button(menubar, text    = 'Help',
                            cursor  = 'gumby',
                            relief  = FLAT,
                            command = self.help).pack(side=RIGHT)

    def addMenuItems(self, menu, items):
        for item in items:                     # scan nested items list
            if item == 'separator':            # string: add separator
                menu.add_separator({})
            elif type(item) == list:           # list: disabled item list
                for num in item:
                    menu.entryconfig(num, state=DISABLED)
            elif type(item[2]) != list:
                menu.add_command(label     = item[0],         # command:
                                 underline = item[1],         # add command
                                 command   = item[2])         # cmd=callable
            else:
                pullover = Menu(menu)
                self.addMenuItems(pullover, item[2])          # sublist:
                menu.add_cascade(label     = item[0],         # make submenu
                                 underline = item[1],         # add cascade
                                 menu      = pullover)


    def makeWidgets(self):
        """
        make 'middle' part last, so menu/toolbar
        is always on top/bottom and clipped last;
        override this default, pack middle any side;
        for grid: grid middle part in a packed frame
        """
        name = Label(self,
                     width=40, height=10,
                     relief=SUNKEN, bg='white',
                     text   = self.__class__.__name__,
                     cursor = 'crosshair')
        name.pack(expand=YES, fill=BOTH, side=TOP)

    def help(self):
        "override me in subclass"
        showinfo('Help', 'Sorry, no help for ' + self.__class__.__name__)

    def start(self): 
        "override me in subclass: set menu/toolbar with self"
        pass


###############################################################################
# Customize for Tk 8.0 main window menu bar, instead of a frame
###############################################################################

GuiMakerFrameMenu = GuiMaker           # use this for embedded component menus

class GuiMakerWindowMenu(GuiMaker):    # use this for top-level window menus
    def makeMenuBar(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        for (name, key, items) in self.menuBar:
            pulldown = Menu(menubar)
            self.addMenuItems(pulldown, items)
            menubar.add_cascade(label=name, underline=key, menu=pulldown)

        if self.helpButton:
            if sys.platform[:3] == 'win':
                menubar.add_command(label='Help', command=self.help)
            else:
                pulldown = Menu(menubar)  # Linux needs real pull down
                pulldown.add_command(label='About', command=self.help)
                menubar.add_cascade(label='Help', menu=pulldown)


