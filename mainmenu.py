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
    
