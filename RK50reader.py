# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter
from tkinter import filedialog
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd

root = tkinter.Tk()
root.lift()
root.withdraw() #use to hide tkinter window

def search_for_file_path ():
    currdir = os.getcwd()
    tempfile = filedialog.askopenfile(parent=root, initialdir=currdir, title='Please select a file')
    if tempfile:
        print ("You chose: %s" % tempfile)
    return tempfile



with open('20-0401.mps', 'rb') as f2:
    data = f2.read().decode('utf-8','ignore')
    print(data)