# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 15:59:47 2022

@author: Alexis.Vivien

This script takes a BlogOut folder and returns all the informations

Last update 17.01.2022

ANY NON-AUTHORIZED USER MODIFICATIONS WILL LEAD TO JUDICIARY PROCEDURES
"""
import tkinter
from tkinter import filedialog
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

root = tkinter.Tk()
root.lift()
root.withdraw() #use to hide tkinter window

def search_for_file_path ():
    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    if len(tempdir) > 0:
        print ("You chose: %s" % tempdir)
    return tempdir

def bin_type(files):
    cnt = 0; treatmentCnt = 0; globalCnt = 0
    l = list([])
    temp = np.empty([128,1], dtype = float)
    for path in files:
        if path.find('BLOG_THERMISTOR') > -1: 
            f = open(file_path_variable + '/' + path,'rb')
            temp = np.insert(temp,cnt+1, np.frombuffer(f.read(4*128), dtype=np.float32), axis =1)
            cnt=cnt+1
        if path.find('TREATMENTCONTROLINFO') > -1:
            treatmentCnt = treatmentCnt + 1
            f = open(file_path_variable + '/' + path,'rb')
            a = np.frombuffer(f.read(7*4), dtype=np.float32)
            hifuLimitVoltage = a[0:2]
            hifuVoltage = a[2]
            treatmentDuration = a[4]
            np.frombuffer(f.read(3*4), dtype=np.int32)
            powerScaleFactor = np.frombuffer(f.read(1*4), dtype=np.float32)
        if path.find('NAMEDTREATMENTPOINT') > -1:
            f = open(file_path_variable + '/' + path,'rb')
            a = np.frombuffer(f.read(6*4), dtype=np.float32)
            pointCoord = a[0:3]
            b = np.frombuffer(f.read(8),dtype=np.float64) #a double is encoded as a 8-bytes float in python (aka float 64)
            patternDutyCycle = b
            c = np.frombuffer(f.read(4*3), dtype=np.int32)
            patternRepetitionTime = c[0]; isTimingUniform = c[1]; patternPointTreatmentTime = c[2]
            f.read(48)
            e = f.read(100).decode('utf-8')
            treatmentPointName = e
            l.append( [treatmentCnt, hifuLimitVoltage, hifuVoltage, treatmentDuration, powerScaleFactor,
                              pointCoord, patternDutyCycle, patternRepetitionTime, isTimingUniform,
                              patternPointTreatmentTime, treatmentPointName])
            globalCnt = globalCnt + 1       
        if path.find('HYDROPHONEDATA') > -1:
            f = open(file_path_variable + '/' + path, 'rb')
            time = np.frombuffer(f.read(8), dtype=np.int64)
            sig = np.frombuffer(f.read(), dtype=np.uint16)
    temp = np.delete(temp,0,1)
    return l, temp
                       
file_path_variable = search_for_file_path()
sheet_name = 'Sheet 1'
files = [f for f in listdir(file_path_variable) if isfile(join(file_path_variable, f))]
l,temp = bin_type(files)
df = pd.DataFrame(l)
colnames = ['TreatmentCount','HIFULimitVoltage', 'HIFUVoltage', 'TreatmentDuration','PowerScaleFactor',
            'PointCoord','PatternDutyCycle','PatternRepetitionTime', 'isTimingUniform', 'patterPointTreatmentTime',
            'TreatmentPointName']

#-------------------------------------------------------------------------
##########################################################################
## HERE FOR THE NAME OF THE EXCEL FILE - DON'T MODIFY ANYTHING BUT THIS ##

writer = pd.ExcelWriter('Results.xlsx',engine='xlsxwriter')

################### END OF USER MODIFYING RIGHTS #########################
##########################################################################
#-------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10,6))
for i in range(31):
    ax.plot(temp[i,:])
ax.axhline(y = 18, xmin=0, xmax=temp.shape[1], color='red', linestyle="--", label='System Temperature Limit : 18°C')
ax.set_xlabel('Time [s]')
ax.set_ylabel('Temperature [°C]')
ax.set_title('Transducers Temperature Response With Time')
ax.legend(loc='upper left')


df.to_excel(writer, sheet_name=sheet_name, index=False,header=colnames)
for column in df:
    col_idx = df.columns.get_loc(column)
    writer.sheets[sheet_name].set_column(col_idx, col_idx, len(colnames[col_idx])+2) # set columns widths
col_idx = df.columns.get_loc(5)    
writer.sheets[sheet_name].set_column(col_idx, col_idx, 35)    # point coord column width is set a bit larger
writer.save()


