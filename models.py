import csv
import os
import json
#from .constants import FieldTypes as FT
from constants import FieldTypes as FT
import sqlite3

class SQLModel:
    def __init__(self, db):
        try:
            self.conn=sqlite3.connect(db)
            self.cursor=self.conn.cursor()
            print("connect ok!")
            #self.cursor.execute("SELECT tbl_name from sqlite_master")
           # self.tbls = self.cursor.fetchall()
            print("query ok")
        except:
            print("connect failed")


    def find_all_records(self, col1, col2, tname, var01="", var02=""):
        if  var01!="" and var02!="":
            self.cursor.execute("SELECT * FROM {tb} WHERE {c01} LIKE ? AND {c02} LIKE ? ".format(tb=tname,c01=col01,c02=col02),('%'+var01+'%','%'+var02+'%'))
        elif var01!="":
            self.cursor.execute("SELECT * FROM {tb} WHERE {c01} LIKE ?".format(tb=tname,c01=col01),('%'+var01+'%',))
        elif var02!="":
            self.cursor.execute("SELECT * FROM {tb} WHERE {c02} LIKE ?".format(tb=tname,c02=col02),('%'+var02+'%',))
        data=self.cursor.fetchall()
        return data
        
    def get_tables(self):
        self.cursor.execute("SELECT tbl_name from sqlite_master")
        data=self.cursor.fetchall()
        return data

    def get_fields(self, tblname):
        self.cursor.execute("pragma table_info({tb})".format(tb=tblname))
        data=self.cursor.fetchall()
        return data

    def get_field_names(self, tblname):
        self.cursor.execute("pragma table_info({tb})".format(tb=tblname))
        data=self.cursor.fetchall()
        print("fieldname:",data)
        n = []
        for r in data:
            n.append(r[1])
        return n

    def get_field_types(self, tblname):
        self.cursor.execute("pragma table_info({tb})".format(tb=tblname))
        data=self.cursor.fetchall()
        return data[2]
      
    def get_all_record(self, tname):
        self.cursor.execute("SELECT * FROM {tb}".format(tb=tname))
        result = self.cursor.fetchall()
        print(result)
        return result if result else {}


    def get_record(self, tname, id_no):
        self.cursor.execute("SELECT * FROM {tb} WHERE id = ?".format(tb=tname),(id_no))
        result = self.cursor.fetchall()
        print(result)
        return result[0] if result else {}



    def save_record(self, record):
        #raise NotImplementedError("This still needs to be implemented for the SQL command.")
        print("This still needs to be implemented for the SQL command.")

 

    def __del__(self):
        self.conn.close()




class SettingsModel:
    """A model for saving settings"""

    variables = {
        'autofill date': {'type': 'bool', 'value': True},
        'autofill sheet data': {'type': 'bool', 'value': True},
        'font size': {'type': 'int', 'value': 9},
        'theme': {'type': 'str', 'value': 'default'}
    }

    def __init__(self, filename='abq_settings.json', path='~'):
        # determine the file path
        self.filepath = os.path.join(os.path.expanduser(path), filename)

        # load in saved values
        self.load()

    def set(self, key, value):
        """Set a variable value"""
        if (
            key in self.variables and
            type(value).__name__ == self.variables[key]['type']
        ):
            self.variables[key]['value'] = value
        else:
            raise ValueError("Bad key or wrong variable type")

    def save(self, settings=None):
        """Save the current settings to the file"""
        json_string = json.dumps(self.variables)
        with open(self.filepath, 'w', encoding='utf-8') as fh:
            fh.write(json_string)

    def load(self):
        """Load the settings from the file"""

        # if the file doesn't exist, return
        if not os.path.exists(self.filepath):
            return

        # open the file and read in the raw values
        with open(self.filepath, 'r', encoding='utf-8') as fh:
            raw_values = json.loads(fh.read())

        # don't implicitly trust the raw values, but only get known keys
        for key in self.variables:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.variables[key]['value'] = raw_value
